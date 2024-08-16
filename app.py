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
    sql_query = " INSERT INTO accounts ( account_num,sort_code,type_id,status,balance,creation_date,customer_id) VALUES ( %s, %s, %s, %s, %s, %s, %s);"

    cursor.execute(sql_query, form_values)
    conn.commit()
    cursor.close()
    conn.close()
    return  jsonify({"message": "Account created successfully"}),200


    #finally:
    cursor.close()
    conn.close()
  


"""
@app.route('/accounts', methods=['PUT'])
def update_account():
    # Update account record in the database
    # Connect to the database
    conn, cursor = database_connection()

    acc= input("Enter the account Number you would like to update ")
    sc=input("Enter sort code of the account you would like to update ")

    query= "SELECT * from accounts where account_num = acc;"
    cursor.execute(query)
    data = request.get_json()

    sort_code = data.get('sort_code')
    account_num = data.get('account_num')
    status_id = data.get('status_id')
    balance = data.get('balance')
    type_id = data.get('type_id')
    customer_id = data.get('customer_id')
    creation_date = data.get('creation_date') 
    
    
     # Validate required fields
    #if not all([sort_code, account_num, status_id, balance, type_id, customer_id, creation_date]):
     #   return jsonify({"error": "Missing required fields"}), 400
    
    query = 
    INSERT INTO accounts (sort_code, account_num, status_id, balance, type_id, customer_id, creation_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    
    values=(sort_code,account_num,status_id, balance,type_id,customer_id,creation_date)
    cursor.execute(query,values)
    conn.commit()
    return jsonify({"message": "Account added successfully"}), 201
    #except mysql.connector.Error as err:
       # conn.rollback()
       # return jsonify({"error": str(err)}), 500
    #finally:
    cursor.close()
    conn.close()    




"""

@app.route('/accounts', methods=['DELETE'])
def close_account():
    # Close an account
    pass
#changes account status to close.

@app.route('/transactions')
def get_transactions():
    # Return details of transactions
    pass

@app.route('/transactions', methods=['POST'])
def create_transaction():
    # Create a new transaction
    pass


#if __name__ == '__main__':
app.run(host="0.0.0.0", port=5001)
