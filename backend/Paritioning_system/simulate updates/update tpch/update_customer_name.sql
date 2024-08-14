-- update_customer_name.sql
UPDATE customer
SET c_name = 'Customer' || FLOOR(RANDOM() * 10000)
WHERE c_custkey = FLOOR(RANDOM() * 10);  -- Randomly select a customer
