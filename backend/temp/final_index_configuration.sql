CREATE INDEX idx_lineorder_lo_custkey ON lineorder (lo_custkey);
CREATE INDEX idx_customer_c_custkey ON customer (c_custkey);
CREATE INDEX idx_lineorder_lo_orderdate ON lineorder (lo_orderdate);
CREATE INDEX idx_dates_d_datekey ON dates (d_datekey);