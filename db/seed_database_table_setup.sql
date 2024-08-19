DROP TABLE IF EXISTS accounts_transactions;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS transaction_type;
DROP TABLE IF EXISTS account_type;
DROP TABLE IF EXISTS customers;

DROP TRIGGER IF EXISTS after_transaction_insert;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT, 
    status VARCHAR(10) NOT NULL, 
    last_name VARCHAR(45), 
    first_name VARCHAR(45), 
    dob DATE, 
    email VARCHAR(150), 
    phone VARCHAR(45), 
    address VARCHAR(150));
CREATE TABLE IF NOT EXISTS account_type (
    type_id INT PRIMARY KEY, 
    type VARCHAR(45) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS transaction_type (
    type_id INT PRIMARY KEY, 
    type VARCHAR(45) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT PRIMARY KEY  AUTO_INCREMENT, 
    account_num VARCHAR(10) NOT NULL, 
    sort_code VARCHAR(45) NOT NULL, 
    type_id INT NOT NULL, 
    status VARCHAR(10) NOT NULL, 
    balance FLOAT NOT NULL, 
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    customer_id INT, 
    FOREIGN KEY (type_id) REFERENCES account_type(type_id), 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id));
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT, 
    type_id INT NOT NULL, 
    account_from INT, 
    account_to INT, 
    transaction_time DATETIME DEFAULT CURRENT_TIMESTAMP, 
    amount FLOAT NOT NULL, 
    FOREIGN KEY (type_id) REFERENCES transaction_type(type_id));
CREATE TABLE IF NOT EXISTS accounts_transactions (
    account_id INT, 
    transaction_id INT, 
    PRIMARY KEY (account_id, transaction_id), 
    FOREIGN KEY (account_id) REFERENCES accounts(account_id), 
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id));
