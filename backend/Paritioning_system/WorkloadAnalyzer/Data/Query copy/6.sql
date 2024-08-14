SELECT c_city,
       s_city,
       d_year,
       sum(lo_revenue) AS lo_revenue
FROM lineorder,
     dates,
     supplier,
     customer
WHERE lo_orderdate = d_datekey
  AND lo_suppkey = s_suppkey
  AND lo_custkey = c_custkey
  AND (c_city = 'UNITED ST1'
       OR c_city = 'UNITED ST1')
  AND (s_city = 'UNITED ST1'
       OR s_city = 'UNITED ST1')
  GROUP BY c_city,
         s_city,
         d_year