import mysql.connector

db_config = {
    # Ensure config details are correct for your user and environment
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'bank'
}

def database_connection():
    conn =  mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

database_connection()