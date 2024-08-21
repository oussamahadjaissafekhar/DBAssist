CREATE INDEX idx_lineorder_lo_suppkey ON lineorder (lo_suppkey);
CREATE INDEX idx_supplier_s_suppkey ON supplier (s_suppkey);
CREATE INDEX idx_lineorder_lo_partkey ON lineorder (lo_partkey);
CREATE INDEX idx_part_p_partkey ON part (p_partkey);
CREATE INDEX idx_part_p_category ON part (p_category);
CREATE INDEX idx_lineorder_lo_custkey ON lineorder (lo_custkey);