from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os
import pytz
from datetime import datetime

# Import modules
from auth import login_credentials, sign_up, logout
from organizations import create_organization, delete_organization, leave_organization, add_member, remove_member, get_organization_info, groups
from inventory import inventory, add_inventory_item, delete_inventory_item, allowed_file
from bulletin import bulletin, handle_announcements
from dashboard import dashboard, account_manager, update_profile
from app.routes.workpad import bp as workpad_bp

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# File upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'csv'}

# Register blueprints
app.register_blueprint(workpad_bp)

# CSRF protection
csrf = CSRFProtect(app)

# Add CSRF token to response headers
@app.after_request
def add_csrf_header(response):
    response.headers['X-CSRFToken'] = generate_csrf()
    return response

# Make user data available to all templates
@app.context_processor
def inject_user():
    if 'user_id' in session:
        return {
            'username': session.get('username'),
            'user_id': session.get('user_id')
        }
    return {'username': None, 'user_id': None}

@app.route('/static/<path:filename>')
def serve_static(filename):
    response = send_from_directory('static', filename)
    # Set cache control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Check if a user is an admin of an organization
def check_admin_status(conn, user_id, org_id):
    admin_check = conn.execute('''
        SELECT 1 FROM user_organizations 
        WHERE user_id = ? AND organization_id = ? AND role = 'admin'
    ''', (user_id, org_id)).fetchone()
    return bool(admin_check)

# Route definitions
@app.route("/", methods=['GET', 'POST'])
def index():
    return login_credentials()

@app.route("/sign_up", methods=['GET', 'POST'])
def signup_route():
    return sign_up()

@app.route("/logout", methods=['GET', 'POST'])
def logout_route():
    return logout()

@app.route("/dashboard")
def dashboard_route():
    return dashboard()

@app.route("/account_manager", methods=['GET', 'POST'])
def account_manager_route():
    return account_manager()

@app.route("/update_profile", methods=['POST'])
def update_profile_route():
    return update_profile()

@app.route("/create_organization", methods=['POST'])
def create_organization_route():
    return create_organization()

@app.route("/delete_organization", methods=['POST'])
def delete_organization_route():
    return delete_organization()

@app.route("/leave_organization", methods=['POST'])
def leave_organization_route():
    return leave_organization()

@app.route("/add_member", methods=['POST'])
def add_member_route():
    return add_member()

@app.route("/remove_member", methods=['POST'])
def remove_member_route():
    return remove_member()

@app.route("/groups")
def groups_route():
    return groups()

@app.route("/user_organizations/<int:org_id>/info")
def get_organization_info_route(org_id):
    return get_organization_info(org_id)

@app.route("/inventory")
def inventory_route():
    return inventory()

@app.route('/add_inventory_item', methods=['POST'])
@csrf.exempt
def add_inventory_item_route():
    return add_inventory_item()

@app.route('/delete_inventory_item/<int:item_id>', methods=['POST'])
def delete_inventory_item_route(item_id):
    return delete_inventory_item(item_id)

@app.route("/bulletin")
def bulletin_route():
    return bulletin()

@app.route("/announcements", methods=['POST', 'DELETE'])
def handle_announcements_route():
    return handle_announcements()

@app.route('/test_css')
def test_css():
    with open('static/styles.css', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}

@app.route("/workpad")
def workpad():
    if 'user_id' not in session:
        return redirect(url_for('login_credentials'))
    return render_template('workpad.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)