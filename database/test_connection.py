from database import get_connection

try:
    connection = get_connection()
    print("PostgreSQL connected successfully!")
    connection.close()
except Exception as error:
    print("Connection failed:")
    print(error)