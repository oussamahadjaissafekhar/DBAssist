UPDATE customer
SET c_phone = FLOOR(RANDOM() * 100) || '-' || FLOOR(RANDOM() * 1000) || '-' || FLOOR(RANDOM() * 1000) || '-' || FLOOR(RANDOM() * 10000)
WHERE c_custkey = FLOOR(RANDOM() * 3000000); 

