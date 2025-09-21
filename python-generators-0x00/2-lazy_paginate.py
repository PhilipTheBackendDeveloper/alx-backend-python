#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """Fetch a page of users from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator that lazily yields pages of users"""
    offset = 0

    while True:  # Loop 1: only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:  # If no more rows, stop the generator
            return
        yield page  # Yield the current page
        offset += page_size  # Move offset for the next page
