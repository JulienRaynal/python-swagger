import mysql.connector


def request_database(get_string: str) -> list:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="marthos"
    )
    cursor = conn.cursor()
    cursor.execute(get_string)
    results: list = cursor.fetchall()
    conn.close()
    cursor.close()
    return results


def execute_database(execute_string: str) -> None:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="marthos"
    )
    cursor = conn.cursor()
    cursor.execute(execute_string)
    conn.commit()
    conn.close()
    cursor.close()
