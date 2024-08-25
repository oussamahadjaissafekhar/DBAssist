SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'EUROPE' AND s_nation = 'EUROPE' AND d_year >= 1992 AND d_year <= 1993 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'ROMANIA  1' OR c_city = 'ROMANIA  1') AND (s_city = 'ROMANIA  1' OR s_city = 'ROMANIA  1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'MIDDLE EAST' AND s_nation = 'MIDDLE EAST' AND d_year >= 1994 AND d_year <= 1995 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND (c_city = 'VIETNAM  1' OR c_city = 'VIETNAM  1') AND (s_city = 'VIETNAM  1' OR s_city = 'VIETNAM  1') AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'UNITED ST1' OR c_city = 'UNITED ST1') AND (s_city = 'UNITED ST1' OR s_city = 'UNITED ST1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'ETHIOPIA 1' OR c_city = 'ETHIOPIA 1') AND (s_city = 'ETHIOPIA 1' OR s_city = 'ETHIOPIA 1') GROUP BY c_city, s_city, d_year;
SELECT c_nation, s_nation, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'MIDDLE EAST' AND s_region = 'AMERICA' AND d_year >= 1991 AND d_year <= 1992 GROUP BY c_nation, s_nation, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'AFRICA' AND s_nation = 'AFRICA' AND d_year >= 1992 AND d_year <= 1993 GROUP BY c_city, s_city, d_year;
SELECT COUNT(*) FROM part where p_brand BETWEEN 'MFGR#243 ' AND 'MFGR#2520';
SELECT COUNT(*) FROM part WHERE p_brand >= 'MFGR#1220' OR p_brand = 'MFGR#2140' and p_category = 'MFGR#53';
SELECT COUNT(*) FROM part WHERE p_brand < 'MFGR#2123' OR p_brand = 'MFGR#231 ';
SELECT COUNT(*) FROM part WHERE p_brand = 'MFGR#1433' OR p_brand = 'MFGR#3121' OR p_mfgr <= 'MFGR#5' and p_category <= 'MFGR#54';
SELECT COUNT(*) FROM part WHERE p_brand > 'MFGR#1233' OR p_brand = 'MFGR#333 ' AND p_mfgr >= 'MFGR#2';
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'CHINA    1' OR c_city = 'CHINA    1') AND (s_city = 'CHINA    1' OR s_city = 'CHINA    1') GROUP BY c_city, s_city, d_year;
SELECT c_nation, s_nation, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AMERICA' AND s_region = 'MIDDLE EAST' AND d_year >= 1991 AND d_year <= 1992 GROUP BY c_nation, s_nation, d_year;
SELECT c_nation, s_nation, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AMERICA' AND s_region = 'MIDDLE EAST' AND d_year >= 1994 AND d_year <= 1995 GROUP BY c_nation, s_nation, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'ARGENTINA1' OR c_city = 'ARGENTINA1') AND (s_city = 'ARGENTINA1' OR s_city = 'ARGENTINA1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND (c_city = 'FRANCE   1' OR c_city = 'FRANCE   1') AND (s_city = 'FRANCE   1' OR s_city = 'FRANCE   1') AND d_year >= 1994 AND d_year <= 1995 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'MIDDLE EAST' AND s_nation = 'MIDDLE EAST' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_city, s_city, d_year;
SELECT COUNT(*) FROM part WHERE p_brand = 'MFGR#1115' OR p_brand = 'MFGR#153 ' AND p_category = 'MFGR#43';
SELECT COUNT(*) FROM part where p_brand <= 'MFGR#4127' AND p_brand >= 'MFGR#3531'
SELECT COUNT(*) FROM part where p_brand <= 'MFGR#557 ' OR p_brand = 'MFGR#5540'
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'JAPAN    1' OR c_city = 'JAPAN    1') AND (s_city = 'JAPAN    1' OR s_city = 'JAPAN    1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'CANADA   1' OR c_city = 'CANADA   1') AND (s_city = 'CANADA   1' OR s_city = 'CANADA   1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city = 'KENYA    1' OR c_city = 'KENYA    1') AND (s_city = 'KENYA    1' OR s_city = 'KENYA    1') GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND (c_city = 'BRAZIL   1' OR c_city = 'BRAZIL   1') AND (s_city = 'BRAZIL   1' OR s_city = 'BRAZIL   1') AND d_year >= 1995 AND d_year <= 1996 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND (c_city = 'CANADA   1' OR c_city = 'CANADA   1') AND (s_city = 'CANADA   1' OR s_city = 'CANADA   1') AND d_year >= 1991 AND d_year <= 1992 GROUP BY c_city, s_city, d_year;
SELECT sum(lo_revenue) AS revenue FROM lineorder, dates WHERE lo_orderdate = d_datekey AND d_weeknuminyear = 40 AND d_year = 1992 AND lo_discount > 2 AND lo_discount < 4 AND lo_quantity > 38 AND lo_quantity < 40;
SELECT sum(lo_revenue) AS revenue FROM lineorder, dates WHERE lo_orderdate = d_datekey AND d_weeknuminyear = 30 AND d_year = 1998 AND lo_discount > 2 AND lo_discount < 4 AND lo_quantity > 38 AND lo_quantity < 40;
SELECT sum(lo_revenue) AS revenue FROM lineorder, dates WHERE lo_orderdate = d_datekey AND lo_discount > 2 AND lo_discount < 4 AND lo_quantity > 38 AND lo_quantity < 40;
SELECT sum(lo_revenue) AS revenue FROM lineorder, dates WHERE lo_orderdate = d_datekey AND d_weeknuminyear = 40 AND d_year = 1995 AND lo_discount > 2 AND lo_discount < 4 AND lo_quantity > 28 AND lo_quantity < 30;    
SELECT sum(lo_revenue) AS revenue FROM lineorder, dates WHERE lo_orderdate = d_datekey AND d_year = 1996 AND lo_discount > 2 AND lo_discount < 4 AND lo_quantity < 0;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0', 'INDONESIA0', 'IRAN     0', 'IRAQ     0', 'JAPAN    0', 'JORDAN   0' )) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0', 'INDONESIA0', 'IRAN     0', 'IRAQ     0', 'JAPAN    0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0', 'INDONESIA0', 'IRAN     0', 'IRAQ     0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0', 'INDONESIA0', 'IRAN     0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0', 'INDONESIA0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0', 'INDIA    0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0', 'GERMANY  0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0', 'FRANCE   0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0', 'ETHIOPIA 0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0', 'EGYPT    0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0', 'CHINA    0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0', 'BRAZIL   0')) GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, sum(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND (c_city IN ('ALGERIA  0', 'ARGENTINA0')) GROUP BY c_city, s_city, d_year;
SELECT sum(lo_revenue) AS lo_revenue, d_year FROM lineorder, dates, supplier WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND s_region = 'EUROPE'   GROUP BY d_year;
SELECT sum(lo_revenue) AS lo_revenue, d_year FROM lineorder, dates, supplier WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND s_region = 'EUROPE'  GROUP BY d_year;
SELECT sum(lo_revenue) AS lo_revenue, d_year FROM lineorder, dates, supplier WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND s_region = 'AMERICA' GROUP BY d_year;
SELECT sum(lo_revenue) AS lo_revenue, d_year FROM lineorder, dates, supplier WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND s_region = 'AFRICA' GROUP BY d_year;
SELECT sum(lo_revenue) AS lo_revenue, d_year FROM lineorder, dates, supplier WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND s_region = 'AFRICA' GROUP BY d_year;
SELECT d_year, s_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_region = 'AMERICA' AND (d_year = 1992 OR d_year = 1993) GROUP BY d_year, s_nation;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'EUROPE' AND (d_year = 1993 OR d_year = 1991);
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'AMERICA' AND (d_year = 1992 OR d_year = 1993);
SELECT d_year, s_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'EUROPE' AND (d_year = 1993 OR d_year = 1994) GROUP BY d_year, s_nation;
SELECT d_year, s_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'AMERICA' AND (d_year = 1992 OR d_year = 1993) GROUP BY d_year, s_nation;
SELECT d_year, s_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'MIDDLE EAST' AND (d_year = 1992 OR d_year = 1993) GROUP BY d_year, s_nation;
SELECT d_year, s_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'AFRICA' AND (d_year = 1992 OR d_year = 1993) GROUP BY d_year, s_nation;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey  AND s_region = 'EUROPE' AND (d_year = 1992 OR d_year = 1993);
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey  AND s_region = 'EUROPE' AND (d_year = 1993 OR d_year = 1994);
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey  AND s_region = 'MIDDLE EAST' AND (d_year = 1992 OR d_year = 1993);
select d_year, c_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_region = 'EUROPE' group by d_year, c_nation;
SELECT COUNT(*) FROM part WHERE p_brand < 'MFGR#1111' OR p_brand = 'MFGR#3525';
SELECT COUNT(*) FROM part WHERE p_brand >= 'MFGR#243 ' AND p_brand < 'MFGR#2510' OR p_brand = 'MFGR#4113';
SELECT COUNT(*) FROM part WHERE p_brand BETWEEN 'MFGR#133 ' AND 'MFGR#1413' OR p_brand = 'MFGR#424 ';
SELECT COUNT(*) FROM part WHERE p_brand <= 'MFGR#1535' OR p_brand = 'MFGR#443 ' OR p_category < 'MFGR#11';
SELECT COUNT(*) FROM part WHERE p_brand >= 'MFGR#1520' OR p_brand = 'MFGR#443 ' OR p_category >= 'MFGR#38';
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_region = 'EUROPE' and (d_year = 1992 or d_year = 1993);
select d_year, s_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_region = 'EUROPE' and (d_year = 1994 or d_year = 1995) group by d_year, s_nation;
select d_year, s_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_region = 'EUROPE' and (d_year = 1993 or d_year = 1994) group by d_year, s_nation;
select d_year, s_city, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_nation = 'FRANCE' and (d_year = 1991 or d_year = 1992) group by d_year, s_city;
select d_year, s_city, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'EUROPE' and s_nation = 'JORDAN' and (d_year = 1993 or d_year = 1994) group by d_year, s_city;
select d_year, s_city, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'AMERICA' and s_nation = 'KENYA' and (d_year = 1992 or d_year = 1993) group by d_year, s_city;
select d_year, s_city, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'AMERICA' and s_nation = 'IRAQ' and (d_year = 1993 or d_year = 1994) group by d_year, s_city;
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and s_nation = 'BRAZIL' and (d_year = 1991 or d_year = 1992);
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and s_nation = 'IRAQ' and (d_year = 1994 or d_year = 1995);
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and s_nation = 'SAUDI ARABIA' and (d_year = 1992 or d_year = 1993);
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and s_nation = 'INDIA' and (d_year = 1992 or d_year = 1993);
select count(*) from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and s_nation = 'GERMANY' and (d_year = 1992 or d_year = 1993);
select d_year, s_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'MIDDLE EAST' and s_region = 'MIDDLE EAST' and (d_year = 1993 or d_year = 1994) group by d_year, s_nation;
select d_year, s_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'AFRICA' and s_region = 'AFRICA' and (d_year = 1993 or d_year = 1994) group by d_year, s_nation;
select d_year, s_nation, sum(lo_revenue) - sum(lo_supplycost) as profit from lineorder, dates, supplier, customer where lo_orderdate = d_datekey and lo_suppkey = s_suppkey and lo_custkey = c_custkey and c_region = 'MIDDLE EAST' and s_region = 'MIDDLE EAST' and (d_year = 1993 or d_year = 1994) group by d_year, s_nation;
SELECT c_nation, s_nation, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'EUROPE' AND s_region = 'EUROPE' AND d_year >= 1994 AND d_year <= 1995 GROUP BY c_nation, s_nation, d_year;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'EUROPE' AND s_region = 'EUROPE' AND d_year >= 1993 AND d_year <= 1994;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AMERICA' AND s_region = 'AMERICA' AND d_year >= 1993 AND d_year <= 1994;
SELECT c_city, s_city, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'ARGENTINA' AND s_nation = 'ARGENTINA' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_city, s_city, d_year;
SELECT c_city, s_city, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_nation = 'FRANCE' AND s_nation = 'FRANCE' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_city, s_city, d_year;
SELECT d_year, s_city, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_nation = 'IRAN' AND (d_year = 1991 OR d_year = 1992) GROUP BY d_year, s_city;
SELECT c_nation, s_nation, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AMERICA' AND s_region = 'MIDDLE EAST' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_nation, s_nation, d_year;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AMERICA' AND s_region = 'AFRICA' AND d_year >= 1993 AND d_year <= 1994;
SELECT c_nation, s_nation, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'AFRICA' AND s_region = 'AMERICA' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_nation, s_nation, d_year;
SELECT c_nation, s_nation, d_year, SUM(lo_revenue) AS lo_revenue FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_custkey = c_custkey AND lo_suppkey = s_suppkey AND c_region = 'EUROPE' AND s_region = 'EUROPE' AND d_year >= 1993 AND d_year <= 1994 GROUP BY c_nation, s_nation, d_year;
SELECT d_year, c_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'EUROPE' AND s_region = 'EUROPE' GROUP BY d_year, c_nation;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_region = 'AMERICA';
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_region = 'AMERICA';
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'EUROPE' AND s_region = 'EUROPE';
SELECT d_year, c_nation, SUM(lo_revenue) - SUM(lo_supplycost) AS profit FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_region = 'AMERICA' GROUP BY d_year, c_nation;
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND c_region = 'AMERICA' AND s_region = 'AMERICA' AND (d_year = 1993 OR d_year = 1994);
SELECT COUNT(*) FROM lineorder, dates, supplier, customer WHERE lo_orderdate = d_datekey AND lo_suppkey = s_suppkey AND lo_custkey = c_custkey AND s_region = 'EUROPE';
SELECT COUNT(*) FROM part WHERE p_brand > 'MFGR#1113' OR p_brand = 'MFGR#1229' AND (p_mfgr = 'MFGR#4' OR p_mfgr = 'MFGR#3');
SELECT COUNT(*) FROM part WHERE p_brand <= 'MFGR#2520' OR p_brand = 'MFGR#1332' OR p_mfgr = 'MFGR#1';

