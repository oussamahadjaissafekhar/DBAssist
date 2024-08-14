-- update_lineitem_status.sql
UPDATE lineitem
SET l_linestatus = CASE l_linestatus
    WHEN 'O' THEN 'F'
    WHEN 'F' THEN 'O'
    ELSE 'O'
END
WHERE l_orderkey = FLOOR(RANDOM() * 10) AND l_linenumber = FLOOR(RANDOM() * 10);  -- Randomly select a line item
