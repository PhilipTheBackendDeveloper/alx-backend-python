#!/usr/bin/python3
"""
0-stream_users.py
Provides a generator function stream_users() that yields rows from
the user_data table in ALX_prodev one by one as dictionaries.
"""

import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator that connects to ALX_prodev and yields each row from user_data
    as a dictionary: {'user_id': ..., 'name': ..., 'email': ..., 'age': ...}

    NOTE:
    - This function contains only one loop (the required one).
    - Adjust MySQL credentials below if necessary.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",               # <-- change if different
            password="7htrmf8e@E",     # <-- change to your MySQL password
            database="ALX_prodev"
        )
        # dictionary=True makes each row a dict
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        # single loop required by the task:
        for row in cursor:
            yield row

    except Error as e:
        # Print error and stop generator (optional)
        print(f"[stream_users] MySQL error: {e}")
        return
    finally:
        # cleanup: executed when generator finishes or is closed
        try:
            if cursor is not None:
                cursor.close()
        except Exception:
            pass
        try:
            if conn is not None and conn.is_connected():
                conn.close()
        except Exception:
            pass
