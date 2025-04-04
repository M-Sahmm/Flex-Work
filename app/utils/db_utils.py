import sqlite3
import os
from contextlib import contextmanager

class DatabaseError(Exception):
    """Exception raised for database errors"""
    pass

@contextmanager
def get_db():
    """Get a database connection"""
    conn = None
    try:
        # Get absolute path to database
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(current_dir, 'database', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()

def execute_query(query, params=()):
    """Execute a query and return all results"""
    try:
        with get_db() as conn:
            result = conn.execute(query, params).fetchall()
        return result
    except Exception as e:
        raise DatabaseError(f"Query error: {str(e)}")

def execute_single_query(query, params=()):
    """Execute a query and return a single result"""
    try:
        with get_db() as conn:
            result = conn.execute(query, params).fetchone()
        return result
    except Exception as e:
        raise DatabaseError(f"Query error: {str(e)}")

def execute_write_query(query, params=()):
    """Execute a write query and return the last row id"""
    try:
        with get_db() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid
    except Exception as e:
        raise DatabaseError(f"Write error: {str(e)}")