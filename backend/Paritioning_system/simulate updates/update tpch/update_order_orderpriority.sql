UPDATE orders
SET o_orderpriority = CASE o_orderpriority
    WHEN '5-NONE' THEN '2-HIGH'
    WHEN '2-HIGH' THEN '1-URGENT'
    when '1-URGENT' THEN '5-NONE'
    ELSE o_orderpriority
END
WHERE o_orderkey = FLOOR(RANDOM() * 10)  -- Randomly select an order