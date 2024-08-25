customerDDL = """
CREATE TABLE customer
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
CREATE TABLE dates
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
CREATE TABLE supplier
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
CREATE TABLE part
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
CREATE TABLE lineorder
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


staticTableDDLs = {'customer': customerDDL, 'dates': datesDDL, 'supplier': supplierDDL, 'part': partDDL, 'lineorder': lineorderDDL}

customerColumns = "(c_custkey, c_name, c_address, c_city, c_nation, c_region, c_phone, c_mktsegment, supp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
datesColumns = "(d_datekey, d_date, d_dayofweek, d_month, d_year, d_yearmonthnum, d_yearmonth, d_daynuminweek, d_daynuminmonth, d_daynuminyear, d_monthnuminyear, d_weeknuminyear, d_sellingseason, d_lastdayinweekfl, d_lastdayinmonthfl, d_holidayfl, d_weekdayfl, supp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
supplierColumns = "(s_suppkey, s_name, s_address, s_city, s_nation, s_region, s_phone, supp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
partColumns = "(p_partkey, p_name, p_mfgr, p_category, p_brand, p_color, p_type, p_size, p_container, supp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
lineorderColumns = "(lo_orderkey, lo_linenumber, lo_custkey, lo_partkey, lo_suppkey, lo_orderdate, lo_orderpriority, lo_shippriority, lo_quantity, lo_extendedprice, lo_ordtotalprice, lo_discount, lo_revenue, lo_supplycost, lo_tax, lo_commitdate, lo_shipmode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

tableColumns = {'customer': customerColumns, 'dates': datesColumns, 'supplier': supplierColumns, 'part': partColumns, 'lineorder': lineorderColumns}

partitioningThreshold = {'customer': 100, 'dates': 100, 'supplier': 150, 'part': 150, 'lineorder': 200}