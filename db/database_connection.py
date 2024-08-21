import mysql.connector

db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'raise_on_warnings': True
}

def database_connection():
    # Connect to the MySQL server without specifying a database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Check if the 'bank' database exists
    cursor.execute("SHOW DATABASES LIKE 'bank';")
    result = cursor.fetchone()

    if result:
        # If 'bank' exists, switch to the 'bank' database
        cursor.execute("USE bank;")

    return conn, cursor