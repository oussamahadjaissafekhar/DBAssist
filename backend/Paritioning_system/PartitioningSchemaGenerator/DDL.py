customerDDL = """
CREATE TABLE customer_partitioned
(
    c_custkey integer NOT NULL,
    c_name character varying(25) NOT NULL,
    c_address character varying(40) NOT NULL,
    c_city character(11) NOT NULL,
    c_nation character(16) NOT NULL,
    c_region character(16) NOT NULL,
    c_phone character(16) NOT NULL,
    c_mktsegment character(11) NOT NULL,
    supp character(1)  
)
"""

datesDDL = """
CREATE TABLE dates_partitioned
(
    d_datekey integer NOT NULL,
    d_date character(19) NOT NULL,
    d_dayofweek character(16) NOT NULL,
    d_month character(10) NOT NULL,
    d_year integer NOT NULL,
    d_yearmonthnum integer NOT NULL,
    d_yearmonth character(8) NOT NULL,
    d_daynuminweek integer NOT NULL,
    d_daynuminmonth integer NOT NULL,
    d_daynuminyear integer NOT NULL,
    d_monthnuminyear integer NOT NULL,
    d_weeknuminyear integer NOT NULL,
    d_sellingseason character(13) NOT NULL,
    d_lastdayinweekfl boolean NOT NULL,
    d_lastdayinmonthfl boolean NOT NULL,
    d_holidayfl boolean NOT NULL,
    d_weekdayfl boolean NOT NULL,
    supp character(1)   
)
"""

supplierDDL = """
CREATE TABLE supplier_partitioned
(
    s_suppkey integer NOT NULL,
    s_name character(25) NOT NULL,
    s_address character varying(40) NOT NULL,
    s_city character(11) NOT NULL,
    s_nation character(16) NOT NULL,
    s_region character(16) NOT NULL,
    s_phone character(16) NOT NULL,
    supp character(1) 
)
"""

partDDL = """
CREATE TABLE part_partitioned
(
    p_partkey integer NOT NULL,
    p_name character varying(50) NOT NULL,
    p_mfgr character(26) NOT NULL,
    p_category character(11) NOT NULL,
    p_brand character(10) NOT NULL,
    p_color character varying(11) NOT NULL,
    p_type character varying(26) NOT NULL,
    p_size integer NOT NULL,
    p_container character(11) NOT NULL,
    supp character(1) 
)
"""

lineorderDDL = """
CREATE TABLE lineorder_partitioned
(
    lo_orderkey integer,
    lo_linenumber integer,
    lo_custkey integer,
    lo_partkey integer,
    lo_suppkey integer,
    lo_orderdate integer,
    lo_orderpriority character(15),
    lo_shippriority character(1),
    lo_quantity integer,
    lo_extendedprice integer,
    lo_ordtotalprice integer,
    lo_discount integer,
    lo_revenue integer,
    lo_supplycost integer,
    lo_tax integer,
    lo_commitdate integer,
    lo_shipmode character(11)
)
"""


tableDDLs = {'customer': customerDDL, 'dates': datesDDL, 'supplier': supplierDDL, 'part': partDDL, 'lineorder': lineorderDDL}