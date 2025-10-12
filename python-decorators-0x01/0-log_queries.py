#!/usr/bin/python3
import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """Decorator to log SQL queries before execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print("Users:", users)
