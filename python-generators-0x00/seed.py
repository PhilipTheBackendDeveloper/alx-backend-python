import mysql.connector
import csv
import os  # to read environment variables

# Get MySQL password from environment
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

if not MYSQL_PASSWORD:
    raise ValueError("Environment variable MYSQL_PASSWORD not set")

#  1. Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      
            password=MYSQL_PASSWORD  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

#  2. Create database ALX_prodev 
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()

#  3. Connect directly to ALX_prodev 
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=MYSQL_PASSWORD,  
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

#  4. Create table user_data 
def create_table(connection):
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
    cursor.close()

#  5. Insert CSV data 
def insert_data(connection, csv_file="user_data.csv"):
    cursor = connection.cursor()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    email=VALUES(email),
                    age=VALUES(age);
            """, row)
    connection.commit()
    cursor.close()

#  Main flow 
if __name__ == "__main__":
    # Connecting to MySQL server
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    #  Connecting to ALX_prodev DB
    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, "user_data.csv")
        conn.close()
        print("✅ Database seeded successfully!")
