import sqlite3
from contextlib import contextmanager
from typing import Generator, Any

class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class ConnectionError(DatabaseError):
    """Exception raised for connection errors"""
    pass

class QueryError(DatabaseError):
    """Exception raised for query execution errors"""
    pass

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Database connection context manager.
    
    Usage:
        with get_db() as conn:
            conn.execute('SELECT * FROM users')
    """
    conn = None
    try:
        conn = sqlite3.connect('database/database.db')  # Updated path to match migration
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        raise ConnectionError(f"Database connection error: {str(e)}")
    finally:
        if conn:
            conn.commit()  # Commit any pending transactions
            conn.close()

def execute_query(query: str, params: tuple = None) -> Any:
    """Execute a single query and return the result"""
    with get_db() as conn:
        try:
            cursor = conn.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise QueryError(f"Query execution error: {str(e)}")

def execute_single_query(query: str, params: tuple = None) -> Any:
    """Execute a query and return a single result"""
    with get_db() as conn:
        try:
            cursor = conn.execute(query, params or ())
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise QueryError(f"Query execution error: {str(e)}")

def execute_write_query(query: str, params: tuple = None) -> int:
    """Execute a write query and return the last row id"""
    with get_db() as conn:
        try:
            cursor = conn.execute(query, params or ())
            return cursor.lastrowid
        except sqlite3.Error as e:
            raise QueryError(f"Query execution error: {str(e)}")
