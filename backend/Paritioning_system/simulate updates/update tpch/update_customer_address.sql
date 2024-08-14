-- update_customer_address.sql
UPDATE customer
SET c_address = 'St ' || FLOOR(RANDOM() * 100) || 'City ' || FLOOR(RANDOM() * 100)
WHERE c_custkey = FLOOR(RANDOM() * 10);  -- Randomly select a customer
