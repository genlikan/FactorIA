import threading
import time
from todo import get_pending_todos

def remind_pending_tasks():
    while True:
        pending_tasks = get_pending_todos()
        if pending_tasks:
            tasks = "\n".join([task[0] for task in pending_tasks])
            print(f"Reminder: You have pending tasks:\n{tasks}")
        time.sleep(600)  # Remind every 10 minutes

def start_reminder_thread():
    reminder_thread = threading.Thread(target=remind_pending_tasks)
    reminder_thread.daemon = True
    reminder_thread.start()
