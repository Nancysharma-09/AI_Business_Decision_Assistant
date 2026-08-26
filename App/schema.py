from database import get_connection


def get_schema():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DESCRIBE retail_sales")

    columns = cursor.fetchall()

    cursor.close()
    connection.close()

    return columns


if __name__ == "__main__":
    columns = get_schema()

    print("\n========== DATABASE SCHEMA ==========")

    for column in columns:
        print(
            f"Column: {column[0]} | "
            f"Type: {column[1]}"
        )