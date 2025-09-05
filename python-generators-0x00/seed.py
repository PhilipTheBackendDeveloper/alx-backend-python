#!/usr/bin/python3
"""
seed.py - Set up MySQL database ALX_prodev and populate user_data table
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connect to MySQL server (no specific database yet)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # Change if using a different MySQL user
            password="password"  # Change to your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert data from CSV into user_data if not already present"""
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if email already exists (avoid duplicates)
                cursor.execute(
                    "SELECT * FROM user_data WHERE email = %s", (row["email"],))
                if cursor.fetchone() is None:
                    user_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s);
                    """, (user_id, row["name"], row["email"], row["age"]))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
