#!/usr/bin/env python3
"""
3-concurrent.py

Run multiple database queries concurrently using asyncio.gather
with aiosqlite for async DB access.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
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
    # Ensure users table exists and seed if empty
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
