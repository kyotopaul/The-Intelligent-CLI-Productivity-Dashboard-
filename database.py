# database.py
import sqlite3
import json
from pathlib import Path
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.db_path = Path.home() / ".productivity_dashboard" / "tasks.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_task(self, description, priority="Medium"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (description, priority) VALUES (?, ?)",
            (description, priority)
        )
        
        conn.commit()
        conn.close()
    
    def get_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks ORDER BY priority DESC, created_at DESC")
        tasks = []
        
        for row in cursor.fetchall():
            tasks.append({
                "id": row[0],
                "description": row[1],
                "priority": row[2],
                "completed": bool(row[3]),
                "created_at": row[4],
                "completed_at": row[5]
            })
        
        conn.close()
        return tasks
    
    def complete_task(self, task_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE tasks SET completed = TRUE, completed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (task_id,)
        )
        
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        
        conn.commit()
        conn.close()