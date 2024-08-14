-- update_part_price.sql
UPDATE part
SET p_retailprice = p_retailprice + (RANDOM() * 10 - 5)  -- Random change between -5 and 5
WHERE p_partkey = FLOOR(RANDOM() * 10);  -- Randomly select a part
