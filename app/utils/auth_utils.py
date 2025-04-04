from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from app.models.organization import is_admin

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Not logged in'}), 401
            flash('Please log in to access this page')
            return redirect(url_for('login_credentials'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Not logged in'}), 401
            flash('Please log in to access this page')
            return redirect(url_for('login_credentials'))
            
        # Check if org_id is in kwargs or request args
        org_id = kwargs.get('org_id') or request.args.get('org_id') or request.form.get('organization_id')
        
        if not org_id:
            if request.is_json:
                return jsonify({'error': 'Organization ID is required'}), 400
            flash('Organization ID is required')
            return redirect(url_for('dashboard'))
            
        # Check if user is admin
        if not is_admin(session['user_id'], org_id):
            if request.is_json:
                return jsonify({'error': 'Admin privileges required'}), 403
            flash('You do not have permission to access this page')
            return redirect(url_for('dashboard'))
            
        return f(*args, **kwargs)
    return decorated_function