from flask import Flask, jsonify, request
from db.database_connection import database_connection

app = Flask(__name__)

@app.route('/')
def index():
    # Eventually will show login page and then show main menu for logged in user
    # conn, cursor = database_connection()
    # cursor.close()
    # conn.close()
    pass

@app.route('/customers')
def get_customers():
    # Establish database connection
    conn, cursor = database_connection()

    # Base SQL query
    sql_query = "SELECT * FROM customers"
    filters = []
    values = []

    # Check for query parameters
    customer_id = request.args.get('customer_id') # .../customers?customer_id=4
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    # Add filters based on the provided query parameters
    if customer_id:
        filters.append("customer_id = %s")
        values.append(customer_id)
    if first_name:
        filters.append("first_name LIKE %s")
        values.append(f"%{first_name}%")
    if last_name:
        filters.append("last_name LIKE %s")
        values.append(f"%{last_name}%")
    if email:
        filters.append("email LIKE %s")
        values.append(f"%{email}%")

    # Add filters to SQL query if there are any
    if filters:
        sql_query += " WHERE " + " AND ".join(filters)

    # Execute the SQL query
    cursor.execute(sql_query, values)
    res = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Return the results as JSON
    return jsonify(res), 200


@app.route('/customers', methods=['POST'])
def create_customer():
    # Create a new customer record in the database

    # Establish database connection
    conn, cursor = database_connection()

    # Extract form data
    form_values = []
    for key in request.form:
        form_values.append(request.form[key])
    
    # SQL query using placeholders
    sql_query = "INSERT INTO customers (status_id, last_name, first_name, dob, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    # Execute SQL substituting placeholder values. Close connection and return success message
    cursor.execute(sql_query, form_values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Customer created successfully"}), 200

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    # Update a customer record in the database
    conn, cursor = database_connection()
    sql_query = "UPDATE customers SET "
    data = request.json
    update_columns = []
    values = []
    for key, value in data.items():
        update_columns.append(f"{key} = %s")
        values.append(value)
    sql_query += ", ".join(update_columns) + " WHERE customer_id = %s"
    values.append(customer_id)
    cursor.execute(sql_query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"customer record updated successfully"}), 200

@app.route('/customers', methods=['DELETE'])
def delete_customer():
    # Delete a customer record from the database
    # Allow for foreign key dependency issues
    pass

@app.route('/accounts')
def get_accounts():
    # Return details of accounts
    pass

@app.route('/accounts', methods=['POST'])
def create_account():
    # Create a new account in the database
    pass

@app.route('/accounts', methods=['PUT'])
def update_account():
    # Update account record in the database
    pass

@app.route('/accounts', methods=['DELETE'])
def close_account():
    # Close an account
    pass

@app.route('/transactions')
def get_transactions():
    # Return details of transactions
    pass

@app.route('/transactions', methods=['POST'])
def create_transaction():
    # Create a new transaction
    pass


app.run(host="0.0.0.0", port=5000)
