import mysql.connector
from database_connection import database_connection

def seed_database(script_path):
    try:
        # Establish connection and cursor from imported function
        conn, cursor = database_connection()

        # Read commands from SQL file
        with open(script_path, 'r', encoding="utf-8") as file:
            sql_script = file.read()

        # Split the script into individual statements if needed
        sql_commands = sql_script.split(';')
        for command in sql_commands:
            if command.strip():  # Avoid executing empty strings
                cursor.execute(command)
        
        # Execute command to create the trigger on transaction table
        with open("db/seed_database_trans_trigger.sql", 'r', encoding="utf-8") as file:
            trigger_command = file.read()
            cursor.execute(trigger_command)
                
        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        # Always close the cursor and connection
        cursor.close()
        conn.close()

# Run the seed_database function
seed_database("db/seed_database_script.sql")