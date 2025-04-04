from flask import session, render_template, redirect, url_for, flash, request, jsonify
from app.utils.db_utils import get_db, execute_query, execute_single_query, execute_write_query, DatabaseError

def create_organization():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    name = request.form.get('name')
    if not name:
        return jsonify({'error': 'Organization name is required'}), 400
    
    try:
        # Check if organization name already exists
        existing = execute_single_query(
            'SELECT id FROM organizations WHERE name = ?',
            (name,)
        )
        if existing:
            return jsonify({'error': 'Organization name already exists'}), 400
            
        # Create organization
        with get_db() as conn:
            # Insert organization
            cursor = conn.execute(
                'INSERT INTO organizations (name) VALUES (?)',
                (name,)
            )
            org_id = cursor.lastrowid
            
            # Add creator as admin
            conn.execute('''
                INSERT INTO user_organizations (user_id, organization_id, role)
                VALUES (?, ?, ?)
            ''', (session['user_id'], org_id, 'admin'))
            
        return jsonify({
            'message': 'Organization created successfully',
            'id': org_id
        })
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to create organization'}), 500

def delete_organization():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    org_id = request.form.get('organization_id')
    if not org_id:
        return jsonify({'error': 'Organization ID is required'}), 400
        
    try:
        # Check if user is admin
        is_admin = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ? AND role = 'admin'
        ''', (session['user_id'], org_id))
        
        if not is_admin:
            return jsonify({'error': 'Only admins can delete organizations'}), 403
            
        with get_db() as conn:
            # Delete organization and all related data
            conn.execute('DELETE FROM organizations WHERE id = ?', (org_id,))
            
        return jsonify({'message': 'Organization deleted successfully'})
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to delete organization'}), 500

def leave_organization():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    org_id = request.form.get('organization_id')
    if not org_id:
        return jsonify({'error': 'Organization ID is required'}), 400
        
    try:
        with get_db() as conn:
            # Check if user is the last admin
            admin_count = conn.execute('''
                SELECT COUNT(*) as count 
                FROM user_organizations 
                WHERE organization_id = ? AND role = 'admin'
            ''', (org_id,)).fetchone()['count']
            
            user_role = conn.execute('''
                SELECT role 
                FROM user_organizations 
                WHERE user_id = ? AND organization_id = ?
            ''', (session['user_id'], org_id)).fetchone()
            
            if user_role and user_role['role'] == 'admin' and admin_count <= 1:
                return jsonify({
                    'error': 'Cannot leave organization. You are the last admin.'
                }), 400
            
            # Remove user from organization
            conn.execute('''
                DELETE FROM user_organizations 
                WHERE user_id = ? AND organization_id = ?
            ''', (session['user_id'], org_id))
            
        return jsonify({'message': 'Left organization successfully'})
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to leave organization'}), 500

def add_member():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
        
    org_id = data.get('organization_id')
    username = data.get('username')
    role = data.get('role', 'member')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    if not org_id:
        return jsonify({'error': 'Organization ID is missing'}), 400
        
    if role not in ['admin', 'member']:
        return jsonify({'error': 'Invalid role'}), 400
        
    try:
        # Check if user is admin
        is_admin = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ? AND role = 'admin'
        ''', (session['user_id'], org_id))
        
        if not is_admin:
            return jsonify({'error': 'Only admins can add members'}), 403
            
        # Check if user exists
        user = execute_single_query('SELECT id FROM users WHERE username = ?', (username,))
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Check if user is already a member
        existing = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ?
        ''', (user['id'], org_id))
        
        if existing:
            return jsonify({'error': 'User is already a member'}), 400
            
        # Add user to organization
        execute_write_query('''
            INSERT INTO user_organizations (user_id, organization_id, role)
            VALUES (?, ?, ?)
        ''', (user['id'], org_id, role))
        
        return jsonify({'message': 'Member added successfully'})
        
    except DatabaseError as e:
        return jsonify({'error': 'Failed to add member'}), 500

def remove_member():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    org_id = request.form.get('organization_id')
    member_id = request.form.get('member_id')
    
    if not org_id or not member_id:
        return jsonify({'error': 'Organization ID and member ID are required'}), 400
        
    try:
        # Check if user is admin
        is_admin = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ? AND role = 'admin'
        ''', (session['user_id'], org_id))
        
        if not is_admin:
            return jsonify({'error': 'Only admins can remove members'}), 403
            
        # Check if member exists in organization
        member = execute_single_query('''
            SELECT role FROM user_organizations 
            WHERE user_id = ? AND organization_id = ?
        ''', (member_id, org_id))
        
        if not member:
            return jsonify({'error': 'Member not found in organization'}), 404
            
        # Check if trying to remove the last admin
        if member['role'] == 'admin':
            admin_count = execute_single_query('''
                SELECT COUNT(*) as count 
                FROM user_organizations 
                WHERE organization_id = ? AND role = 'admin'
            ''', (org_id,))['count']
            
            if admin_count <= 1:
                return jsonify({'error': 'Cannot remove the last admin'}), 400
        
        # Remove member
        execute_write_query('''
            DELETE FROM user_organizations 
            WHERE user_id = ? AND organization_id = ?
        ''', (member_id, org_id))
        
        return jsonify({'message': 'Member removed successfully'})
        
    except DatabaseError as e:
        return jsonify({'error': 'Failed to remove member'}), 500

def get_organization_info(org_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    try:
        # Check if user is member of organization
        member = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ?
        ''', (session['user_id'], org_id))
        
        if not member:
            return jsonify({'error': 'Not a member of this organization'}), 403
            
        # Get organization info
        org_info = execute_single_query('''
            SELECT o.*, 
                   (SELECT COUNT(*) FROM user_organizations WHERE organization_id = o.id) as member_count,
                   (SELECT COUNT(*) FROM announcements WHERE organization_id = o.id) as announcement_count
            FROM organizations o
            WHERE o.id = ?
        ''', (org_id,))
        
        # Get members info
        members = execute_query('''
            SELECT u.id, u.username, uo.role
            FROM users u
            JOIN user_organizations uo ON u.id = uo.user_id
            WHERE uo.organization_id = ?
            ORDER BY u.username
        ''', (org_id,))
        
        return jsonify({
            'organization': dict(org_info),
            'members': [dict(m) for m in members]
        })
        
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to get organization info'}), 500

def groups():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
        
    try:
        # Get user's organizations
        organizations = execute_query('''
            SELECT o.*, uo.role,
                   (SELECT COUNT(*) FROM user_organizations WHERE organization_id = o.id) as member_count
            FROM organizations o
            JOIN user_organizations uo ON o.id = uo.organization_id
            WHERE uo.user_id = ?
            ORDER BY o.name
        ''', (session['user_id'],))

        # For each organization, get its members
        orgs_with_members = []
        for org in organizations:
            members = execute_query('''
                SELECT u.id, u.username, uo.role
                FROM users u
                JOIN user_organizations uo ON u.id = uo.user_id
                WHERE uo.organization_id = ?
                ORDER BY u.username
            ''', (org['id'],))
            
            org_dict = dict(org)
            org_dict['members'] = [dict(m) for m in members]
            orgs_with_members.append(org_dict)
        
        return render_template('groups.html',
                           organizations=orgs_with_members,
                           title='Group Management')
                           
    except DatabaseError as e:
        flash('Error loading groups')
        print(f"Database error: {str(e)}")
        return redirect(url_for('dashboard'))
