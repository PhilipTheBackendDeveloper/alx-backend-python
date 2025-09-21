#!/usr/bin/python3
import mysql.connector
import os

# Get MySQL password from environment variable
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from the database in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:          # Loop 1: iterate over all rows
        batch.append(row)
        if len(batch) == batch_size:
            yield batch        # Yield a batch of rows
            batch = []
    
    if batch:
        yield batch            # Yield any remaining rows

    # Stop the generator explicitly (optional)
    return
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes each batch to filter users over 25"""
    for batch in stream_users_in_batches(batch_size):   # Loop 2: iterate over batches
        for user in batch:                              # Loop 3: iterate inside batch
            if user['age'] > 25:
                yield user  # Yield each filtered user one by one
    
    # Stop the generator safely (optional)
    return
