import mysql.connector
import streamlit as st

def get_db_connection():
"""Connect to the hosted Aiven MySQL database."""
try:
config = st.secrets["mysql"]

```
    connection = mysql.connector.connect(
        host=config["host"],
        port=int(config["port"]),
        database=config["database"],
        user=config["user"],
        password=config["password"],
        ssl_disabled=False,
        connection_timeout=15,
    )
    return connection

except Exception as error:
    st.error(f"MySQL connection failed: {error}")
    return None
```
