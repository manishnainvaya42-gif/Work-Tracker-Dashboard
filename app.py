import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_db_connection

# Page configuration
st.set_page_config(
    page_title="Work Tracker Dashboard",
    page_icon="📊",
    layout="wide",
)

# Dashboard header
st.title("📊 Work Tracker Dashboard")
st.markdown("### Manage tasks, monitor progress, and track employee performance")

# Sidebar
st.sidebar.title("⚙️ Dashboard Menu")
st.sidebar.info("Welcome to Work Tracker Dashboard!")


@st.cache_data(ttl=10)
def load_tasks():
    """Fetch task records from MySQL."""
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame(
            columns=["task_id", "Employee", "Task", "Status", "Priority", "Due Date"]
        )

    try:
        query = """
            SELECT
                task_id,
                employee_name AS Employee,
                task_name AS Task,
                status AS Status,
                priority AS Priority,
                due_date AS `Due Date`
            FROM tasks
            ORDER BY task_id
        """
        return pd.read_sql(query, connection)
    except Exception as error:
        st.error(f"Could not load tasks from MySQL: {error}")
        return pd.DataFrame(
            columns=["task_id", "Employee", "Task", "Status", "Priority", "Due Date"]
        )
    finally:
        connection.close()


# Add New Task
st.subheader("➕ Add New Task")
with st.form("add_task_form", clear_on_submit=True):
    new_employee = st.text_input("Employee Name")
    new_task = st.text_input("Task Name")
    add_col1, add_col2, add_col3 = st.columns(3)

    with add_col1:
        new_status = st.selectbox("Status", ["Pending", "Completed", "Overdue"])
    with add_col2:
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
    with add_col3:
        new_due_date = st.date_input("Due Date")

    add_submitted = st.form_submit_button("➕ Add Task")

if add_submitted:
    if not new_employee.strip() or not new_task.strip():
        st.warning("Please enter both Employee Name and Task Name.")
    else:
        connection = get_db_connection()
        if connection is not None:
            cursor = None
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO tasks
                        (employee_name, task_name, status, priority, due_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (new_employee.strip(), new_task.strip(), new_status, new_priority, new_due_date),
                )
                connection.commit()
                st.cache_data.clear()
                st.success("Task added successfully!")
                st.rerun()
            except Exception as error:
                st.error(f"Could not add task: {error}")
            finally:
                if cursor is not None:
                    cursor.close()
                connection.close()


# Load tasks
df = load_tasks()

# Update Task
st.divider()
st.subheader("✏️ Update Task")

if df.empty:
    st.info("There are no tasks available to update or delete.")
