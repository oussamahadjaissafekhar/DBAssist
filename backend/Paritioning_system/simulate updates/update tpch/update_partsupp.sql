-- update_partsupp.sql
UPDATE partsupp
SET ps_availqty = ps_availqty + (RANDOM() * 50 - 25),  -- Random change between -25 and 25
    ps_supplycost = ps_supplycost + (RANDOM() * 5 - 2.5)  -- Random change between -2.5 and 2.5
WHERE ps_partkey = FLOOR(RANDOM() * 10) AND ps_suppkey = FLOOR(RANDOM() * 10);  -- Randomly select a partsupp
