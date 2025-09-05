#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        print("\nStreaming rows one by one using generator:")
        for row in seed.stream_user_data(connection, batch_size=5):
            # row is a dict like {'user_id': ..., 'name': ..., 'email': ..., 'age': ...}
            print(row)
