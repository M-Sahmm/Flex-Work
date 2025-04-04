from flask import session, render_template, redirect, url_for, flash, request, jsonify
from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError

def bulletin():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
        
    try:
        # Get all announcements from organizations the user is a member of
        announcements = execute_query('''
            SELECT a.*, o.name as organization_name, u.username as author_name,
                   datetime(a.created_at) as formatted_date
            FROM announcements a
            JOIN organizations o ON a.organization_id = o.id
            JOIN users u ON a.author_id = u.id
            JOIN user_organizations uo ON a.organization_id = uo.organization_id
            WHERE uo.user_id = ?
            ORDER BY a.created_at DESC
        ''', (session['user_id'],))
        
        # Get organizations where user is admin
        admin_orgs = execute_query('''
            SELECT o.* 
            FROM organizations o
            JOIN user_organizations uo ON o.id = uo.organization_id
            WHERE uo.user_id = ? AND uo.role = 'admin'
        ''', (session['user_id'],))
        
        return render_template('bulletin.html',
                           announcements=announcements,
                           admin_organizations=admin_orgs,
                           username=session.get('username', 'User'))
                           
    except DatabaseError as e:
        flash('Error loading bulletin board')
        print(f"Database error: {str(e)}")
        return redirect(url_for('dashboard'))

def handle_announcements():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    if request.method == 'POST':
        data = request.get_json()
        org_id = data['organization_id']
        title = data['title']
        content = data['content']
        
        if not all([org_id, title, content]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        try:
            # Check if user is admin
            is_admin = execute_single_query('''
                SELECT 1 FROM user_organizations 
                WHERE user_id = ? AND organization_id = ? AND role = 'admin'
            ''', (session['user_id'], org_id))
            
            if not is_admin:
                return jsonify({'error': 'Only admins can post announcements'}), 403
                
            # Create announcement
            announcement_id = execute_write_query('''
                INSERT INTO announcements (organization_id, author_id, title, content)
                VALUES (?, ?, ?, ?)
            ''', (org_id, session['user_id'], title, content))
            
            # Get the created announcement
            announcement = execute_single_query('''
                SELECT a.*, o.name as organization_name, u.username as author_name,
                       datetime(a.created_at) as formatted_date
                FROM announcements a
                JOIN organizations o ON a.organization_id = o.id
                JOIN users u ON a.author_id = u.id
                WHERE a.id = ?
            ''', (announcement_id,))
            
            return jsonify({
                'message': 'Announcement created successfully',
                'announcement': dict(announcement)
            })
            
        except DatabaseError as e:
            print(f"Database error: {str(e)}")
            return jsonify({'error': 'Failed to create announcement'}), 500
            
    elif request.method == 'DELETE':
        announcement_id = request.form.get('announcement_id')
        if not announcement_id:
            return jsonify({'error': 'Announcement ID is required'}), 400
            
        try:
            # Check if user is admin of the organization
            announcement = execute_single_query('''
                SELECT organization_id 
                FROM announcements 
                WHERE id = ?
            ''', (announcement_id,))
            
            if not announcement:
                return jsonify({'error': 'Announcement not found'}), 404
                
            is_admin = execute_single_query('''
                SELECT 1 FROM user_organizations 
                WHERE user_id = ? AND organization_id = ? AND role = 'admin'
            ''', (session['user_id'], announcement['organization_id']))
            
            if not is_admin:
                return jsonify({'error': 'Only admins can delete announcements'}), 403
                
            # Delete announcement
            execute_write_query(
                'DELETE FROM announcements WHERE id = ?',
                (announcement_id,)
            )
            
            return jsonify({'message': 'Announcement deleted successfully'})
            
        except DatabaseError as e:
            print(f"Database error: {str(e)}")
            return jsonify({'error': 'Failed to delete announcement'}), 500