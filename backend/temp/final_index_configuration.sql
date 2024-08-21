CREATE INDEX idx_lineorder_lo_custkey ON lineorder (lo_custkey);
CREATE INDEX idx_customer_c_custkey ON customer (c_custkey);
CREATE INDEX idx_lineorder_lo_suppkey ON lineorder (lo_suppkey);
CREATE INDEX idx_supplier_s_suppkey ON supplier (s_suppkey);
CREATE INDEX idx_lineorder_lo_partkey ON lineorder (lo_partkey);
CREATE INDEX idx_part_p_partkey ON part (p_partkey);
CREATE INDEX idx_lineorder_lo_orderdate ON lineorder (lo_orderdate);