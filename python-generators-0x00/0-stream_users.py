#!/usr/bin/python3
"""
Stream users from the database one by one using a generator
"""

import mysql.connector


def stream_users():
    """
    Generator function that yields rows from the user_data table one by one.
    Uses yield to avoid loading all rows into memory at once.
    """
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # change to your MySQL username if different
        password="root",   # change if your MySQL password is different
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)

    # Execute query
    cursor.execute("SELECT * FROM user_data")

    # Loop through cursor and yield one row at a time
    for row in cursor:
        yield row

    # Cleanup
    cursor.close()
    connection.close()
