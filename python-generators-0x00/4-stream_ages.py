#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one from user_data"""
    connection = seed.connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculate average age of users using the generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
