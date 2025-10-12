#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database
    """
    connection = seed.connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Lazily load users page by page
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:   # stop when no more data
            break
        yield page
        offset += page_size
