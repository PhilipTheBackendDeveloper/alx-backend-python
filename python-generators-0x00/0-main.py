import seed

if __name__ == "__main__":
    connection = seed.connect_db()
    if connection:
        for row in seed.stream_user_data(connection):
            print(row)
        connection.close()
