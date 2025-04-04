from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError, get_db

def get_organization_by_id(org_id):
    """Get an organization by ID"""
    try:
        return execute_single_query(
            'SELECT * FROM organizations WHERE id = ?',
            (org_id,)
        )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def get_organization_by_name(name):
    """Get an organization by name"""
    try:
        return execute_single_query(
            'SELECT * FROM organizations WHERE name = ?',
            (name,)
        )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def create_organization(name, creator_id):
    """Create a new organization with the creator as admin"""
    try:
        with get_db() as conn:
            cursor = conn.execute(
                'INSERT INTO organizations (name) VALUES (?)',
                (name,)
            )
            org_id = cursor.lastrowid
            
            conn.execute('''
                INSERT INTO user_organizations (user_id, organization_id, role)
                VALUES (?, ?, ?)
            ''', (creator_id, org_id, 'admin'))
            
        return org_id
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def delete_organization(org_id):
    """Delete an organization"""
    try:
        execute_write_query(
            'DELETE FROM organizations WHERE id = ?',
            (org_id,)
        )
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def get_user_organizations(user_id):
    """Get all organizations a user belongs to"""
    try:
        return execute_query('''
            SELECT o.*, uo.role 
            FROM organizations o 
            JOIN user_organizations uo ON o.id = uo.organization_id 
            WHERE uo.user_id = ?
        ''', (user_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return []

def get_organization_members(org_id):
    """Get all members of an organization"""
    try:
        return execute_query('''
            SELECT u.id, u.username, uo.role
            FROM users u
            JOIN user_organizations uo ON u.id = uo.user_id
            WHERE uo.organization_id = ?
            ORDER BY u.username
        ''', (org_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return []

def add_organization_member(org_id, user_id, role='member'):
    """Add a member to an organization"""
    try:
        execute_write_query('''
            INSERT INTO user_organizations (user_id, organization_id, role)
            VALUES (?, ?, ?)
        ''', (user_id, org_id, role))
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def remove_organization_member(org_id, user_id):
    """Remove a member from an organization"""
    try:
        execute_write_query('''
            DELETE FROM user_organizations 
            WHERE user_id = ? AND organization_id = ?
        ''', (user_id, org_id))
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def is_admin(user_id, org_id):
    """Check if a user is an admin of an organization"""
    try:
        result = execute_single_query('''
            SELECT 1 FROM user_organizations 
            WHERE user_id = ? AND organization_id = ? AND role = 'admin'
        ''', (user_id, org_id))
        return bool(result)
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False