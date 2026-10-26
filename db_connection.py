import mysql.connector
import streamlit as st


def get_db_connection():
    """Create and return a MySQL connection, or None if it fails."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=st.secrets["mysql"]["password"],
            database="work_tracker_db",
        )
    except (mysql.connector.Error, KeyError, FileNotFoundError) as error:
        st.error(f"MySQL connection failed: {error}")
        return None
