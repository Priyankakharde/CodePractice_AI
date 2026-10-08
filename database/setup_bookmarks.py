from database import get_connection


connection = None

try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL
                REFERENCES users(id) ON DELETE CASCADE,
            lesson_id INTEGER NOT NULL
                REFERENCES lessons(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (user_id, lesson_id)
        );
        """
    )

    connection.commit()

    print("Bookmarks table created successfully!")

except Exception as error:
    if connection:
        connection.rollback()

    print("Failed to create bookmarks table:")
    print(error)

finally:
    if connection:
        connection.close()
        