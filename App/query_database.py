from database import get_connection


def execute_query(sql):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    sql = """
    SELECT Country, SUM(Revenue) AS TotalRevenue
    FROM retail_sales
    GROUP BY Country
    ORDER BY TotalRevenue DESC
    LIMIT 1;
    """

    results = execute_query(sql)

    print("\n========== MYSQL RESULT ==========")

    for row in results:
        print(row)