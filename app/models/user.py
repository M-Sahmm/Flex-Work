from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_id(user_id):
    """Get a user by ID"""
    try:
        return execute_single_query(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def get_user_by_username(username):
    """Get a user by username"""
    try:
        return execute_single_query(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def create_user(username, password, email=None):
    """Create a new user"""
    try:
        hashed_password = generate_password_hash(password)
        return execute_write_query(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, hashed_password, email)
        )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def update_user(user_id, data):
    """Update user data"""
    try:
        fields = []
        values = []
        
        for key, value in data.items():
            if key == 'password':
                value = generate_password_hash(value)
            fields.append(f"{key} = ?")
            values.append(value)
            
        values.append(user_id)
        
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        execute_write_query(query, tuple(values))
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def delete_user(user_id):
    """Delete a user"""
    try:
        execute_write_query(
            'DELETE FROM users WHERE id = ?',
            (user_id,)
        )
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def verify_password(user, password):
    """Verify a user's password"""
    if not user:
        return False
    return check_password_hash(user['password'], password)