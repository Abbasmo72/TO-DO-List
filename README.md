<div align="center">

# TO DO List
<img alt="Gif" src="https://i.makeagif.com/media/11-24-2013/8l7jir.gif" height="250px" width="500px">
</div>
<hr>

## TO-DO List: A Tool for Task Management and Productivity
### What is a TO-DO List?
A TO-DO List refers to a list where individuals record their tasks, duties, and goals for a specific period. This tool can be as simple as a piece of paper or as advanced as digital applications and software.
### Why Do We Need a TO-DO List?
1. <b>Time Management:</b> Having a list helps you prioritize tasks and manage your time effectively.
2. <b>Increased Productivity:</b> By writing down tasks, you can focus on completing them instead of worrying about forgetting them.
3. <b>Reduced Stress:</b> Recording tasks reduces mental pressure as you no longer need to remember everything.
4. <b>Progress and Motivation:</b> Completing tasks on the list provides a sense of achievement and satisfaction, which can be motivating.
### Key Components of a TO-DO List
1. <b>Specific Tasks:</b> Each task should be clear and actionable.
2. <b>Prioritization:</b> Place the most important tasks at the top of the list.
3. <b>Scheduling:</b> Assign a specific time frame or date to each task.
4. <b>Tracking Progress:</b> Mark or remove tasks as they are completed.
### Tips for Effective Use of a TO-DO List
1. <b>Keep it Manageable:</b> Avoid making the list too long; this can lead to confusion and reduced motivation.
2. <b>Be Flexible:</b> If tasks remain incomplete, move them to the next day.
3. <b>Daily Review:</b> Review and update your list each morning or evening.
4. <b>Focus on One Task at a Time:</b> Avoid unnecessary multitasking.
### Conclusion
A TO-DO List is a simple yet powerful tool for organizing tasks and enhancing productivity. By consistently using this tool, you can get closer to your goals, manage your time better, and reduce stress. If you’re not using a TO-DO List yet, start today!
<hr>

## Key Points to Consider When Building a To-Do List Application:
1. User Interface (UI):
   - <b>Simplicity and Clarity:</b> Ensure the interface is clean and intuitive. Buttons, forms, and lists should be clearly labeled.
   - <b>Responsive Design:</b> The app should work seamlessly across devices (mobile, tablet, desktop).
   - <b>Essential UI Features:</b>
       - Add new tasks.
       - View the task list.
       - Edit or delete tasks.
       - Sort tasks by priority or due date.
2. Data Management:
   - <b>Storage:</b>
      - Use JSON files or databases (SQLite, MySQL) for storing tasks.
      - For online apps, consider server-based data storage.
   - <b>Offline Support:</b> Allow access to tasks without an internet connection, with sync capabilities when back online.
   - <b>Backups:</b> Provide options for backing up and restoring data.
3. Core Functionalities:
   - <b>Add Task:</b> A simple form to input task name, description, due date, and priority.
   - <b>Edit Task:</b> Enable modifying task details.
   - <b>Delete Task:</b> Allow removing one or multiple tasks with user confirmation.
   - <b>Task Status:</b> Mark tasks as "completed" or "in-progress."
   - <b>Sorting:</b> Allow sorting tasks by priority, date, or status.
4. Advanced Features:
   - <b>Categories/Tags:</b> Group tasks under categories (e.g., Work, Personal, Shopping).
   - <b>Notifications:</b> Send reminders before task deadlines.
   - <b>Cloud Sync:</b> Store data in the cloud for cross-device accessibility.
   - <b>Search and Filter:</b> Enable searching and filtering tasks by status, category, or priority.
5. Security:
   - Authentication: If multi-user, ensure login with username and password.
   - Data Encryption: Encrypt sensitive data (e.g., deadlines or personal details).
   - Access Control: Ensure users can only access their own data.
6. Technology and Tools:
   - <b>Programming Language:</b>
      - For desktop: Python (Tkinter, PyQt, Kivy).
      - For web: JavaScript (React, Vue, Angular for front-end) and Python/Node.js for back-end.
      - For mobile: Flutter, React Native, or Kotlin/Swift.
   - <b>Libraries:</b> Use libraries like Todoist API or FullCalendar to speed up development.
