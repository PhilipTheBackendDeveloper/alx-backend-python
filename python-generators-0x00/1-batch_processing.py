#!/usr/bin/python3
"""
Batch processing of users from the database using generators
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    Yields a list of dictionaries, each batch containing up to batch_size users.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # adjust if different
        password="root",   # adjust if different
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield remaining rows if not empty
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Process batches of users, filtering users older than 25,
    and printing them one by one.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
