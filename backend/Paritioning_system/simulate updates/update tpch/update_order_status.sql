-- update_order_status.sql
UPDATE orders
SET o_orderstatus = CASE o_orderstatus
    WHEN 'O' THEN 'F'
    WHEN 'F' THEN 'P'
    WHEN 'P' THEN 'O'
    ELSE 'O'
END
WHERE o_orderkey = FLOOR(RANDOM() * 10);  -- Randomly select an order
