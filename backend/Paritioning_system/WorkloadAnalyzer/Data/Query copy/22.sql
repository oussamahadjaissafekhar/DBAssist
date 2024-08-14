SELECT c_city,
       s_city,
       d_year,
       sum(lo_revenue) AS lo_revenue
FROM lineorder,
     dates,
     supplier,
     customer
WHERE lo_orderdate = d_datekey
  AND lo_custkey = c_custkey
  AND lo_suppkey = s_suppkey
  AND (c_city = 'CANADA   1'
       OR c_city = 'CANADA   1')
  AND (s_city = 'CANADA   1'
       OR s_city = 'CANADA   1')
  AND d_year >= 1991
  AND d_year <= 1992
GROUP BY c_city,
         s_city,
         d_year;