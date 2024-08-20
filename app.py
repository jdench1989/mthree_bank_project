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
@app.route('/login', methods=['GET', 'POST'])
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
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


# http://localhost:5000/bank/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/bank/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
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
@app.route('/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/bank/profile - this will be the profile page, only accessible for logged in users
@app.route('/profile')
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
def get_customers():
    conn, cursor = database_connection()
    sql_query = "SELECT * FROM customers"
    
    # Mapping query parameters to SQL conditions
    filters = {
        'customer_id': 'customer_id = %s',
        'first_name': 'first_name LIKE %s',
        'last_name': 'last_name LIKE %s',
        'email': 'email LIKE %s'
    }
    
    # Generate WHERE clause and values without using zip
    conditions = []
    values = []

    for key, value in request.args.items():
        if key in filters:
            conditions.append(filters[key])
            values.append(f"%{value}%" if 'LIKE' in filters[key] else value)

    # Append conditions to the SQL query
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql_query, values)
    res = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    
    cursor.close()
    conn.close()
    
    table = f'<div class="content"><p>{tabulate(res, headers=headers, tablefmt="html")}</p></div>'
    return render_template('customer.html', table=table)

@app.route('/customer/search', methods=['GET'])
def search_customers():
    return render_template('customer_search.html')

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


@app.route('/account')
def get_accounts():
    conn, cursor = database_connection()
    sql_query = "SELECT * FROM accounts"
    
    # Mapping query parameters to SQL conditions
    filters = {
        'account_id': 'account_id = %s',
        'sort_code': 'sort_code = %s',
        'account_num': 'account_num = %s',
        'status': 'status = %s',
        'balance': 'balance = %s',
        'type_id': 'type_id = %s',
        'customer_id': 'customer_id = %s',
        'creation_date': 'creation_date = %s'
    }
    
    # Generate WHERE clause and values without using zip
    conditions = []
    values = []

    for key, value in request.args.items():
        if key in filters:
            conditions.append(filters[key])
            values.append(value)

    # Append conditions to the SQL query
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql_query, values)
    res = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    
    cursor.close()
    conn.close()
    
    table = f'<div class="content"><p>{tabulate(res, headers=headers, tablefmt="html")}</p></div>'
    return render_template('account.html', table=table)



@app.route('/account/new', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('account_new.html')
    elif request.method == 'POST':

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
        account_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return redirect(url_for('get_accounts', account_id=account_id))


@app.route('/account/<account_id>', methods=['GET', 'PUT'])
def update_account(account_id):
    if request.method == 'GET':
        return render_template('account_modify.html', account_id=account_id)
    elif request.method == "PUT":
        conn, cursor = database_connection()  # Establish database connection
        status = request.form.get('status')
        sql_query = "UPDATE accounts SET status = %s WHERE account_id = %s"
        cursor.execute(sql_query, (status, account_id))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template(url_for('get_accounts', account_id=account_id))


@app.route('/transaction')
def get_transactions():
    conn, cursor = database_connection()
    sql_query = """SELECT * FROM customers c
                   INNER JOIN accounts a ON c.customer_id = a.customer_id
                   INNER JOIN accounts_transactions a_tr ON a_tr.account_id = a.account_id
                   INNER JOIN transactions t ON a_tr.transaction_id = t.transaction_id"""
    
    # Mapping query parameters to SQL conditions
    filters = {
        'customer_id': 'c.customer_id = %s',
        'account_id': 'a.account_id = %s',
        'first_name': 'c.first_name LIKE %s',
        'last_name': 'c.last_name LIKE %s',
        'account_num': 'a.account_num = %s',
        'sort_code': 'a.sort_code = %s',
        'transaction_time_earliest': 'date(t.transaction_time) >= %s',
        'transaction_time_latest': 'date(t.transaction_time) <= %s'
    }
    
    # Generate WHERE clause and values without using zip
    conditions = []
    values = []

    for key, value in request.args.items():
        if key in filters:
            conditions.append(filters[key])
            # Adjust value formatting for LIKE queries
            if 'LIKE' in filters[key]:
                values.append(f"%{value}%")
            else:
                values.append(value)

    # Append conditions to the SQL query
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql_query, values)
    res = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    
    cursor.close()
    conn.close()
    
    table = f'<div class="content"><p>{tabulate(res, headers=headers, tablefmt="html")}</p></div>'
    return render_template('transaction.html', table=table)



@app.route('/transaction/new', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'GET':
        return render_template('transaction_new.html')
    
    if request.method == 'POST':
        # Establish database connection
        conn, cursor = database_connection()

        # Extract form data
        form_data = request.form.to_dict()
        columns = ', '.join(form_data.keys())
        placeholders = ', '.join(['%s'] * len(form_data))
        values = list(form_data.values())

        # SQL query
        sql_query = f"INSERT INTO transactions ({columns}) VALUES ({placeholders})"
        
        # Execute SQL query
        cursor.execute(sql_query, values)
        conn.commit()
        transaction_id = cursor.lastrowid
        
        # Clean up
        cursor.close()
        conn.close()

        return redirect(url_for('get_transactions', transaction_id=transaction_id))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
