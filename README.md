# Work Tracker Dashboard

A task-management dashboard built with Python, Streamlit, Pandas, Plotly, and MySQL.

## Features

- View task totals and counts by status (Completed, Pending, Overdue)
- Visualize task status distribution with a pie chart
- View tasks assigned per employee with a bar chart
- Add new tasks
- Update task status, priority, and due date
- Delete tasks with a confirmation step
- Search tasks by task name or employee name
- Filter tasks by status and priority

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly Express
- MySQL
- mysql-connector-python

## Project Files

- `app.py` — Streamlit dashboard and task-management interface
- `db_connection.py` — MySQL connection helper
- `test_connection.py` — optional database connection test
- `.streamlit/secrets.toml` — local database credentials (keep private)

## Requirements

- Python installed
- MySQL Server running
- Database named `work_tracker_db`
- Table named `tasks` with these columns:
  - `task_id`
  - `employee_name`
  - `task_name`
  - `status`
  - `priority`
  - `due_date`
  - `created_at` (optional for the dashboard queries)

## Setup on Windows

1. Open the project folder in VS Code.
2. Create a virtual environment if one does not already exist:

   ```powershell
   python -m venv .venv
   ```

3. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install packages:

   ```powershell
   python -m pip install streamlit pandas plotly mysql-connector-python
   ```

5. Create `.streamlit\secrets.toml` with your local MySQL credentials:

   ```toml
   [mysql]
   password = "YOUR_MYSQL_PASSWORD"
   ```

   The `db_connection.py` helper expects the MySQL user to be `root`, host to be `localhost`, and database to be `work_tracker_db`. If your settings differ, update `db_connection.py` accordingly.

6. Start the dashboard:

   ```powershell
   python -m streamlit run app.py
   ```

7. Optional: test the database connection separately:

   ```powershell
   python -m streamlit run test_connection.py
   ```

## Security

- Do not commit `.streamlit/secrets.toml` or any real database password to GitHub.
- Keep `.venv/` and `__pycache__/` out of version control.
- If a database password was exposed in a screenshot or shared file, change it in MySQL and update your local `secrets.toml`.

## Manual Test Checklist

- [ ] Dashboard starts without Python errors.
- [ ] MySQL connection works.
- [ ] Task table loads records.
- [ ] KPI counts match the database.
- [ ] Add a test task and confirm it appears.
- [ ] Update the test task and confirm the change is saved.
- [ ] Delete only a test task and confirm it disappears.
- [ ] Search by task name and employee name.
- [ ] Filter by status and priority.
- [ ] Confirm the `.streamlit/secrets.toml` file is not shared or committed.

## Notes

This README describes the current local Streamlit/MySQL project. Features should be marked complete only after each one has been tested in the running application.
