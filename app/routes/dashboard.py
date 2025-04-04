from datetime import datetime
from flask import session, render_template, redirect, url_for, flash, request, jsonify
from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError
from flask_wtf.csrf import generate_csrf
from app.models.task import get_user_tasks

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
    
    user_id = session['user_id']
    try:
        # Get groups count (organizations the user is a member of)
        groups_result = execute_single_query('''
            SELECT COUNT(*) as count
            FROM organizations o
            JOIN user_organizations uo ON o.id = uo.organization_id
            WHERE uo.user_id = ?
        ''', (user_id,))
        
        groups_count = groups_result['count'] if groups_result else 0
        
        # Get inventory count
        inventory_count = execute_single_query(
            'SELECT COUNT(*) as count FROM inventory WHERE user_id = ?',
            (user_id,)
        )['count']
        
        # Get tasks count from workpad
        tasks_data = get_user_tasks(user_id)
        tasks_count = tasks_data['metadata']['todo'] + tasks_data['metadata']['in_progress']
        
        # Get announcements count for user's organizations
        announcements_count = execute_single_query('''
            SELECT COUNT(DISTINCT a.id) as count 
            FROM announcements a
            JOIN organizations o ON a.organization_id = o.id
            JOIN user_organizations uo ON o.id = uo.organization_id
            WHERE uo.user_id = ?
        ''', (user_id,))['count']
        
        # Get current date in a nice format
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Create template data
        template_data = {
            'groups_count': groups_count,
            'inventory_count': inventory_count,
            'tasks_count': tasks_count,
            'announcements_count': announcements_count,
            'current_date': current_date,
            'username': session.get('username', 'User'),
            'csrf': generate_csrf()
        }
        
        return render_template('dashboard.html', **template_data)
                           
    except DatabaseError as e:
        print(f"Database error: {str(e)}")  # Debug
        flash('Error loading dashboard data')
        return render_template('dashboard.html',
                           groups_count=0,
                           inventory_count=0,
                           tasks_count=0,
                           announcements_count=0,
                           current_date=datetime.now().strftime('%B %d, %Y'),
                           username=session.get('username', 'User'),
                           csrf=generate_csrf())

def account_manager():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
    
    try:
        # Get user information
        user = execute_single_query(
            'SELECT * FROM users WHERE id = ?',
            (session['user_id'],)
        )
        
        # Get user's organizations
        organizations = execute_query('''
            SELECT o.*, uo.role 
            FROM organizations o 
            JOIN user_organizations uo ON o.id = uo.organization_id 
            WHERE uo.user_id = ?
        ''', (session['user_id'],))
        
        return render_template('account_manager.html',
                           user=user,
                           username=session.get('username', 'User'),
                           organizations=organizations,
                           csrf=generate_csrf())
                           
    except DatabaseError as e:
        flash('Error loading account data')
        return redirect(url_for('dashboard'))

def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    email = request.form.get('email')
    
    try:
        execute_write_query(
            'UPDATE users SET email = ? WHERE id = ?',
            (email, session['user_id'])
        )
        return jsonify({'message': 'Profile updated successfully'})
    except DatabaseError as e:
        return jsonify({'error': 'Failed to update profile'}), 500

def workpad():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
    return render_template('workpad.html', username=session.get('username', 'User'), csrf=generate_csrf())