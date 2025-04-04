from flask import render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.db_utils import execute_single_query, execute_write_query, DatabaseError

def login_credentials():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = execute_single_query(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            )
            
            if not user:
                flash('Username does not exist')
                return redirect(url_for('login_credentials'))
                
            if not check_password_hash(user['password'], password):
                flash('Incorrect password')
                return redirect(url_for('login_credentials'))
                
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
            
        except DatabaseError:
            flash('An error occurred during login')
            return redirect(url_for('login_credentials'))
    
    return render_template('login.html')

def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('sign_up'))
        
        try:
            # Check if username exists
            existing_user = execute_single_query(
                'SELECT 1 FROM users WHERE username = ?',
                (username,)
            )
            
            if existing_user:
                flash('Username already exists')
                return redirect(url_for('sign_up'))
            
            # Create new user
            hashed_password = generate_password_hash(password)
            user_id = execute_write_query(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )
            
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('dashboard'))
            
        except DatabaseError as e:
            flash('An error occurred during sign up')
            print(f"Database error: {str(e)}")
            return redirect(url_for('sign_up'))
        
    return render_template("sign_up.html", title="Sign Up")

def logout():
    session.clear()
    return redirect(url_for('login_credentials'))