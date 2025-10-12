#!/usr/bin/python3
"""
1-batch_processing.py

Provides:
- stream_users_in_batches(batch_size): generator yielding lists (batches) of rows
- batch_processing(batch_size): processes each batch and prints users with age > 25

Loops used:
- stream_users_in_batches: 1 loop (while + fetchmany)
- batch_processing: 2 loops (for batch, for user)
Total loops = 3
"""

import mysql.connector
from mysql.connector import Error

# Update these credentials if yours are different
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "7htrmf8e@E",   # change to your MySQL password
    "database": "ALX_prodev"
}

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches (lists) of rows from user_data table.
    Each yielded item is a list of dict rows (cursor with dictionary=True).
    Uses a single loop (while) and cursor.fetchmany(batch_size).
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        while True:                       # loop #1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"[stream_users_in_batches] MySQL error: {e}")
        return
    finally:
        # Ensure resources are closed when generator finishes or is GC'ed
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

def batch_processing(batch_size):
    """
    Processes batches produced by stream_users_in_batches.
    For each user in a batch, if age > 25 it prints the user dict.

    Loops:
      for batch in stream_users_in_batches(...) -> loop #2
          for user in batch -> loop #3
    """
    for batch in stream_users_in_batches(batch_size):   # loop #2
        for user in batch:                              # loop #3
            # age might be int, Decimal, or string depending on DB; normalize to float
            try:
                age_val = float(user.get("age", 0))
            except (TypeError, ValueError):
                continue
            if age_val > 25:
                print(user)
