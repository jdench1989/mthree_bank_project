CREATE DATABASE IF NOT EXISTS bank;
USE bank;

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
    customer_id INT NOT NULL, 
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

CREATE TABLE IF NOT EXISTS users (
	id int(11) NOT NULL AUTO_INCREMENT,
  	username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
  	email varchar(100) NOT NULL,
    PRIMARY KEY (id)
);

DELIMITER //
CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE account_from_status VARCHAR(20);
    DECLARE account_to_status VARCHAR(20);
    DECLARE account_from_balance FLOAT;

    -- Check the status and balance of account_from
    IF NEW.account_from IS NOT NULL THEN
        SELECT a.status, a.balance INTO account_from_status, account_from_balance
        FROM accounts a
        WHERE a.account_id = NEW.account_from;

        IF account_from_status != 'OPEN' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'account_from does not exist or is not OPEN';
        END IF;

        IF account_from_balance < NEW.amount THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'account_from does not have a sufficient balance';
        END IF;

        -- Deduct the amount from account_from
        UPDATE accounts
        SET balance = balance - NEW.amount
        WHERE account_id = NEW.account_from;
    END IF;

    -- Check the status of account_to
    IF NEW.account_to IS NOT NULL THEN
        SELECT a.status INTO account_to_status
        FROM accounts a
        WHERE a.account_id = NEW.account_to;

        IF account_to_status != 'OPEN' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'account_to does not exist or is not OPEN';
        END IF;

        -- Add the amount to account_to
        UPDATE accounts
        SET balance = balance + NEW.amount
        WHERE account_id = NEW.account_to;
    END IF;

    -- Insert into accounts_transactions bridge table
    IF NEW.account_from IS NOT NULL THEN
        INSERT INTO accounts_transactions (account_id, transaction_id)
        VALUES (NEW.account_from, NEW.transaction_id);
    END IF;

    IF NEW.account_to IS NOT NULL THEN
        INSERT INTO accounts_transactions (account_id, transaction_id)
        VALUES (NEW.account_to, NEW.transaction_id);
    END IF;

END//

DELIMITER ;

INSERT INTO transaction_type VALUES (1, "deposit"), (2, "withdrawal"), (3, "transfer");
INSERT INTO account_type VALUES (1, "current"), (2, "savings");
INSERT INTO customers (status, last_name, first_name, dob, email, phone, address) VALUES 
    ("ACTIVE", "Peralta", "Jake", "2000-03-14", "jakeperalta@gmail.com", "07777123123", "123 First Street, Anytown, Somecounty, AB12 3CD"), 
    ("ACTIVE", "Holt", "Raymond", "1998-06-23", "raymondholt@yahoo.com", "07555987654", "456 Second Street, Here, There, CD32 1AB"), 
    ("INACTIVE", "Santiago", "Amy", "2004-03-12", "amysantiago@msn.com", "07123456789", "789 Third Street, Somewhere, Nowhere, EF45 6GH"),
    ("ACTIVE", "Boyle", "Charles", "1989-10-30", "charlesboyle@icloud.com", "07987654321", "121a Fourth Street, Thisville, Thatcounty, XY34 Z56"),
    ("ACTIVE", "Jeffords", "Terry", "1989-12-11", "email@email.com", "07162983068", "121b Fourth Street, Thisville, Thatcounty, XY34 Z56");
INSERT INTO accounts (account_num, sort_code, type_id, status, balance, creation_date, customer_id) VALUES 
    ("12345678", "11-22-33", 1, "OPEN", 1000.00, CURTIME(), 1), 
    ("98765432", "44-55-66", 1, "OPEN", 1345.54, CURTIME(), 2),
    ("65927384", "55-66-77", 2, "OPEN", 2000000.23, CURTIME(), 2),
    ("91836498", "12-34-56", 1, "OPEN", 128.02, CURTIME(), 1),
    ("01736592", "11-22-33", 1, "CLOSED", 00.00, CURTIME(), 3),
    ("92736492", "11-22-33", 2, "CLOSED", 00.00, CURTIME(), 3),
    ("91725364", "44-55-66", 1, "OPEN", 8000.43, CURTIME(), 4);
INSERT INTO transactions (type_id, account_from, account_to, transaction_time, amount) VALUES
    (1, NULL, 1, CURTIME(), 100.00),
    (2, 7, NULL, CURTIME(), 123.00),
    (3, 3, 2, CURTIME(), 100000.00);
