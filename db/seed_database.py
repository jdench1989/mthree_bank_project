import mysql.connector
from database_connection import database_connection

def seed_database(script_paths):
    try:
        # Establish connection and cursor from imported function
        conn, cursor = database_connection()
        for script_path in script_paths:

            # Read commands from SQL file
            if "trigger" in script_path: # Must be passed to MySQL as a single command to prevent delimiter errors
                with open(script_path, 'r', encoding="utf-8") as file:
                    sql_script = file.read()
                    cursor.execute(sql_script)

            else: # Non-trigger scripts can be split into individual commands
                with open(script_path, 'r', encoding="utf-8") as file:
                    sql_script = file.read()

                # Split the script into individual statements
                sql_commands = sql_script.split(';')
                for command in sql_commands:
                    if command.strip():  # Avoid executing empty strings
                        cursor.execute(command)
            
            # Commit the transaction
            conn.commit()

    except mysql.connector.Error as err: # If the try block throws an error print the error to the terminal and rollback any changes to the database
        print(f"Error: {err}")
        conn.rollback()

    finally:
        # Always close the cursor and connection
        cursor.close()
        conn.close()

# Define a list of paths for script files to be executed
script_paths = [
    "db/seed_database_table_setup.sql",
    "db/seed_database_trans_trigger.sql",
    "db/seed_database_dummy_data.sql"
]

# Call the seed_database function
seed_database(script_paths)