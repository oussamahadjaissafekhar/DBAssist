UPDATE lineorder
SET lo_shipmode = CASE lo_shipmode
    WHEN 'AIR|' THEN 'TRUCK|'
    WHEN 'TRUCK|' THEN 'SHIP|'
    WHEN 'SHIP|' THEN 'REG AIR|'
    WHEN 'REG AIR|'THEN 'RAIL|'
    WHEN 'RAIL|'THEN 'MAIL|'
    WHEN 'MAIL|'THEN 'FOB|'
    WHEN 'FOB|'THEN 'AIR|'
    end
WHERE lo_orderkey = FLOOR(RANDOM() * 6000000);
