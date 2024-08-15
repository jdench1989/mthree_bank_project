CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE account_from_status VARCHAR(20);
    DECLARE account_to_status VARCHAR(20);
    DECLARE account_from_balance FLOAT;
    DECLARE account_to_balance FLOAT;
    DECLARE open_status_id INT;

    -- Get the status ID for 'OPEN'
    SELECT status_id INTO open_status_id
    FROM account_status
    WHERE status = 'OPEN'
    LIMIT 1;

    -- Check the status and balance of account_from
    IF NEW.account_from IS NOT NULL THEN
        SELECT a_s.status, a.balance INTO account_from_status, account_from_balance
        FROM accounts a
        JOIN account_status a_s ON a.status_id = a_s.status_id
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

    -- Check the status and balance of account_to
    IF NEW.account_to IS NOT NULL THEN
        SELECT a_s.status, a.balance INTO account_to_status, account_to_balance
        FROM accounts a
        JOIN account_status a_s ON a.status_id = a_s.status_id
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

END;

