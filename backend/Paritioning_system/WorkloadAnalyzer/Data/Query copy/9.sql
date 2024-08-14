SELECT c_nation,
       s_nation,
       d_year,
       sum(lo_revenue) AS lo_revenue
FROM lineorder,
     dates,
     supplier,
     customer
WHERE lo_orderdate = d_datekey
  AND lo_custkey = c_custkey
  AND lo_suppkey = s_suppkey
  AND c_region = 'MIDDLE EAST'
  AND s_region = 'AMERICA'
  AND d_year >= 1991
  AND d_year <= 1992
GROUP BY c_nation,
         s_nation,
         d_year;