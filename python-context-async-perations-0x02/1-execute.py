#!/usr/bin/env python3
"""
Custom class-based context manager for executing queries
"""

import sqlite3


class ExecuteQuery:
    """Context manager that executes a SQL query and returns results"""

    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and optional parameters
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and fetch results"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("test.db", query, (25,)) as results:
        for row in results:
            print(row)
