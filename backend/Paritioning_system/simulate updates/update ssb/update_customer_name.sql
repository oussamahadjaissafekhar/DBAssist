UPDATE customer
SET c_name = 'Customer' || c_custkey
WHERE c_custkey = FLOOR(RANDOM() * 3000000);
