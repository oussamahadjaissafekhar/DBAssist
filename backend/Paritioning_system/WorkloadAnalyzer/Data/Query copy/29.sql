SELECT sum(lo_revenue) AS revenue
FROM lineorder,
     dates
WHERE lo_orderdate = d_datekey
  AND d_year = 1996
  AND lo_discount > 2
  AND lo_discount < 4
  AND lo_quantity < 0;