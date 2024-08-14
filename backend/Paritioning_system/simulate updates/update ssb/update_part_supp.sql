UPDATE part
SET supp = CASE p_partkey % 2
    WHEN 0 THEN 'E'
    WHEN 1 THEN 'O'
END
WHERE p_partkey = FLOOR(RANDOM() * 1400000);
