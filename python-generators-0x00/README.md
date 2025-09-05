# Python Generators - Getting Started

## Objective

Create a generator that streams rows from an SQL database one by one.

## Implemented Features

- `connect_db()`: Connect to MySQL server
- `create_database()`: Create `ALX_prodev` if not exists
- `connect_to_prodev()`: Connect to `ALX_prodev`
- `create_table()`: Create `user_data` table
- `insert_data()`: Populate `user_data` from `user_data.csv`
- `stream_user_data()`: **Generator that streams rows lazily using `yield`**

## Usage

```bash
./0-main.py
```
