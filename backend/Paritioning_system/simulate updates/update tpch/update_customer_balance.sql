UPDATE customer
SET c_acctbal = c_acctbal + (RANDOM() * 100 - 50)  -- Random change between -50 and 50
WHERE c_custkey = FLOOR(RANDOM() * 10);  -- Randomly select a customer