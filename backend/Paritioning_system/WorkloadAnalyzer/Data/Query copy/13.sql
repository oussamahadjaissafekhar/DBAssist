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
  AND c_region = 'AMERICA'
  AND s_region = 'MIDDLE EAST'
  AND d_year >= 1994
  AND d_year <= 1995
GROUP BY c_nation,
         s_nation,
         d_year;