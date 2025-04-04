"""
Database initialization script for Flex-Work
"""
import sqlite3
import os

def create_database():
    # Ensure the database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Connect to database (will create if not exists)
    conn = sqlite3.connect('database/database.db')
    
    try:
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create users table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')
        
        # Create organizations table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create user_organizations table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS user_organizations (
            user_id INTEGER,
            organization_id INTEGER,
            role TEXT DEFAULT 'member',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, organization_id)
        )
        ''')
        
        # Create inventory table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_path TEXT,
            url TEXT,
            description TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create announcements table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER,
            author_id INTEGER,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
        print("Database created successfully")
        
    except sqlite3.Error as e:
        print(f"Error creating database: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()