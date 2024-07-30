import sqlite3

def setup_database():
    conn = sqlite3.connect('factoria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_todo_item(task):
    conn = sqlite3.connect('factorio_assistant.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todo_list (task, status) VALUES (?, ?)', (task, 'pending'))
    conn.commit()
    conn.close()

def get_todo_list():
    conn = sqlite3.connect('factorio_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, status FROM todo_list')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_todo_status(task_id, status):
    conn = sqlite3.connect('factorio_assistant.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE todo_list SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

def get_pending_todos():
    conn = sqlite3.connect('factorio_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task FROM todo_list WHERE status = ?', ('pending',))
    rows = cursor.fetchall()
    conn.close()
    return rows
