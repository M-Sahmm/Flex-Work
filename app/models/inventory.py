from app.utils.db_utils import execute_query, execute_single_query, execute_write_query, DatabaseError

def get_user_inventory(user_id):
    """Get all inventory items for a user"""
    try:
        return execute_query('''
            SELECT * FROM inventory 
            WHERE user_id = ?
            ORDER BY date_added DESC
        ''', (user_id,))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return []

def get_inventory_item(item_id, user_id=None):
    """Get an inventory item by ID"""
    try:
        if user_id:
            return execute_single_query(
                'SELECT * FROM inventory WHERE id = ? AND user_id = ?',
                (item_id, user_id)
            )
        else:
            return execute_single_query(
                'SELECT * FROM inventory WHERE id = ?',
                (item_id,)
            )
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def create_inventory_item(user_id, name, description=None, file_type='url', file_path=None, url=None):
    """Create a new inventory item"""
    try:
        return execute_write_query('''
            INSERT INTO inventory (user_id, name, description, file_type, file_path, url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, description, file_type, file_path, url))
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return None

def update_inventory_item(item_id, user_id, data):
    """Update an inventory item"""
    try:
        fields = []
        values = []
        
        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)
            
        values.append(item_id)
        values.append(user_id)
        
        query = f"UPDATE inventory SET {', '.join(fields)} WHERE id = ? AND user_id = ?"
        execute_write_query(query, tuple(values))
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False

def delete_inventory_item(item_id, user_id):
    """Delete an inventory item"""
    try:
        execute_write_query(
            'DELETE FROM inventory WHERE id = ? AND user_id = ?',
            (item_id, user_id)
        )
        return True
    except DatabaseError as e:
        print(f"Database error: {str(e)}")
        return False