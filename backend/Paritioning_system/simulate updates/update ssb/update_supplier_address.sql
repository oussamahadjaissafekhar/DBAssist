UPDATE supplier
SET s_address = 'P.O.B N ' || FLOOR(RANDOM() * 25) || 'St N ' || FLOOR(RANDOM() * 1000)
WHERE s_suppkey = FLOOR(RANDOM() * 200000);
