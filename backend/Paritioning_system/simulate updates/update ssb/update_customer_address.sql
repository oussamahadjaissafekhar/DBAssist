UPDATE customer
SET c_address = 'P.O Box N ' || FLOOR(RANDOM() * 25) || 'St N ' || FLOOR(RANDOM() * 1000)
WHERE c_custkey = FLOOR(RANDOM() * 3000000);

