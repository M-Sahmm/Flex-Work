import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from database.database import execute_write_query, execute_query, execute_single_query

def init_task_table():
    """Initialize the user_tasks table if it doesn't exist"""
    query = """
    CREATE TABLE IF NOT EXISTS user_tasks (
        user_id TEXT NOT NULL,
        tasks_data JSON NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    )
    """
    execute_write_query(query)

def get_user_tasks(user_id: str) -> Dict[str, Any]:
    """Get all tasks for a user"""
    query = "SELECT tasks_data FROM user_tasks WHERE user_id = ?"
    result = execute_single_query(query, (user_id,))
    
    if result:
        return json.loads(result['tasks_data'])
    
    # Return empty task structure if no tasks exist
    return {
        "tasks": {},
        "metadata": {
            "total_tasks": 0,
            "todo": 0,
            "in_progress": 0,
            "completed": 0
        }
    }

def save_user_tasks(user_id: str, tasks_data: Dict[str, Any]) -> bool:
    """Save or update tasks data for a user"""
    query = """
    INSERT OR REPLACE INTO user_tasks (user_id, tasks_data, updated_at)
    VALUES (?, ?, CURRENT_TIMESTAMP)
    """
    try:
        execute_write_query(query, (user_id, json.dumps(tasks_data)))
        return True
    except Exception:
        return False

def add_task(user_id: str, title: str, description: str) -> Optional[str]:
    """Add a new task for a user"""
    try:
        tasks_data = get_user_tasks(user_id)
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create new task
        task = {
            "title": title,
            "description": description,
            "status": "todo",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Add task to tasks dictionary
        if "tasks" not in tasks_data:
            tasks_data["tasks"] = {}
        tasks_data["tasks"][task_id] = task
        
        # Update metadata
        if "metadata" not in tasks_data:
            tasks_data["metadata"] = {"total_tasks": 0, "todo": 0, "in_progress": 0, "completed": 0}
        tasks_data["metadata"]["total_tasks"] += 1
        tasks_data["metadata"]["todo"] += 1
        
        if save_user_tasks(user_id, tasks_data):
            return task_id
        return None
    except Exception:
        return None

def update_task_status(user_id: str, task_id: str, new_status: str) -> bool:
    """Update the status of a task"""
    tasks_data = get_user_tasks(user_id)
    
    if task_id not in tasks_data["tasks"]:
        return False
    
    task = tasks_data["tasks"][task_id]
    old_status = task["status"]
    
    # Update task
    task["status"] = new_status
    task["updated_at"] = datetime.now().isoformat()
    
    # Update metadata
    tasks_data["metadata"][old_status] -= 1
    tasks_data["metadata"][new_status] += 1
    
    return save_user_tasks(user_id, tasks_data)

def delete_task(user_id: str, task_id: str) -> bool:
    """Delete a task"""
    tasks_data = get_user_tasks(user_id)
    
    if task_id not in tasks_data["tasks"]:
        return False
    
    # Update metadata
    status = tasks_data["tasks"][task_id]["status"]
    tasks_data["metadata"][status] -= 1
    tasks_data["metadata"]["total_tasks"] -= 1
    
    # Remove task
    del tasks_data["tasks"][task_id]
    
    return save_user_tasks(user_id, tasks_data)
