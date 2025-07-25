import sqlite3
from .models import Task
def get_connection():
    conn = sqlite3.connect("../data/tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.exceute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                priority TEXT CHECK(priority IN ('low', 'med', 'high')) NOT NULL,
                due_date TEXT,
                status TEXT CHECK(status IN ('Pending', 'Done')) NOT NULL DEFAULT 'Pending',
                archived INTEGER CHECK (archived IN (0, 1)) NOT NULL DEFAULT 0
            );
        ''')
        conn.commit()

def add_task(description: str, priority:str, due_date: str = None):
    with get_connection as conn:
        conn.execute('''
            INSERT INTO tasks (description, due_date, priority)
            VALUES (?, ?, ?);
        ''', (description, due_date, priority))
        conn.commit()
        
def get_tasks(archived: bool = False):
    with get_connection() as conn:
        rows = conn.execute('''
            SELECT * FROM tasks '' if archived else 'WHERE archived = 0' ORDER BY id; 
                            ''').fetchall()
        return [Task(**row) for row in rows]
    
def mark_done(id:int, status: str):
    with get_connection() as conn:
        conn.execute('''UPDATE tasks SET status = (status) WHERE (id);''', (status, id))
        conn.commit()

def archive_task(id: int):
    with get_connection() as conn:
        conn.execute('''UPDATE tasks SET archived = 1 WHERE (id);''', (id))
        conn.commit()

def archive_old_tasks():
    with get_connection() as conn:
        conn.execute('''UPDATE tasks SET archived = 1 WHERE due_date IS NOT NULL
                     AND DATE(due_date) < DATE('now', '-30 days');''')
        conn.commit()

def delete_task(id: int):
    with get_connection() as conn:
        conn.execute('''DELETE FROM tasks WHERE id = ?;''', (id,))
        conn.commit()

def change_priority(id: int, priority: str):
    with get_connection() as conn:
        conn.execute('''UPDATE tasks SET priority = ? WHERE id = ?;''', (priority, id))
        conn.commit()

def filter_tasks(status: str = None, priority:str = None):
    # Here, on the frontend, we take in the status and priority individually and call the function as needed by calling with keyword arguments.
    query = 'SELECT * FROM tasks WHERE archived = 0'
    params = []

    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if priority:
        query += ' AND priority = ?'
        params.append(priority)

    query += ' ORDER BY id;'

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [Task(**row) for row in rows]
