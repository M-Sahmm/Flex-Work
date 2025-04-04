from flask import render_template, request, jsonify, session, redirect, url_for
from flask_wtf.csrf import validate_csrf
from app.models.task import (
    init_task_table,
    get_user_tasks,
    add_task,
    update_task_status as update_status,
    delete_task as remove_task
)

# Initialize tasks table
init_task_table()

def workpad():
    """Render workpad page"""
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
    
    try:
        # Get tasks for the current user
        user_tasks = get_user_tasks(session['user_id'])
        
        # Ensure we have the expected structure
        tasks_data = {
            'tasks': user_tasks.get('tasks', {}),
            'metadata': user_tasks.get('metadata', {
                'total_tasks': 0,
                'todo': 0,
                'in_progress': 0,
                'completed': 0
            })
        }
        
        return render_template('workpad.html', 
                             tasks=tasks_data['tasks'],
                             task_metadata=tasks_data['metadata'])
    
    except Exception:
        # Return empty data structure on error
        return render_template('workpad.html', 
                             tasks={},
                             task_metadata={
                                 'total_tasks': 0,
                                 'todo': 0,
                                 'in_progress': 0,
                                 'completed': 0
                             })

def create_task():
    """Create a new task"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        title = data.get('title')
        description = data.get('description', '')
        
        task_id = add_task(session['user_id'], title, description)
        
        if task_id:
            return jsonify({
                'message': 'Task created successfully',
                'task_id': task_id
            }), 201
        
        return jsonify({'error': 'Failed to create task'}), 500
        
    except Exception as e:
        print(f"Error in create_task: {str(e)}")  # Debug log
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def update_task_status(task_id):
    """Update task status"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        # Get CSRF token from header
        csrf_token = request.headers.get('X-CSRF-Token')
        if not csrf_token:
            return jsonify({'error': 'CSRF token missing'}), 400
            
        try:
            validate_csrf(csrf_token)
        except Exception as e:
            return jsonify({'error': 'Invalid CSRF token'}), 400
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        if data['status'] not in ['todo', 'in_progress', 'completed']:
            return jsonify({'error': 'Invalid status'}), 400
        
        success = update_status(session['user_id'], task_id, data['status'])
        
        if success:
            return jsonify({'message': 'Task status updated successfully'}), 200
        return jsonify({'error': 'Failed to update task status'}), 500
        
    except Exception as e:
        print(f"Error in update_task_status: {str(e)}")
        return jsonify({'error': str(e)}), 500

def delete_task(task_id):
    """Delete task"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        # Get CSRF token from header
        csrf_token = request.headers.get('X-CSRF-Token')
        if not csrf_token:
            return jsonify({'error': 'CSRF token missing'}), 400
            
        try:
            validate_csrf(csrf_token)
        except Exception as e:
            return jsonify({'error': 'Invalid CSRF token'}), 400
        
        success = remove_task(session['user_id'], task_id)
        
        if success:
            return jsonify({'message': 'Task deleted successfully'}), 200
        return jsonify({'error': 'Failed to delete task'}), 500
        
    except Exception as e:
        print(f"Error in delete_task: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_task_stats():
    """Get task statistics"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
            
        user_tasks = get_user_tasks(session['user_id'])
        return jsonify(user_tasks.get('metadata', {
            'total_tasks': 0,
            'todo': 0,
            'in_progress': 0,
            'completed': 0
        }))
        
    except Exception as e:
        print(f"Error getting task stats: {str(e)}")
        return jsonify({'error': str(e)}), 500
