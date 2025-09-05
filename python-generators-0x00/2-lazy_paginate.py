#!/usr/bin/python3
"""
Lazy loading paginated data from user_data table using generators
"""

import seed  # reuse database connection setup from seed.py


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from user_data table.
    - page_size: number of rows per page
    - offset: where to start fetching rows
    Returns a list of rows (as dicts).
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that yields pages of users lazily.
    It fetches the next page only when needed.

    Uses only one loop:
    - starts at offset = 0
    - fetches a page
    - yields it if not empty
    - stops when no rows are left
    """
    offset = 0
    while True:   # only one loop
        page = paginate_users(page_size, offset)
        if not page:   # no more rows
            break
        yield page
        offset += page_size
