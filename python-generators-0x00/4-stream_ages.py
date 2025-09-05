#!/usr/bin/python3
"""
Memory-Efficient Aggregation with Generators:
- Stream user ages from the database one by one
- Compute the average age without loading all data in memory
"""

import seed  # reuse database setup and connection


def stream_user_ages():
    """
    Generator that streams user ages from the user_data table.
    Fetches rows one by one using a cursor.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    # only one loop (streaming)
    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate the average age.
    Does not load the entire dataset into memory.
    """
    total_age = 0
    count = 0

    # only one loop (aggregation)
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
