"""
Core routes and utility functions for Flex-Work
"""
from flask import render_template
from .. import app, csrf
from ..utils.db_utils import get_db

def check_admin_status(conn, user_id, org_id):
    """Check if a user is an admin of an organization"""
    cursor = conn.cursor()
    cursor.execute(
        'SELECT role FROM user_organizations WHERE user_id = ? AND organization_id = ?',
        (user_id, org_id)
    )
    result = cursor.fetchone()
    return result and result['role'] == 'admin'

@app.route('/test_css')
def test_css():
    """Route for testing CSS - returns the raw CSS file content"""
    with open('static/styles.css', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}
