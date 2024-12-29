import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'Pending',
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

# Functions for database interaction
def add_task(name, description, deadline, priority, category):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (name, description, deadline, priority, category)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, deadline, priority, category))
    conn.commit()
    conn.close()

def fetch_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY priority, deadline")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

# UI Application
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # UI Elements
        self.name_label = tk.Label(root, text="Task Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.desc_label = tk.Label(root, text="Description:")
        self.desc_label.grid(row=1, column=0, padx=10, pady=5)
        self.desc_entry = tk.Entry(root, width=30)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        self.deadline_label = tk.Label(root, text="Deadline:")
        self.deadline_label.grid(row=2, column=0, padx=10, pady=5)
        self.deadline_entry = tk.Entry(root, width=30)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        self.priority_label = tk.Label(root, text="Priority (1-5):")
        self.priority_label.grid(row=3, column=0, padx=10, pady=5)
        self.priority_entry = tk.Entry(root, width=30)
        self.priority_entry.grid(row=3, column=1, padx=10, pady=5)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=4, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(root, width=30)
        self.category_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task_ui)
        self.add_button.grid(row=5, column=1, pady=10)

        self.tasks_listbox = tk.Listbox(root, width=80, height=20)
        self.tasks_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.tasks_listbox.bind("<Double-1>", self.mark_as_done)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task_ui)
        self.delete_button.grid(row=7, column=1, pady=10)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        tasks = fetch_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"[{task[5]}] {task[1]} - {task[2]} (Due: {task[3]}, Priority: {task[4]}, Category: {task[6]})")

    def add_task_ui(self):
        name = self.name_entry.get()
        description = self.desc_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()

        if not name or not priority.isdigit():
            messagebox.showwarning("Input Error", "Task Name and Priority (1-5) are required!")
            return

        add_task(name, description, deadline, int(priority), category)
        self.refresh_tasks()
        self.clear_inputs()

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def delete_task_ui(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        task_id = fetch_tasks()[selected[0]][0]
        delete_task(task_id)
        self.refresh_tasks()

    def mark_as_done(self, event):
        selected = self.tasks_listbox.curselection()
        if not selected:
            return

        task_id = fetch_tasks()[selected[0]][0]
        update_task_status(task_id, "Done")
        self.refresh_tasks()

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
