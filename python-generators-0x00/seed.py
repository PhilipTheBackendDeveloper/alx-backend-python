import mysql.connector
from mysql.connector import Error
import csv
import uuid

def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="7htrmf8e@E"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
<<<<<<< HEAD
            print("✅ Database ALX_prodev created successfully (or already exists)")
=======
            print(" Database ALX_prodev created successfully (or already exists)")
>>>>>>> c5118663a28d1472ff7d24fa156e98785a87c25b
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_table():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="7htrmf8e@E",
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    age INT
                )
            """)
<<<<<<< HEAD
            print("✅ Table user_data created successfully")
=======
            print(" Table user_data created successfully")
>>>>>>> c5118663a28d1472ff7d24fa156e98785a87c25b
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_data(csv_file):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="7htrmf8e@E",
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor()

            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    user_id = str(uuid.uuid4())
                    name = row['name']
                    email = row['email']
                    age = row['age']

                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))

            connection.commit()
<<<<<<< HEAD
            print("✅ Data inserted successfully")
=======
            print(" Data inserted successfully")
>>>>>>> c5118663a28d1472ff7d24fa156e98785a87c25b
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def stream_user_data(connection):
    """
    Generator that yields one row at a time from user_data table
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    
def connect_db():
    """
    Connects to the ALX_prodev database and returns the connection
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="7htrmf8e@E",  # use your root password
            database="ALX_prodev"
        )
        if connection.is_connected():
<<<<<<< HEAD
            print("✅ Connected to ALX_prodev database")
=======
            print(" Connected to ALX_prodev database")
>>>>>>> c5118663a28d1472ff7d24fa156e98785a87c25b
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
