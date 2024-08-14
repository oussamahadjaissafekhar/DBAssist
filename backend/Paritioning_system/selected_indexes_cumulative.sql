CREATE INDEX lineorder_lo_orderdate ON lineorder(lo_orderdate);
CREATE INDEX dates_d_datekey ON dates(d_datekey);
CREATE INDEX lineorder_lo_suppkey ON lineorder(lo_suppkey);
CREATE INDEX supplier_s_suppkey ON supplier(s_suppkey);
CREATE INDEX lineorder_lo_custkey ON lineorder(lo_custkey);
CREATE INDEX customer_c_custkey ON customer(c_custkey);
