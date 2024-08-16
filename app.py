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
