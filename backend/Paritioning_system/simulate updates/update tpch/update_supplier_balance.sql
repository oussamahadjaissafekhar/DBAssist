-- update_supplier_balance.sql
UPDATE supplier
SET s_acctbal = s_acctbal + (RANDOM() * 100 - 50)  -- Random change between -50 and 50
WHERE s_suppkey = FLOOR(RANDOM() * 10);  -- Randomly select a supplier
