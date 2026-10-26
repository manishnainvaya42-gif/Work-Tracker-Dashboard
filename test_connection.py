import streamlit as st
from db_connection import get_db_connection

st.set_page_config(page_title="MySQL Connection Test", page_icon="🔌")
st.title("🔌 MySQL Connection Test")

connection = get_db_connection()

if connection is not None:
    try:
        if connection.is_connected():
            st.success("MySQL Connection Successful!")
            st.write("Database: work_tracker_db")
        else:
            st.error("MySQL connection was not established.")
    finally:
        connection.close()
else:
    st.error("MySQL Connection Failed. Check .streamlit/secrets.toml and MySQL.")
