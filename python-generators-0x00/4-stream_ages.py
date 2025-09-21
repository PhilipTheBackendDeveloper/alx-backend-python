#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:        # Loop 1
        yield row['age']      # Yield one age at a time
    
    cursor.close()
    connection.close()
    return                    # End of generator

def calculate_average_age():
    """Calculate average age using the generator"""
    total = 0
    count = 0
    
    for age in stream_user_ages():  # Loop 2
        total += age
        count += 1
    
    if count == 0:
        return 0
    
    average = total / count
    print(f"Average age of users: {average}")