7. Maintenance and Future Development:
   - <b>Updates:</b> Design the app for easy updates.
   - <b>User Feedback:</b> Add a section to collect user feedback.
   - <b>Testing:</b> Test the app with diverse users to identify potential issues and real needs.
8. User Experience (UX):
   - <b>Consistency:</b> Provide a consistent experience across devices (mobile and desktop).
   - <b>Interactive Elements:</b> Use animations or simple effects for better interaction.
   - <b>Performance:</b> Ensure smooth and fast operations.
     
By following these guidelines, you can build a professional and functional To-Do List application. Let me know if you'd like sample code or further details on any specific part!
<hr>

# Getting Started
In this section, we show some examples of the to do list program in different forms
<hr>

### The first program TO DO List
[To Do List English one](TODOlist/DOTOList_1_English.py)<br>
[To Do List Persian one](TODOlist/DOTOList_1_Persian.py)<br>

This Python code implements a task management application with a graphical user interface (GUI) using the customtkinter library. It provides functionality to create, view, update, delete, and export tasks. The application stores tasks in a SQLite database and offers a user-friendly interface for managing them.

### Code Analysis
1. Database Setup:
   - The setup_database() function ensures that the SQLite database (tasks.db) and the tasks table are created if they don’t already exist. The table includes fields such as id, name, description, deadline, priority, status, and category.
2. Database Management Functions:
   - add_task(): Inserts a new task into the database.
   - fetch_tasks(): Retrieves tasks from the database, optionally filtered by status and/or category. The results are ordered by priority and deadline.
   - delete_task(): Removes a task from the database based on its id.
   - update_task(): Updates a task's details.
   - update_task_status(): Modifies the status of a task.
3. User Interface:
   - Built using customtkinter, a modern alternative to the traditional tkinter library.
   - Input fields for task attributes such as name, description, deadline, priority, and category.
   - A list box for displaying tasks.
   - Buttons for adding, editing, deleting, and exporting tasks.
4. Task Export Options:
   - Tasks can be exported to CSV or JSON format using export_to_csv() and export_to_json() functions. The exported files include all task details, making it easy to share or back up the data.
5. Error Handling and Validation:
   - The validate_date() method ensures that deadlines are provided in the correct YYYY-MM-DD format.
   - Basic validation checks for empty fields and priority values between 1 and 5.
6. Modularity:
   - Database operations and UI functions are separated, improving code readability and maintainability.
<hr>

### The second program TO DO List
[To Do List English Two](TODOlist/TODOList_2_English.py)<br>
[To Do List Persian Two](TODOlist/TODOList_2_Persian.py)<br>

This code implements a To-Do List application using Tkinter for the graphical user interface (GUI) and SQLite for data storage. Here's an analysis of its components:
1. Database Setup
The setup_database function initializes an SQLite database and creates a table named tasks if it doesn't already exist. The table includes the following fields:
   - id: A unique primary key for each task.
   - name: The task's name (required).
   - description: A description of the task.
   - deadline: The due date for the task.
   - priority: The task's priority (default value is 5).
   - status: The task's current status (default is "Pending").
   - category: The category the task belongs to.
2. Database Interaction Functions
   - add_task: Adds a new task to the tasks table.
   - fetch_tasks: Retrieves all tasks from the database, ordered by priority and deadline..
   - delete_task: Deletes a specific task based on its id.
   - update_task_status: Updates the status of a specific task (e.g., marking it as "Done").<br>
These functions handle database interactions and ensure that changes are committed.
3. Graphical User Interface (ToDoApp Class)
The ToDoApp class implements the graphical interface. Key elements include:
   - Input Fields: For task name, description, deadline, priority, and category.
   - Buttons:
        - Add Task: Adds a new task with the provided information.
        - Delete Task: Deletes the selected task from the list.
   - Task List: Displays existing tasks with details.
        - Double-clicking on a task marks it as "Done."

   
