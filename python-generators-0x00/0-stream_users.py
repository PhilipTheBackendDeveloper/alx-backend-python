#!/usr/bin/python3
import mysql.connector
import os

MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

def stream_users():
    """Generator that streams rows from user_data table one by one"""
    
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)
    
    # Fetch all rows lazily, yielding one at a time
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # yield each row as a dictionary
    
    cursor.close()
    connection.close()
