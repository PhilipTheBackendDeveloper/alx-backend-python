#!/usr/bin/python3
import sqlite3
import functools

# In-memory cache dictionary
query_cache = {}


def with_db_connection(func):
    """Decorator to manage opening and closing DB connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """Decorator to cache query results"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            # Return cached result
            return query_cache[query]
        # Execute query and store result in cache
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call → hits DB
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call:", users)

    # Second call → uses cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call (from cache):", users_again)
