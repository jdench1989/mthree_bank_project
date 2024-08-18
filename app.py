from flask import Flask, jsonify, request
from db.database_connection import database_connection
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def index():
    # Eventually will show login page and then show main menu for logged in user
    # conn, cursor = database_connection()
    # cursor.close()
    # conn.close()
    pass

@app.route('/customers')
def get_customers():  # 
    """Return details of all customers or search a specific customer
    ---
    parameters:
      - name: customer_id
        in: query
        type: string
    responses:
      200:
        description: A list of customers, optionally filtered by query strings
    """
    conn, cursor = database_connection()  # Establish database connection
    sql_query = "SELECT * FROM customers"  # Base SQL query
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

    cursor.execute(sql_query, values) # Execute SQL query
    res = cursor.fetchall()  # Extract results
    cursor.close()
    conn.close()
    return jsonify(res), 200


@app.route('/customers', methods=['POST'])
def create_customer(): # Create a new customer record in the database
    conn, cursor = database_connection()  # Establish database connection

    # Extract form data
    form_values = []
    for key in request.form:
        form_values.append(request.form[key])
    
    # SQL query using placeholders
    sql_query = "INSERT INTO customers (status, last_name, first_name, dob, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    cursor.execute(sql_query, form_values)  # Execute SQL query
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Customer created successfully"}), 200

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):  # Update a customer record in the database
    conn, cursor = database_connection()  # Establish database connection
    sql_query = "UPDATE customers SET "  # Base SQL query

    # Extract columns and values to be updated from the request JSON
    data = request.json
    update_columns = []
    values = []
    for key, value in data.items():
        update_columns.append(f"{key} = %s")
        values.append(value)

    # Compile columns and values into a SQL query using placeholders
    sql_query += ", ".join(update_columns) + " WHERE customer_id = %s"
    values.append(customer_id)

    cursor.execute(sql_query, values) # Execute the query
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message":"customer record updated successfully"}), 200

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):  # Delete a customer record from the database only if no account dependency
    conn, cursor = database_connection()  # Establish database connection

    # Check the database to see if the provided customer has an associated account
    cursor.execute("SELECT account_id FROM accounts WHERE customer_id = %s LIMIT 1;", [customer_id])
    account_record = cursor.fetchone()  # Fetch the first result if it exists

    res = {}
    if account_record:  # Check if account_record is not None
        res["success"] = "false"
        res["message"] = "Customer cannot be deleted. Customer record is associated with an account record. Deactivate customer instead."
    else:  # If there is no account record then the customer can be safely deleted
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", [customer_id])
        res["success"] = "true"
        res["message"] = "Customer record deleted successfully."
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(res), 200

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
