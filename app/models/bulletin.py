from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError

def get_user_announcements(user_id):
    """Get all announcements for organizations a user belongs to"""
    try:
        return execute_query('''
            SELECT a.*, o.name as organization_name, u.username as author_name,
                   datetime(a.created_at) as formatted_date
            FROM announcements a
            JOIN organizations o ON a.organization_id = o.id
            JOIN users u ON a.author_id = u.id
            JOIN user_organizations uo ON a.organization_id = uo.organization_id
            WHERE uo.user_id = ?
            ORDER BY a.created_at DESC
        ''', (user_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return []

def get_organization_announcements(org_id):
    """Get all announcements for an organization"""
    try:
        return execute_query('''
            SELECT a.*, u.username as author_name,
                   datetime(a.created_at) as formatted_date
            FROM announcements a
            JOIN users u ON a.author_id = u.id
            WHERE a.organization_id = ?
            ORDER BY a.created_at DESC
        ''', (org_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return []

def get_announcement(announcement_id):
    """Get an announcement by ID"""
    try:
        return execute_single_query('''
            SELECT a.*, o.name as organization_name, u.username as author_name,
                   datetime(a.created_at) as formatted_date
            FROM announcements a
            JOIN organizations o ON a.organization_id = o.id
            JOIN users u ON a.author_id = u.id
            WHERE a.id = ?
        ''', (announcement_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def create_announcement(org_id, author_id, title, content):
    """Create a new announcement"""
    try:
        return execute_write_query('''
            INSERT INTO announcements (organization_id, author_id, title, content)
            VALUES (?, ?, ?, ?)
        ''', (org_id, author_id, title, content))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def delete_announcement(announcement_id):
    """Delete an announcement"""
    try:
        execute_write_query(
            'DELETE FROM announcements WHERE id = ?',
            (announcement_id,)
        )
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False