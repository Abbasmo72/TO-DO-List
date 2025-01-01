import customtkinter as ctk
import json
from datetime import datetime
from tkinter import filedialog, messagebox

# Initialize CustomTkinter
ctk.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Other options: "green", "dark-blue"

# Language Dictionary
LANGUAGES = {
    "en": {
        "title": "To-Do List Manager",
        "add_task": "Add Task",
        "search": "Search Tasks",
        "export": "Export Data",
        "task_name": "Task Name",
        "deadline": "Deadline (YYYY-MM-DD)",
        "priority": "Priority (1-5)",
        "save_task": "Save Task",
        "input_error": "Input Error",
        "all_fields_required": "All fields are required!",
        "priority_error": "Priority must be between 1 and 5",
        "export_success": "Export Successful",
        "tasks_exported": "Tasks exported to",
    },
    "fa": {
        "title": "مدیریت لیست وظایف",
        "add_task": "اضافه کردن وظیفه",
        "search": "جستجوی وظایف",
        "export": "خروجی گرفتن",
        "task_name": "نام وظیفه",
        "deadline": "مهلت (YYYY-MM-DD)",
        "priority": "اولویت (1-5)",
        "save_task": "ذخیره وظیفه",
        "input_error": "خطای ورودی",
        "all_fields_required": "تمام فیلدها باید پر شوند!",
        "priority_error": "اولویت باید بین 1 تا 5 باشد",
        "export_success": "خروجی با موفقیت انجام شد",
        "tasks_exported": "وظایف به فایل ذخیره شدند",
    }
}

class ToDoApp(ctk.CTk):
    def __init__(self, language):
        super().__init__()
        self.lang = language
        self.translations = LANGUAGES[self.lang]

        # Window Settings
        self.title(self.translations["title"])
        self.geometry("800x600")
        self.tasks = []

        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", pady=10)

        self.label = ctk.CTkLabel(self.header_frame, text=self.translations["title"], font=("Arial", 24))
        self.label.pack(pady=5)

        # Buttons
        self.add_task_button = ctk.CTkButton(self.header_frame, text=self.translations["add_task"], command=self.add_task_ui)
        self.add_task_button.pack(side="left", padx=10)

        self.search_button = ctk.CTkButton(self.header_frame, text=self.translations["search"], command=self.search_tasks)
        self.search_button.pack(side="left", padx=10)

        self.export_button = ctk.CTkButton(self.header_frame, text=self.translations["export"], command=self.export_tasks)
        self.export_button.pack(side="left", padx=10)

        # Task List
        self.task_frame = ctk.CTkScrollableFrame(self)
        self.task_frame.pack(fill="both", expand=True, pady=10)

        # Load Initial Tasks
        self.load_tasks()

    def add_task_ui(self):
        """Open a new window for adding tasks."""
        task_window = ctk.CTkToplevel(self)
        task_window.title(self.translations["add_task"])
        task_window.geometry("400x300")

        # Input Fields
        ctk.CTkLabel(task_window, text=self.translations["task_name"]).pack(pady=5)
        task_name_entry = ctk.CTkEntry(task_window)
        task_name_entry.pack()

        ctk.CTkLabel(task_window, text=self.translations["deadline"]).pack(pady=5)
        deadline_entry = ctk.CTkEntry(task_window)
        deadline_entry.pack()

        ctk.CTkLabel(task_window, text=self.translations["priority"]).pack(pady=5)
        priority_entry = ctk.CTkEntry(task_window)
        priority_entry.pack()

        def save_task():
            """Save the new task."""
            name = task_name_entry.get()
            deadline = deadline_entry.get()
            priority = priority_entry.get()

            if not name or not deadline or not priority:
                messagebox.showerror(self.translations["input_error"], self.translations["all_fields_required"])
                return

            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                if not (1 <= int(priority) <= 5):
                    raise ValueError(self.translations["priority_error"])
            except Exception as e:
                messagebox.showerror(self.translations["input_error"], str(e))
                return

            self.tasks.append({
                "name": name,
                "deadline": deadline,
                "priority": priority,
                "status": "Pending"
            })
            self.refresh_task_list()
            task_window.destroy()

        # Save Button
        ctk.CTkButton(task_window, text=self.translations["save_task"], command=save_task).pack(pady=20)

    def refresh_task_list(self):
        """Refresh the task list in the UI."""
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_text = f"{task['name']} | {self.translations['deadline']}: {task['deadline']} | {self.translations['priority']}: {task['priority']} | Status: {task['status']}"
            ctk.CTkLabel(self.task_frame, text=task_text, anchor="w").pack(fill="x", pady=2)

    def search_tasks(self):
        """Implement search functionality."""
        pass

    def export_tasks(self):
        """Export tasks to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.tasks, file, indent=4)
            messagebox.showinfo(self.translations["export_success"], f"{self.translations['tasks_exported']} {file_path}")

    def load_tasks(self):
        """Load tasks from a file."""
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                self.refresh_task_list()
        except FileNotFoundError:
            self.tasks = []

# Language Selection Window
def select_language():
    lang_window = ctk.CTk()
    lang_window.title("Select Language")
    lang_window.geometry("300x150")

    def set_language(lang):
        lang_window.destroy()
        app = ToDoApp(lang)
        app.mainloop()

    ctk.CTkLabel(lang_window, text="Choose your language / زبان خود را انتخاب کنید", font=("Arial", 14)).pack(pady=20)
    ctk.CTkButton(lang_window, text="English", command=lambda: set_language("en")).pack(pady=5)
    ctk.CTkButton(lang_window, text="فارسی", command=lambda: set_language("fa")).pack(pady=5)

    lang_window.mainloop()

if __name__ == "__main__":
    select_language()
