UPDATE lineorder
SET lo_quantity = (lo_quantity + 1) % 51
WHERE lo_orderkey = FLOOR(RANDOM() * 6000000);
