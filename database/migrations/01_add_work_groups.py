"""
Migration to add work groups functionality
"""
import sqlite3
import os

def migrate():
    # Connect to database
    conn = sqlite3.connect('database/database.db')
    
    try:
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create work_groups table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS work_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_by INTEGER NOT NULL,
            organization_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
            UNIQUE(name, created_by)
        )
        ''')
        
        # Create work_group_items table (junction table)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS work_group_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_group_id INTEGER NOT NULL,
            inventory_item_id INTEGER NOT NULL,
            added_by INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (work_group_id) REFERENCES work_groups (id) ON DELETE CASCADE,
            FOREIGN KEY (inventory_item_id) REFERENCES inventory (id) ON DELETE CASCADE,
            FOREIGN KEY (added_by) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(work_group_id, inventory_item_id)
        )
        ''')
        
        conn.commit()
        print("Work groups tables created successfully")
        
    except sqlite3.Error as e:
        print(f"Error creating work groups tables: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    # Create migrations directory if it doesn't exist
    os.makedirs('database/migrations', exist_ok=True)
    migrate()
