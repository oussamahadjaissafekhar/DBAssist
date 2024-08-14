UPDATE lineorder
SET lo_discount = (lo_discount + 1) % 11
WHERE lo_orderkey = FLOOR(RANDOM() * 6000000);