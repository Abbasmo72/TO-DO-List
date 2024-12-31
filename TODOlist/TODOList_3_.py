import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime

# Constants for language options
LANGUAGES = {
    "English": {
        "title": "To-Do Application",
        "add_task": "Add Task",
        "view_tasks": "View Tasks",
        "search_tasks": "Search Tasks",
        "backup": "Backup",
        "exit": "Exit",
        "name": "Name",
        "description": "Description",
        "deadline": "Deadline (YYYY-MM-DD)",
        "priority": "Priority (1-5)",
        "category": "Category",
        "add": "Add",
        "task_list": "Task List",
        "status": "Status",
        "completed": "Completed",
        "pending": "Pending",
        "search": "Search",
        "sort_by": "Sort By",
        "priority_sort": "Priority",
        "deadline_sort": "Deadline",
        "change_status": "Change Status",
        "filter": "Filter",
        "all_tasks": "All Tasks",
        "by_category": "By Category",
        "generate_report": "Generate Report",
        "error": "Error",
        "invalid_date": "Invalid date format or past date!",
        "invalid_priority": "Priority must be between 1 and 5!"
    },
    "Persian": {
        "title": "برنامه انجام وظایف",
        "add_task": "افزودن وظیفه",
        "view_tasks": "مشاهده وظایف",
        "search_tasks": "جستجوی وظایف",
        "backup": "پشتیبان‌گیری",
        "exit": "خروج",
        "name": "نام",
        "description": "توضیحات",
        "deadline": "مهلت (YYYY-MM-DD)",
        "priority": "اولویت (1-5)",
        "category": "دسته‌بندی",
        "add": "افزودن",
        "task_list": "لیست وظایف",
        "status": "وضعیت",
        "completed": "انجام‌شده",
        "pending": "در حال انجام",
        "search": "جستجو",
        "sort_by": "مرتب‌سازی بر اساس",
        "priority_sort": "اولویت",
        "deadline_sort": "مهلت",
        "change_status": "تغییر وضعیت",
        "filter": "فیلتر",
        "all_tasks": "تمام وظایف",
        "by_category": "بر اساس دسته‌بندی",
        "generate_report": "تولید گزارش",
        "error": "خطا",
        "invalid_date": "فرمت تاریخ نامعتبر است یا تاریخ گذشته!",
        "invalid_priority": "اولویت باید بین 1 تا 5 باشد!"
    }
}

class ToDoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.language = "English"
        self.tasks = []
        self.load_tasks()
        self.setup_language_selection()

    def setup_language_selection(self):
        self.root.title("Select Language / انتخاب زبان")
        label = tk.Label(self.root, text="Choose Language / زبان را انتخاب کنید:")
        label.pack(pady=10)

        for lang in LANGUAGES.keys():
            button = tk.Button(self.root, text=lang, command=lambda l=lang: self.set_language(l))
            button.pack(pady=5)

        self.root.mainloop()

    def set_language(self, language):
        self.language = language
        self.root.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        self.root = tk.Tk()
        self.root.title(LANGUAGES[self.language]["title"])

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        task_menu = tk.Menu(menubar, tearoff=0)
        task_menu.add_command(label=LANGUAGES[self.language]["add_task"], command=self.add_task)
        task_menu.add_command(label=LANGUAGES[self.language]["view_tasks"], command=self.view_tasks)
        task_menu.add_command(label=LANGUAGES[self.language]["search_tasks"], command=self.search_tasks)
        menubar.add_cascade(label=LANGUAGES[self.language]["task_list"], menu=task_menu)

        backup_menu = tk.Menu(menubar, tearoff=0)
        backup_menu.add_command(label=LANGUAGES[self.language]["backup"], command=self.backup_tasks)
        menubar.add_cascade(label=LANGUAGES[self.language]["backup"], menu=backup_menu)

        menubar.add_command(label=LANGUAGES[self.language]["exit"], command=self.root.quit)

        self.root.mainloop()

    def add_task(self):
        add_window = tk.Toplevel(self.root)
        add_window.title(LANGUAGES[self.language]["add_task"])

        tk.Label(add_window, text=LANGUAGES[self.language]["name"]).grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text=LANGUAGES[self.language]["description"]).grid(row=1, column=0)
        desc_entry = tk.Entry(add_window)
        desc_entry.grid(row=1, column=1)

        tk.Label(add_window, text=LANGUAGES[self.language]["deadline"]).grid(row=2, column=0)
        deadline_entry = tk.Entry(add_window)
        deadline_entry.grid(row=2, column=1)

        tk.Label(add_window, text=LANGUAGES[self.language]["priority"]).grid(row=3, column=0)
        priority_entry = tk.Entry(add_window)
        priority_entry.grid(row=3, column=1)

        tk.Label(add_window, text=LANGUAGES[self.language]["category"]).grid(row=4, column=0)
        category_entry = tk.Entry(add_window)
        category_entry.grid(row=4, column=1)

        def save_task():
            name = name_entry.get()
            desc = desc_entry.get()
            deadline = deadline_entry.get()
            priority = priority_entry.get()
            category = category_entry.get()

            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                if datetime.strptime(deadline, "%Y-%m-%d") < datetime.now():
                    raise ValueError
            except ValueError:
                messagebox.showerror(LANGUAGES[self.language]["error"], LANGUAGES[self.language]["invalid_date"])
                return

            if not priority.isdigit() or not (1 <= int(priority) <= 5):
                messagebox.showerror(LANGUAGES[self.language]["error"], LANGUAGES[self.language]["invalid_priority"])
                return

            self.tasks.append({
                "name": name,
                "description": desc,
                "deadline": deadline,
                "priority": int(priority),
                "category": category,
                "status": LANGUAGES[self.language]["pending"]
            })
            self.save_tasks()
            add_window.destroy()

        tk.Button(add_window, text=LANGUAGES[self.language]["add"], command=save_task).grid(row=5, column=1)

    def view_tasks(self):
        view_window = tk.Toplevel(self.root)
        view_window.title(LANGUAGES[self.language]["task_list"])

        tree = ttk.Treeview(view_window, columns=("Name", "Description", "Deadline", "Priority", "Category", "Status"), show="headings")
        tree.heading("Name", text=LANGUAGES[self.language]["name"])
        tree.heading("Description", text=LANGUAGES[self.language]["description"])
        tree.heading("Deadline", text=LANGUAGES[self.language]["deadline"])
        tree.heading("Priority", text=LANGUAGES[self.language]["priority"])
        tree.heading("Category", text=LANGUAGES[self.language]["category"])
        tree.heading("Status", text=LANGUAGES[self.language]["status"])

        for task in self.tasks:
            tree.insert("", "end", values=(task["name"], task["description"], task["deadline"], task["priority"], task["category"], task["status"]))

        tree.pack()

        def change_status():
            selected_item = tree.selection()
            if selected_item:
                task_index = tree.index(selected_item[0])
                self.tasks[task_index]["status"] = LANGUAGES[self.language]["completed"]
                self.save_tasks()
                view_window.destroy()
                self.view_tasks()

        tk.Button(view_window, text=LANGUAGES[self.language]["change_status"], command=change_status).pack()

    def search_tasks(self):
        search_window = tk.Toplevel(self.root)
        search_window.title(LANGUAGES[self.language]["search_tasks"])

        tk.Label(search_window, text=LANGUAGES[self.language]["name"]).grid(row=0, column=0)
        name_entry = tk.Entry(search_window)
        name_entry.grid(row=0, column=1)

        tk.Label(search_window, text=LANGUAGES[self.language]["category"]).grid(row=1, column=0)
        category_entry = tk.Entry(search_window)
        category_entry.grid(row=1, column=1)

        def perform_search():
            name = name_entry.get().lower()
            category = category_entry.get().lower()
            results = [task for task in self.tasks if name in task["name"].lower() or category in task["category"].lower()]

            result_window = tk.Toplevel(search_window)
            result_window.title(LANGUAGES[self.language]["search_results"])

            tree = ttk.Treeview(result_window, columns=("Name", "Description", "Deadline", "Priority", "Category", "Status"), show="headings")
            tree.heading("Name", text=LANGUAGES[self.language]["name"])
            tree.heading("Description", text=LANGUAGES[self.language]["description"])
            tree.heading("Deadline", text=LANGUAGES[self.language]["deadline"])
            tree.heading("Priority", text=LANGUAGES[self.language]["priority"])
            tree.heading("Category", text=LANGUAGES[self.language]["category"])
            tree.heading("Status", text=LANGUAGES[self.language]["status"])

            for task in results:
                tree.insert("", "end", values=(task["name"], task["description"], task["deadline"], task["priority"], task["category"], task["status"]))

            tree.pack()

        tk.Button(search_window, text=LANGUAGES[self.language]["search"], command=perform_search).grid(row=2, column=1)

    def backup_tasks(self):
        with open("tasks_backup.json", "w") as file:
            json.dump(self.tasks, file)
        messagebox.showinfo(LANGUAGES[self.language]["backup"], "Backup created successfully!")

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

if __name__ == "__main__":
    app = ToDoApp()
