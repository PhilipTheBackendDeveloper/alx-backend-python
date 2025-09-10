#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime   # ✅ Required import

# Decorator to log SQL queries


def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
