import mysql.connector

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}

def database_connection():
    # Connect to the MySQL server without specifying a database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Check if the 'bank' database exists
    cursor.execute("SHOW DATABASES LIKE 'bank';")
    result = cursor.fetchone()

    if result:
        # If 'bank' exists, switch to the 'bank' database
        cursor.execute("USE bank;")

    return conn, cursor