#!/usr/bin/python3
import time
import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """The decorator to retry DB operation if it fails"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempts += 1
                    if attempts >= retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