else:
    task_options = {
        f'#{int(row["task_id"])} — {row["Task"]} ({row["Employee"]})': int(row["task_id"])
        for _, row in df.iterrows()
    }
    selected_label = st.selectbox(
        "Select a task to update",
        options=list(task_options.keys()),
        key="update_task_select",
    )
    selected_task_id = task_options[selected_label]
    selected_row = df.loc[df["task_id"] == selected_task_id].iloc[0]

    with st.form("update_task_form"):
        update_col1, update_col2, update_col3 = st.columns(3)
        with update_col1:
            updated_status = st.selectbox(
                "Status",
                ["Pending", "Completed", "Overdue"],
                index=["Pending", "Completed", "Overdue"].index(selected_row["Status"]),
            )
        with update_col2:
            updated_priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"],
                index=["Low", "Medium", "High"].index(selected_row["Priority"]),
            )
        with update_col3:
            current_due_date = selected_row["Due Date"]
            if pd.isna(current_due_date):
                current_due_date = pd.Timestamp.today().date()
            elif hasattr(current_due_date, "date"):
                current_due_date = current_due_date.date()
            updated_due_date = st.date_input("Due Date", value=current_due_date)

        update_submitted = st.form_submit_button("💾 Save Changes")

    if update_submitted:
        connection = get_db_connection()
        if connection is not None:
            cursor = None
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    UPDATE tasks
                    SET status = %s, priority = %s, due_date = %s
                    WHERE task_id = %s
                    """,
                    (updated_status, updated_priority, updated_due_date, selected_task_id),
                )
                connection.commit()
                st.cache_data.clear()
                st.success("Task updated successfully!")
                st.rerun()
            except Exception as error:
                st.error(f"Could not update task: {error}")
            finally:
                if cursor is not None:
                    cursor.close()
                connection.close()


# Delete Task
st.divider()
st.subheader("🗑️ Delete Task")

if df.empty:
    st.info("There are no tasks available to delete.")
else:
    delete_options = {
        f'#{int(row["task_id"])} — {row["Task"]} ({row["Employee"]})': int(row["task_id"])
        for _, row in df.iterrows()
    }
    delete_label = st.selectbox(
        "Select a task to delete",
        options=list(delete_options.keys()),
        key="delete_task_select",
    )
    delete_task_id = delete_options[delete_label]
    delete_row = df.loc[df["task_id"] == delete_task_id].iloc[0]

    st.warning(
        f'You selected task "{delete_row["Task"]}" assigned to {delete_row["Employee"]}. '
        "Deleting it will permanently remove it from the database."
    )
    confirm_delete = st.checkbox(
        "I understand this task will be permanently deleted.",
        key="confirm_delete_task",
    )

    if st.button("🗑️ Delete Selected Task", type="primary"):
        if not confirm_delete:
            st.warning("Please tick the confirmation checkbox before deleting.")
        else:
            connection = get_db_connection()
            if connection is not None:
                cursor = None
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (delete_task_id,))
                    connection.commit()
                    st.cache_data.clear()
                    st.success("Task deleted successfully!")
                    st.rerun()
                except Exception as error:
                    st.error(f"Could not delete task: {error}")
                finally:
                    if cursor is not None:
                        cursor.close()
                    connection.close()


# Reload current task data after database actions
df = load_tasks()

if df.empty:
    st.warning("No tasks found. Check the MySQL connection and tasks table.")
    if st.button("Retry loading tasks"):
        st.cache_data.clear()
        st.rerun()
    st.stop()

# Search and filters
st.divider()
st.subheader("🔎 Search & Filter Tasks")

search_col1, search_col2 = st.columns(2)
with search_col1:
    search_text = st.text_input(
        "Search by task or employee name",
        placeholder="e.g. Sales Report or Amit",
        key="task_search",
    )
with search_col2:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Completed", "Overdue"],
        key="status_filter",
    )

priority_filter = st.selectbox(
    "Filter by Priority",
    ["All", "Low", "Medium", "High"],
    key="priority_filter",
)

filtered_df = df.copy()

if search_text.strip():
    term = search_text.strip()
    filtered_df = filtered_df[
        filtered_df["Task"].astype(str).str.contains(term, case=False, na=False)
        | filtered_df["Employee"].astype(str).str.contains(term, case=False, na=False)
    ]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

if priority_filter != "All":
    filtered_df = filtered_df[filtered_df["Priority"] == priority_filter]

st.caption(f"Showing {len(filtered_df)} of {len(df)} tasks")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# KPI cards based on all tasks, not filtered subset
total_tasks = len(df)
completed_tasks = int((df["Status"] == "Completed").sum())
pending_tasks = int((df["Status"] == "Pending").sum())
overdue_tasks = int((df["Status"] == "Overdue").sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tasks", total_tasks)
col2.metric("Completed Tasks", completed_tasks)
col3.metric("Pending Tasks", pending_tasks)
col4.metric("Overdue Tasks", overdue_tasks)

st.divider()

# Charts based on all tasks
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📌 Tasks by Status")
    status_data = df["Status"].value_counts().reset_index()
    status_data.columns = ["Status", "Count"]
    fig1 = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.45,
        title="Task Status Distribution",
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.subheader("👥 Employee Task Overview")
    employee_data = df.groupby("Employee").size().reset_index(name="Tasks")
    fig2 = px.bar(
        employee_data,
        x="Employee",
        y="Tasks",
        text="Tasks",
        title="Tasks Assigned by Employee",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.caption("Work Tracker Dashboard | Python • MySQL • Streamlit • Plotly")
