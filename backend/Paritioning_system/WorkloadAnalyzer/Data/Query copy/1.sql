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
  AND c_nation = 'EUROPE'
  AND s_nation = 'EUROPE'
  AND d_year >= 1992
  AND d_year <= 1993
GROUP BY c_city,
         s_city,
         d_year