# Python Generators - Getting Started

## Task: Getting started with python generators

### Objective

Create a generator that streams rows from an SQL database one by one.

### Steps Implemented

1. Connect to MySQL server.
2. Create a database `ALX_prodev` if it does not exist.
3. Create a table `user_data` with:
   - `user_id` (Primary Key, UUID, Indexed)
   - `name` (VARCHAR, NOT NULL)
   - `email` (VARCHAR, NOT NULL)
   - `age` (DECIMAL, NOT NULL)
4. Populate table using `user_data.csv`.
5. Verify setup with `0-main.py`.

### Usage

```bash
# Run setup
./0-main.py
```
