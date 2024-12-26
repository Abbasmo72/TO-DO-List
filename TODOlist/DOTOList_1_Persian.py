import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import csv
import json
from datetime import datetime

# تنظیم پایگاه داده
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

def fetch_tasks(status=None, category=None):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    params = []

    if status or category:
        query += " WHERE"
        if status:
            query += " status = ?"
            params.append(status)
        if category:
            if status:
                query += " AND"
            query += " category = ?"
            params.append(category)

    query += " ORDER BY priority, deadline"
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, name, description, deadline, priority, category):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET name = ?, description = ?, deadline = ?, priority = ?, category = ?
        WHERE id = ?
    """, (name, description, deadline, priority, category, task_id))
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
        self.root.title("مدیریت وظایف")

        # تنظیمات رابط کاربری
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # عناصر رابط کاربری
        self.name_entry = ctk.CTkEntry(root, placeholder_text="نام وظیفه")
        self.name_entry.grid(row=0, column=0, padx=10, pady=5)

        self.desc_entry = ctk.CTkEntry(root, placeholder_text="توضیحات")
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)

        self.deadline_entry = ctk.CTkEntry(root, placeholder_text="مهلت انجام (YYYY-MM-DD)")
        self.deadline_entry.grid(row=1, column=0, padx=10, pady=5)

        self.priority_entry = ctk.CTkEntry(root, placeholder_text="اولویت (1-5)")
        self.priority_entry.grid(row=1, column=1, padx=10, pady=5)

        self.category_entry = ctk.CTkEntry(root, placeholder_text="دسته‌بندی")
        self.category_entry.grid(row=2, column=0, padx=10, pady=5)

        self.add_button = ctk.CTkButton(root, text="افزودن وظیفه", command=self.add_task_ui)
        self.add_button.grid(row=2, column=1, padx=10, pady=5)

        self.tasks_listbox = ctk.CTkTextbox(root, width=400, height=300)
        self.tasks_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.edit_button = ctk.CTkButton(root, text="ویرایش وظیفه", command=self.edit_task_ui)
        self.edit_button.grid(row=4, column=0, padx=10, pady=5)

        self.delete_button = ctk.CTkButton(root, text="حذف وظیفه", command=self.delete_task_ui)
        self.delete_button.grid(row=4, column=1, padx=10, pady=5)

        self.export_csv_button = ctk.CTkButton(root, text="خروجی CSV", command=self.export_to_csv)
        self.export_csv_button.grid(row=5, column=0, padx=10, pady=5)

        self.export_json_button = ctk.CTkButton(root, text="خروجی JSON", command=self.export_to_json)
        self.export_json_button.grid(row=5, column=1, padx=10, pady=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks_listbox.delete("1.0", ctk.END)
        tasks = fetch_tasks()
        for task in tasks:
            self.tasks_listbox.insert(ctk.END, f"[{task[5]}] {task[1]} - {task[3]} (اولویت: {task[4]}, دسته‌بندی: {task[6]})\n")

    def add_task_ui(self):
        name = self.name_entry.get()
        description = self.desc_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()

        if not name or not priority.isdigit() or not self.validate_date(deadline) or not (1 <= int(priority) <= 5):
            messagebox.showwarning("خطا در ورودی", "لطفاً اطلاعات معتبر وارد کنید.")
            return

        add_task(name, description, deadline, int(priority), category)
        self.refresh_tasks()
        self.clear_inputs()

    def edit_task_ui(self):
        selected = self.tasks_listbox.get("1.0", "1.0 lineend")
        if not selected:
            messagebox.showwarning("خطا در انتخاب", "لطفاً یک وظیفه انتخاب کنید.")
            return

        # ویرایش وظیفه (به صورت تستی برای این نسخه صرفاً نمایش داده می‌شود)
        messagebox.showinfo("ویرایش وظیفه", "این قابلیت در دست توسعه است.")

    def delete_task_ui(self):
        selected = self.tasks_listbox.get("1.0", "1.0 lineend")
        if not selected:
            messagebox.showwarning("خطا در انتخاب", "لطفاً یک وظیفه انتخاب کنید.")
            return

        # حذف وظیفه (به صورت تستی برای این نسخه صرفاً نمایش داده می‌شود)
        messagebox.showinfo("حذف وظیفه", "این قابلیت در دست توسعه است.")

    def export_to_csv(self):
        tasks = fetch_tasks()
        with open("tasks.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["نام", "توضیحات", "مهلت انجام", "اولویت", "وضعیت", "دسته‌بندی"])
            for task in tasks:
                writer.writerow(task[1:])
        messagebox.showinfo("خروجی CSV", "خروجی با موفقیت ذخیره شد.")

    def export_to_json(self):
        tasks = fetch_tasks()
        data = [
            {"name": task[1], "description": task[2], "deadline": task[3], "priority": task[4], "status": task[5], "category": task[6]} 
            for task in tasks
        ]
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        messagebox.showinfo("خروجی JSON", "خروجی با موفقیت ذخیره شد.")

    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def clear_inputs(self):
        self.name_entry.delete(0, ctk.END)
        self.desc_entry.delete(0, ctk.END)
        self.deadline_entry.delete(0, ctk.END)
        self.priority_entry.delete(0, ctk.END)
        self.category_entry.delete(0, ctk.END)

if __name__ == "__main__":
    setup_database()
    root = ctk.CTk()
    app = ToDoApp(root)
    root.mainloop()
