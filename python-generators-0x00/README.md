# alx-backend-python

# Python Generators - ALX Backend Project 0

## Project Overview
This project demonstrates the use of **Python generators** and how to efficiently handle data from a MySQL database.  
The main goal is to create a script (`seed.py`) that connects to MySQL, creates a database and table, and inserts sample data from a CSV file (`user_data.csv`). This setup prepares the project for memory-efficient data processing in later tasks.

## Project Structure

python-generators-0x00/
├── seed.py # Script to connect to MySQL, create DB/table, and insert data
├── user_data.csv # Sample CSV data for the user_data table
└── README.md # Project documentation

markdown
Copy code

## Requirements

- Python 3.x
- MySQL server installed
- `mysql-connector-python` library
- `user_data.csv` file with sample data

## Setup Instructions

-Verify in MySQL Workbench:

-Open MySQL Workbench

-Check that the database ALX_prodev exists

-Open the table user_data and confirm rows from user_data.csv were inserted

## How It Works

-connect_db() → Connects to MySQL server (no database yet)

-create_database(connection) → Creates ALX_prodev if it does not exist

-connect_to_prodev() → Connects directly to ALX_prodev database

-create_table(connection) → Creates user_data table with columns:

-user_id (UUID, primary key, indexed)

-name (VARCHAR, NOT NULL)

-email (VARCHAR, NOT NULL)

-age (DECIMAL, NOT NULL)

-insert_data(connection, "user_data.csv") → Reads CSV and inserts rows into the table

-0-main.py → Runs all functions and prints first 5 rows as a test

Notes
-Used environment variables for security.

-The CSV file must be in the same directory as seed.py.

-This project sets up the database and table for later use with Python generators.
