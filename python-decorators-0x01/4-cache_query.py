#!/usr/bin/env python3
import time
import sqlite3
import functools

# simple in-memory query cache
query_cache = {}


def with_db_connection(func):
    """Decorator to handle opening and closing database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results based on SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None)
        if query is None and len(args) > 1:  # skip conn, get query from second arg
            query = args[1]

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call -> runs query
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call -> returns from cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
