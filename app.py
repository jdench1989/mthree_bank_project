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
def get_customers():  # Return details of all customers or search a specific customer
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
    # Establish database connection
    conn, cursor = database_connection()

    #Base SQL query
    sql_query = "SELECT * FROM accounts"
    filters = []
    values = []

    #check for query parameters
    sort_code = request.args.get('sort_code')
    account_id=request.args.get('account_id')
    account_num = request.args.get('account_num')
    status = request.args.get('status')
    balance = request.args.get('balance')
    type_id = request.args.get('type_id')
    customer_id = request.args.get('customer_id')
    creation_date = request.args.get('creation_date') 

    # Add filters based on the provided query parameters

    if account_id:
        filters.append("account_id = %s")
        values.append(account_id)
    if sort_code:
        filters.append("sort_code = %s")
        values.append(sort_code)
    if account_num:
        filters.append("account_num = %s")
        values.append(account_num)
    if status:
        filters.append("status = %s")
        values.append(status)  
    if balance:
        filters.append("balance = %s")
        values.append(balance)
    if sort_code:
        filters.append("type_id = %s")
        values.append(type_id)  
    if sort_code:
        filters.append("customer_id = %s")
        values.append(customer_id)  
    if sort_code:
        filters.append("creation_date = %s")
        values.append(creation_date) 

    #Add filters to SQL query if there are any
    if filters:
        sql_query += " WHERE " + " AND ".join(filters)
    
    #Execute the SQL sqlQuery
    cursor.execute(sql_query,values)
    res=cursor.fetchall()

    # close cursor and connection
    cursor.close()
    conn.close()


    return jsonify(res), 200

@app.route('/accounts', methods=['POST'])
def create_account(): 
     # Connect to the database
    conn, cursor = database_connection()

    #Etract form data
    form_values = []
    for key in  request.form:
        form_values.append(request.form[key])
    
    #SQL query using placeholders
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
  

@app.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    conn, cursor = database_connection()  # Establish database connection
    

    # Extract columns and values to be updated from the request JSON
    #data = request.get_json()
    status = request.form.get('status')

    #check if status is provided in request
    if not status:
        return jsonify({"error : missing 'status' field"}),400

    # execute the query
    try:
        sql_query = "UPDATE accounts SET status = %s WHERE account_id = %s"
        cursor.execute(sql_query, (status, account_id))

    
        conn.commit()
        return jsonify({"message":"account status updated successfully"}), 200
    
    except Exception as err:
        # Rollback in case of error
        conn.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


@app.route('/transactions')
def get_transactions():  # Return details of all transactions or search a specific transaction
    conn, cursor = database_connection()  # Establish database connection
    sql_query = """SELECT * FROM customers c INNER JOIN accounts a ON c.customer_id = a.customer_id
                 INNER JOIN accounts_transactions a_tr ON a_tr.account_id= a.account_id
                 INNER JOIN transactions t on a_tr.transaction_id=t.transaction_id """  # Base SQL query
    filters = []
    values = []


    # Check for query parameters
    customer_id = request.args.get('customer_id') # .../customers?customer_id=4
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    sort_code = request.args.get('sort_code')
    account_num = request.args.get('account_num')
    transaction_date_earliest = request.args.get('transaction_time_earliest')
    transaction_date_latest = request.args.get('transaction_time_latest')


    # Add filters based on the provided query parameters
    if customer_id:
        filters.append("c.customer_id = %s")
        values.append(customer_id)
    if first_name:
        filters.append("c.first_name LIKE %s")
        values.append(f"%{first_name}%")
    if last_name:
        filters.append("c.last_name LIKE %s")
        values.append(f"%{last_name}%")
    if account_num:
        filters.append("a.account_num = %s")
        values.append(account_num)
    if sort_code:
        filters.append("a.sort_code = %s")
        values.append(sort_code)

    if transaction_date_earliest:
        filters.append("date(t.transaction_time) >= %s")
        values.append(transaction_date_earliest)
    if transaction_date_latest:
        filters.append("date(t.transaction_time) <= %s")
        values.append(transaction_date_latest)

    # Add filters to SQL query if there are any
    if filters:
        sql_query += " WHERE " + " AND ".join(filters)

     # Print the query and parameters
    print("SQL Query:", sql_query)
    print("Values:", values)


    cursor.execute(sql_query, values) # Execute SQL query
    res = cursor.fetchall()  # Extract results
    cursor.close()
    conn.close()
    return jsonify(res), 200


@app.route('/transactions', methods=['POST'])
def create_transaction():
    # Create a new transaction
    conn, cursor = database_connection()  # Establish database connection

    # Extract form data
    form_values = []
    for key in request.form:
        form_values.append(request.form[key])
    
    try:
        # SQL query using placeholders
        sql_query = "INSERT INTO transactions (type_id, account_from, account_to, amount) VALUES (%s, %s, %s, %s);"

        cursor.execute(sql_query, form_values)  # Execute SQL query
        conn.commit()
        return jsonify({"message": "Transaction created successfully"}), 200
    
    except Exception as err:
        # Rollback in case of error
        conn.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()
 


#if __name__ == '__main__':
app.run(host="0.0.0.0", port=5001)
