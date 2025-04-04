from flask import Flask, session, send_from_directory
from flask_wtf.csrf import CSRFProtect, generate_csrf
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create and configure the Flask application
app = Flask(__name__,
    template_folder='../templates',
    static_folder='../static'
)

# Basic configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')  # Fallback for development only
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WTF_CSRF_ENABLED'] = True  # Enable CSRF protection
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit on tokens

# File upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'csv'}

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Add datetime filter
@app.template_filter('datetime')
def format_datetime(value):
    """Format a datetime string to a readable format"""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return value

# Make CSRF token available to all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf=generate_csrf())

# Make user data available to all templates
@app.context_processor
def inject_user():
    if 'user_id' in session:
        return {
            'username': session.get('username'),
            'user_id': session.get('user_id')
        }
    return {'username': None, 'user_id': None}

# Serve static files with cache control
@app.route('/static/<path:filename>')
def serve_static(filename):
    response = send_from_directory(app.static_folder, filename)
    # Set cache control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Create required directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register routes
from app.routes.workpad import workpad, create_task, update_task_status, delete_task, get_task_stats

# Register workpad routes
app.add_url_rule('/workpad', view_func=workpad)
app.add_url_rule('/tasks', view_func=create_task, methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=update_task_status, methods=['PATCH'])
app.add_url_rule('/tasks/<task_id>', view_func=delete_task, methods=['DELETE'])
app.add_url_rule('/tasks/stats', view_func=get_task_stats)
