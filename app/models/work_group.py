"""
Work Group models for managing inventory groups
"""
from typing import List, Optional, Dict, Any
from database.database import execute_query, execute_single_query, execute_write_query
from datetime import datetime

class WorkGroup:
    def __init__(self, id: int, name: str, description: Optional[str], 
                 created_by: int, organization_id: Optional[int], created_at: str):
        self.id = id
        self.name = name
        self.description = description
        self.created_by = created_by
        self.organization_id = organization_id
        self.created_at = created_at

    @staticmethod
    def create(name: str, created_by: int, description: Optional[str] = None, 
               organization_id: Optional[int] = None) -> int:
        """Create a new work group"""
        query = '''
        INSERT INTO work_groups (name, description, created_by, organization_id)
        VALUES (?, ?, ?, ?)
        '''
        return execute_write_query(query, (name, description, created_by, organization_id))

    @staticmethod
    def get_by_id(group_id: int) -> Optional[Dict[str, Any]]:
        """Get work group by ID"""
        query = 'SELECT * FROM work_groups WHERE id = ?'
        return execute_single_query(query, (group_id,))

    @staticmethod
    def get_by_user(user_id: int) -> List[Dict[str, Any]]:
        """Get all work groups created by a user"""
        query = 'SELECT * FROM work_groups WHERE created_by = ? ORDER BY created_at DESC'
        return execute_query(query, (user_id,))

    @staticmethod
    def delete(group_id: int, user_id: int) -> bool:
        """Delete a work group (only if user is the creator)"""
        query = 'DELETE FROM work_groups WHERE id = ? AND created_by = ?'
        execute_write_query(query, (group_id, user_id))
        return True

    @staticmethod
    def update(group_id: int, user_id: int, name: Optional[str] = None, 
               description: Optional[str] = None) -> bool:
        """Update work group details"""
        updates = []
        params = []
        
        if name:
            updates.append('name = ?')
            params.append(name)
        if description is not None:  # Allow empty description
            updates.append('description = ?')
            params.append(description)
            
        if not updates:
            return False
            
        query = f'''
        UPDATE work_groups 
        SET {", ".join(updates)}
        WHERE id = ? AND created_by = ?
        '''
        params.extend([group_id, user_id])
        execute_write_query(query, tuple(params))
        return True

class WorkGroupItem:
    @staticmethod
    def item_exists_in_group(group_id: int, item_id: int) -> bool:
        """Check if an item already exists in a specific work group"""
        query = '''
        SELECT COUNT(*) as count
        FROM work_group_items
        WHERE work_group_id = ? AND inventory_item_id = ?
        '''
        result = execute_single_query(query, (group_id, item_id))
        return result[0] > 0 if result else False

    @staticmethod
    def item_exists_in_any_group(item_id: int) -> bool:
        """Check if an item exists in any work group"""
        query = '''
        SELECT COUNT(*) as count
        FROM work_group_items
        WHERE inventory_item_id = ?
        '''
        result = execute_single_query(query, (item_id,))
        return result[0] > 0 if result else False

    @staticmethod
    def add_item(group_id: int, item_id: int, user_id: int) -> int:
        """Add an inventory item to a work group"""
        # Check if item exists in any group
        if WorkGroupItem.item_exists_in_any_group(item_id):
            raise ValueError("Item already exists in a work group")
            
        # Check if item exists in this specific group
        if WorkGroupItem.item_exists_in_group(group_id, item_id):
            raise ValueError("Item already exists in this group")
            
        query = '''
        INSERT INTO work_group_items (work_group_id, inventory_item_id, added_by)
        VALUES (?, ?, ?)
        '''
        return execute_write_query(query, (group_id, item_id, user_id))

    @staticmethod
    def remove_item(group_id: int, item_id: int, user_id: int) -> bool:
        """Remove an item from a work group (only if user is the group creator)"""
        query = '''
        DELETE FROM work_group_items 
        WHERE work_group_id = ? 
        AND inventory_item_id = ? 
        AND work_group_id IN (SELECT id FROM work_groups WHERE created_by = ?)
        '''
        execute_write_query(query, (group_id, item_id, user_id))
        return True

    @staticmethod
    def get_group_items(group_id: int) -> List[Dict[str, Any]]:
        """Get all items in a work group"""
        query = '''
        SELECT i.*, wgi.added_at, wgi.added_by
        FROM inventory i
        JOIN work_group_items wgi ON i.id = wgi.inventory_item_id
        WHERE wgi.work_group_id = ?
        ORDER BY wgi.added_at DESC
        '''
        return execute_query(query, (group_id,))

    @staticmethod
    def get_item_groups(item_id: int) -> List[Dict[str, Any]]:
        """Get all groups that contain a specific item"""
        query = '''
        SELECT wg.*, wgi.added_at, wgi.added_by
        FROM work_groups wg
        JOIN work_group_items wgi ON wg.id = wgi.work_group_id
        WHERE wgi.inventory_item_id = ?
        ORDER BY wgi.added_at DESC
        '''
        return execute_query(query, (item_id,))
