"""
Work Groups API endpoints
"""
from flask import jsonify, request, session
from functools import wraps
from app.models.work_group import WorkGroup, WorkGroupItem
from app.utils.auth_utils import login_required

def group_owner_required(f):
    @wraps(f)
    def decorated_function(group_id, *args, **kwargs):
        group = WorkGroup.get_by_id(group_id)
        if not group or group['created_by'] != session.get('user_id'):
            return jsonify({'error': 'Unauthorized access to work group'}), 403
        return f(group_id, *args, **kwargs)
    return decorated_function

@login_required
def create_work_group():
    """Create a new work group"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request format'}), 400

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({'error': 'Group name is required'}), 400
    
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    try:
        group_id = WorkGroup.create(
            name=name,
            description=description,
            created_by=session['user_id']
        )
        return jsonify({
            'message': 'Work group created successfully',
            'group_id': group_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@login_required
def get_user_groups():
    """Get all work groups for the current user"""
    try:
        groups = WorkGroup.get_by_user(session['user_id'])
        return jsonify({
            'groups': [{
                'id': group['id'],
                'name': group['name'],
                'description': group['description'],
                'created_at': group['created_at']
            } for group in groups]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@login_required
@group_owner_required
def update_work_group(group_id):
    """Update a work group's details"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request format'}), 400

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    try:
        success = WorkGroup.update(
            group_id=group_id,
            user_id=session['user_id'],
            name=name,
            description=description
        )
        if success:
            return jsonify({'message': 'Work group updated successfully'}), 200
        return jsonify({'error': 'No changes made'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@login_required
@group_owner_required
def delete_work_group(group_id):
    """Delete a work group"""
    try:
        WorkGroup.delete(group_id, session['user_id'])
        return jsonify({'message': 'Work group deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@login_required
def get_group_details(group_id):
    """Get work group details including its items"""
    group = WorkGroup.get_by_id(group_id)
    if not group:
        return jsonify({'error': 'Work group not found'}), 404
        
    items = WorkGroupItem.get_group_items(group_id)
    
    return jsonify({
        'group': {
            'id': group['id'],
            'name': group['name'],
            'description': group['description'],
            'created_at': group['created_at'],
            'is_owner': group['created_by'] == session.get('user_id'),
            'items': [{
                'id': item['id'],
                'name': item['name'],
                'file_type': item['file_type'],
                'description': item['description'],
                'added_at': item['added_at']
            } for item in items]
        }
    }), 200

@login_required
@group_owner_required
def add_item_to_group(group_id):
    """Add an inventory item to a work group"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request format'}), 400

    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400
        
    try:
        item_group_id = WorkGroupItem.add_item(
            group_id=group_id,
            item_id=item_id,
            user_id=session['user_id']
        )
        return jsonify({
            'message': 'Item added to work group successfully',
            'item_group_id': item_group_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to add item to work group'}), 400

@login_required
@group_owner_required
def remove_item_from_group(group_id, item_id):
    """Remove an inventory item from a work group"""
    try:
        WorkGroupItem.remove_item(
            group_id=group_id,
            item_id=item_id,
            user_id=session['user_id']
        )
        return jsonify({'message': 'Item removed from work group successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
