UPDATE lineorder
SET lo_supplycost = CASE 
    WHEN lo_supplycost > (SELECT MAX(lo_supplycost)  FROM lineorder) THEN lo_supplycost + 10
    ELSE lo_supplycost - 10
END
WHERE lo_orderkey = FLOOR(RANDOM() * 6000000);

