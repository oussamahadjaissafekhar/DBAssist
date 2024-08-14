UPDATE lineorder
SET lo_orderpriority = CASE lo_orderpriority
    WHEN '1-URGENT' THEN '2-HIGH'
    WHEN '2-HIGH' THEN '3-MEDIUM'
    WHEN '3-MEDIUM' THEN '4-NOT SPECI'
    WHEN '4-NOT SPECI'THEN '5-LOW'
    WHEN '5-LOW'THEN '1-URGENT'
    end
WHERE lo_orderkey = FLOOR(RANDOM() * 6000000);