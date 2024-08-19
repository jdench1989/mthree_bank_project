
INSERT INTO transaction_type VALUES (1, "deposit"), (2, "withdrawal"), (3, "transfer");
INSERT INTO account_type VALUES (1, "current"), (2, "savings");
INSERT INTO customers (status, last_name, first_name, dob, email, phone, address) VALUES 
    ("ACTIVE", "Peralta", "Jake", "2000-03-14", "jakeperalta@gmail.com", "07777123123", "123 First Street, Anytown, Somecounty, AB12 3CD"), 
    ("ACTIVE", "Holt", "Raymond", "1998-06-23", "raymondholt@yahoo.com", "07555987654", "456 Second Street, Here, There, CD32 1AB"), 
    ("INACTIVE", "Santiago", "Amy", "2004-03-12", "amysantiago@msn.com", "07123456789", "789 Third Street, Somewhere, Nowhere, EF45 6GH"),
    ("ACTIVE", "Boyle", "Charles", "1989-10-30", "charlesboyle@icloud.com", "07987654321", "121a Fourth Street, Thisville, Thatcounty, XY34 Z56");
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
INSERT INTO users (id, username, password, email) VALUES 
    (1, 'test', 'aa689352e9dc50fb43b1e3428db0af42ed9186b9', 'test@test.com');