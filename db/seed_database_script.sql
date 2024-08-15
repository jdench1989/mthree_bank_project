DROP TABLE IF EXISTS accounts_transactions;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS account_status;
DROP TABLE IF EXISTS transaction_type;
DROP TABLE IF EXISTS account_type;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS customer_status;


CREATE TABLE IF NOT EXISTS customer_status (status_id INT PRIMARY KEY, status VARCHAR(10));
CREATE TABLE IF NOT EXISTS customers (customer_id INT PRIMARY KEY AUTO_INCREMENT, status_id INT NOT NULL, last_name VARCHAR(45), first_name VARCHAR(45), dob DATE, email VARCHAR(150), phone VARCHAR(45), address VARCHAR(150), FOREIGN KEY (status_id) REFERENCES customer_status(status_id));
CREATE TABLE IF NOT EXISTS account_type (type_id INT PRIMARY KEY, type VARCHAR(45) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS transaction_type (type_id INT PRIMARY KEY, type VARCHAR(45) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS account_status (status_id INT PRIMARY KEY, status VARCHAR(20) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS accounts (account_id INT PRIMARY KEY  AUTO_INCREMENT, account_num VARCHAR(10) NOT NULL, sort_code VARCHAR(45) NOT NULL, type_id INT NOT NULL, status_id INT NOT NULL, balance FLOAT NOT NULL, creation_date DATETIME NOT NULL, customer_id INT UNIQUE, FOREIGN KEY (type_id) REFERENCES account_type(type_id), FOREIGN KEY (customer_id) REFERENCES customers(customer_id), FOREIGN KEY (status_id) REFERENCES account_status(status_id) );
CREATE TABLE IF NOT EXISTS transactions (transaction_id INT PRIMARY KEY AUTO_INCREMENT, type_id INT NOT NULL, account_from INT, account_to INT, transaction_time DATETIME NOT NULL, amount FLOAT NOT NULL,FOREIGN KEY (type_id) REFERENCES transaction_type(type_id));
CREATE TABLE IF NOT EXISTS accounts_transactions (account_id INT , transaction_id INT, PRIMARY KEY (account_id, transaction_id), FOREIGN KEY (account_id) REFERENCES accounts(account_id),FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id));

INSERT INTO transaction_type VALUES (1, "deposit"), (2, "withdrawal"), (3, "transfer");
INSERT INTO account_type VALUES (1, "current"), (2, "savings");
INSERT INTO account_status VALUES (1, "OPEN"), (2, "SUSPENDED"), (3, "CLOSED");
INSERT INTO customer_status VALUES (1, "ACTIVE"), (2, "INACTIVE");
INSERT INTO customers (status_id, last_name, first_name, dob, email, phone, address) VALUES (1, "Smith", "John", "2000-03-14", "johnsmith@gmail.com", "07777123123", "123 First Street, Anytown, Somecounty, AB12 3CD"), (1, "Doe", "Jane", "1998-06-23", "janedoe@yahoo.com", "07555987654", "456 Second Street, Here, There, CD32 1AB");
INSERT INTO accounts (account_num, sort_code, type_id, status_id, balance, creation_date, customer_id) VALUES ("12345678", "11-22-33", 1, 1, 1000.00, CURDATE(), 1), ("98765432", "44-55-66", 1, 1, 1345.54, CURDATE(), 2);

