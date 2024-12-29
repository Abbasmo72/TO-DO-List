import tkinter as tk
from tkinter import messagebox
import sqlite3

# تابع تنظیم پایگاه داده
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
            status TEXT DEFAULT 'در حال انجام',
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

# توابع مدیریت پایگاه داده
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

# کلاس مدیریت رابط کاربری
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("لیست وظایف")

        # عناصر رابط کاربری
        self.name_label = tk.Label(root, text="نام وظیفه:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.desc_label = tk.Label(root, text="توضیحات:")
        self.desc_label.grid(row=1, column=0, padx=10, pady=5)
        self.desc_entry = tk.Entry(root, width=30)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        self.deadline_label = tk.Label(root, text="مهلت انجام:")
        self.deadline_label.grid(row=2, column=0, padx=10, pady=5)
        self.deadline_entry = tk.Entry(root, width=30)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        self.priority_label = tk.Label(root, text="اولویت (1-5):")
        self.priority_label.grid(row=3, column=0, padx=10, pady=5)
        self.priority_entry = tk.Entry(root, width=30)
        self.priority_entry.grid(row=3, column=1, padx=10, pady=5)

        self.category_label = tk.Label(root, text="دسته‌بندی:")
        self.category_label.grid(row=4, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(root, width=30)
        self.category_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_button = tk.Button(root, text="افزودن وظیفه", command=self.add_task_ui)
        self.add_button.grid(row=5, column=1, pady=10)

        self.tasks_listbox = tk.Listbox(root, width=80, height=20)
        self.tasks_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.tasks_listbox.bind("<Double-1>", self.mark_as_done)

        self.delete_button = tk.Button(root, text="حذف وظیفه", command=self.delete_task_ui)
        self.delete_button.grid(row=7, column=1, pady=10)

        self.refresh_tasks()

    def refresh_tasks(self):
        # به‌روزرسانی لیست وظایف در رابط کاربری
        self.tasks_listbox.delete(0, tk.END)
        tasks = fetch_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"[{task[5]}] {task[1]} - {task[2]} (مهلت: {task[3]}, اولویت: {task[4]}, دسته‌بندی: {task[6]})")

    def add_task_ui(self):
        # افزودن وظیفه جدید
        name = self.name_entry.get()
        description = self.desc_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()

        if not name or not priority.isdigit():
            messagebox.showwarning("خطا در ورودی", "وارد کردن نام وظیفه و اولویت (1-5) الزامی است!")
            return

        add_task(name, description, deadline, int(priority), category)
        self.refresh_tasks()
        self.clear_inputs()

    def clear_inputs(self):
        # پاک کردن فیلدهای ورودی
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def delete_task_ui(self):
        # حذف وظیفه انتخاب شده
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("خطا در انتخاب", "لطفاً یک وظیفه برای حذف انتخاب کنید.")
            return

        task_id = fetch_tasks()[selected[0]][0]
        delete_task(task_id)
        self.refresh_tasks()

    def mark_as_done(self, event):
        # علامت‌گذاری وظیفه به‌عنوان "انجام شده"
        selected = self.tasks_listbox.curselection()
        if not selected:
            return

        task_id = fetch_tasks()[selected[0]][0]
        update_task_status(task_id, "انجام شده")
        self.refresh_tasks()

if __name__ == "__main__":
    # تنظیم اولیه پایگاه داده و اجرای برنامه
    setup_database()
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
