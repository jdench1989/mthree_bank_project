from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db.database_connection import database_connection
import hashlib
import re
import os
from dotenv import load_dotenv
from tabulate import tabulate

# Load environment variables from .env file to local environment variables
load_dotenv()

app = Flask(__name__)  # Instantiate Flask
app.secret_key = os.environ["APP_SECRET_KEY"]  # Load secret key from environment variables

# Root endpoint automatically routed to http://localhost:5000/bank/home
@app.route('/')
def index():
    return redirect(url_for('home'))


# http://localhost:5000/bank/ - the following will be our login page, which will use both GET and POST requests
@app.route('/bank/', methods=['GET', 'POST'])
def login():
    conn, cursor = database_connection()
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# http://localhost:5000/bank/logout - this will be the logout page
@app.route('/bank/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/bank/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/bank/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        conn, cursor = database_connection()
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute(
                'INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()
            cursor.close()
            conn.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/bank/home - this will be the home page, only accessible for logged in users
@app.route('/bank/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/bank/profile - this will be the profile page, only accessible for logged in users
@app.route('/bank/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        conn, cursor = database_connection()
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))


@app.route('/customer')
def get_customers():  # Return details of all customers or search a specific customer
    conn, cursor = database_connection()  # Establish database connection
    sql_query = "SELECT * FROM customers"  # Base SQL query
    filters = []
    values = []

    # Check for query parameters
    # .../customer?customer_id=4
    customer_id = request.args.get('customer_id')
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

    cursor.execute(sql_query, values)  # Execute SQL query
    res = cursor.fetchall()  # Extract results
    cursor.close()
    conn.close()
    headers = [i[0] for i in cursor.description]
    table = f'<div class="content"><p>{tabulate(res, headers=headers, tablefmt="html")}</p></div>'
    return render_template('customer.html', table=table)


@app.route('/customer/new', methods=['GET', 'POST'])
def new_customer():  # Create a new customer record in the database
    if request.method == "GET":
        return render_template('customer_new.html')
    elif request.method == 'POST':
        conn, cursor = database_connection()  # Establish database connection

        # Extract form data
        form_values = ['OPEN']
        for key in request.form:
            form_values.append(request.form[key])

        # SQL query using placeholders
        sql_query = "INSERT INTO customers (status, last_name, first_name, dob, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        cursor.execute(sql_query, form_values)  # Execute SQL query
        conn.commit()
        customer_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return redirect(url_for('get_customers', customer_id=customer_id))


@app.route('/customer/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def modify_customer(customer_id):  # Update a customer record in the database
    if request.method == 'GET':
        return render_template('customer_modify.html', customer_id=customer_id)
    
    elif request.method == 'PUT':
        # Extract columns and values to be updated from the request JSON
        form_values = []
        for key in request.form:
            form_values.append(request.form[key])

        # Compile columns and values into a SQL query using placeholders
        sql_query = """UPDATE customers SET 
        status = %s, last_name = %s, first_name = %s, dob = %s, email = %s, phone = %s, address = %s
        WHERE customer_id = %s;
        """
        form_values.append(customer_id)
        conn, cursor = database_connection()  # Establish database connection
        cursor.execute(sql_query, form_values)  # Execute the query
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_customers', customer_id=customer_id))
    
    elif request.method == "DELETE":
        conn, cursor = database_connection()  # Establish database connection

        # Check the database to see if the provided customer has an associated account
        cursor.execute(
            "SELECT account_id FROM accounts WHERE customer_id = %s LIMIT 1;", [customer_id])
        account_record = cursor.fetchone()  # Fetch the first result if it exists

        res = {}
        if account_record:  # Check if account_record is not None
            res["success"] = "false"
            res["message"] = "Customer cannot be deleted. Customer record is associated with an account record. Deactivate customer instead."
        else:  # If there is no account record then the customer can be safely deleted
            cursor.execute(
                "DELETE FROM customers WHERE customer_id = %s", [customer_id])
            res["success"] = "true"
            res["message"] = "Customer record deleted successfully."
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('customer_modify.html', res=res)


@app.route('/accounts')
def get_accounts():
    # Establish database connection
    conn, cursor = database_connection()

    # Base SQL query
    sql_query = "SELECT * FROM accounts"
    filters = []
    values = []

    # check for query parameters
    sort_code = request.args.get('sort_code')
    account_id = request.args.get('account_id')
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

    # Add filters to SQL query if there are any
    if filters:
        sql_query += " WHERE " + " AND ".join(filters)

    # Execute the SQL sqlQuery
    cursor.execute(sql_query, values)
    res = cursor.fetchall()

    # close cursor and connection
    cursor.close()
    conn.close()

    return jsonify(res), 200


@app.route('/accounts', methods=['POST'])
def create_account():
    # Connect to the database
    conn, cursor = database_connection()

    # Extract form data
    form_values = []
    for key in request.form:
        form_values.append(request.form[key])

    # SQL query using placeholders
    sql_query = "INSERT INTO accounts (account_num, sort_code, type_id, status, balance, customer_id) VALUES (%s, %s, %s, %s, %s, %s);"

    cursor.execute(sql_query, form_values)  # Execute SQL query
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Account created successfully"}), 200


@app.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    conn, cursor = database_connection()  # Establish database connection
    # Extract columns and values to be updated from the request JSON
    # data = request.get_json()
    status = request.form.get('status')

    # check if status is provided in request
    if not status:
        return jsonify({"error : missing 'status' field"}), 400

    # execute the query
    try:
        sql_query = "UPDATE accounts SET status = %s WHERE account_id = %s"
        cursor.execute(sql_query, (status, account_id))
        conn.commit()
        return jsonify({"message": "account status updated successfully"}), 200

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
    # .../customers?customer_id=4
    customer_id = request.args.get('customer_id')
    account_id = request.args.get('account_id')
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
    if account_id:
        filters.append("a.account_id = %s")
        values.append(account_id)
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

    cursor.execute(sql_query, values)  # Execute SQL query
    res = cursor.fetchall()  # Extract results
    cursor.close()
    conn.close()
    return jsonify(res), 200


@app.route('/transactions', methods=['POST'])
def create_transaction():
    # Create a new transaction
    conn, cursor = database_connection()  # Establish database connection

    # Extract form data
    form_columns = []
    form_values = []
    for key, value in request.form.items():
        form_columns.append(key)
        form_values.append(value)

    try:
        # SQL query using placeholders
        sql_query = "INSERT INTO transactions ("
        sql_query += ", ".join(form_columns)  # Add column names
        sql_query += ") VALUES ("
        sql_query += ", ".join(["%s"] * len(form_values))  # Add placeholders
        sql_query += ")"

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
