#!/usr/bin/env python3
"""
4-cache_query.py

Implements:
 - with_db_connection: ensures DB connection lifecycle.
 - cache_query: caches query results to avoid redundant DB calls.

Usage:
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
"""

import sqlite3
import functools
from typing import Callable, Any, Optional

# Global dictionary for caching query results
query_cache = {}


# ------------------------------
# Decorator 1: with_db_connection
# ------------------------------
def with_db_connection(func: Callable) -> Callable:
    """
    Ensures wrapped function has a sqlite3 connection.
    - If `conn` is provided, it will be used (not closed).
    - If not, it will open `users.db`, inject it, and close afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "conn" in kwargs and kwargs["conn"] is not None:
            return func(*args, **kwargs)

        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect("users.db")
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper


# ------------------------------
# Decorator 2: cache_query
# ------------------------------
def cache_query(func: Callable) -> Callable:
    """
    Decorator to cache query results based on the SQL query string.
    - Uses a global dictionary `query_cache`.
    - Key is the SQL query string.
    - Avoids re-executing the same query multiple times.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query is None:
            raise ValueError("cache_query requires 'query' argument")

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


# ------------------------------
# Example usage
# ------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn: sqlite3.Connection, query: str):
    """
    Fetch users from DB. Results are cached by query string.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# --- helper for testing locally ---
def _ensure_sample_db():
    """Create users.db with a sample users table if missing."""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (username, email) VALUES (?, ?);",
            [("alice", "alice@example.com"),
             ("bob", "bob@example.com"),
             ("carol", "carol@example.com")]
        )
        conn.commit()
    conn.close()


if __name__ == "__main__":
    _ensure_sample_db()

    print("\n--- First call (cache miss, DB executed) ---")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    print("\n--- Second call (cache hit, no DB query) ---")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)

    print("\n--- Different query (new cache miss) ---")
    one_user = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
    print(one_user)
