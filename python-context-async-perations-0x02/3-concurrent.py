#!/usr/bin/env python3
"""
3-concurrent.py

Task:
- Run multiple database queries concurrently using asyncio.gather
- Use aiosqlite for async DB access
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="users.db"):
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_name="users.db", age_limit=40):
    """Fetch users older than age_limit asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (age_limit,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Run both fetch queries concurrently using asyncio.gather."""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\nAll Users:")
    for user in results_all:
        print(user)

    print("\nUsers older than 40:")
    for user in results_older:
        print(user)


if __name__ == "__main__":
    # Create sample data if not exists
    import sqlite3
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER DEFAULT 30
    )
    """)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
            [
                ("alice", "alice@example.com", 22),
                ("bob", "bob@example.com", 29),
                ("carol", "carol@example.com", 34),
                ("david", "david@example.com", 45),
                ("eva", "eva@example.com", 52),
            ]
        )
        conn.commit()
    conn.close()

    # Run async queries concurrently
    asyncio.run(fetch_concurrently())
