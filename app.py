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
    # Return details of customers
    pass

@app.route('/customers', methods=['POST'])
def create_customer():
    # Create a new customer record in the database
    pass

@app.route('/customers', methods=['PUT'])
def update_customer():
    # Update a customer record in the database
    pass

@app.route('/customers', methods=['DELETE'])
def delete_customer():
    # Delete a customer record from the database
    # Allow for foreign key dependency issues
    pass

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
    sql_query = " INSERT INTO accounts ( account_id,account_num,sort_code,type_id,status_id,balance,creation_date,customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

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
