SELECT sum(lo_revenue) AS revenue
FROM lineorder,
     dates
WHERE lo_orderdate = d_datekey
  AND d_weeknuminyear = 10
  AND d_year = 1992
  AND lo_discount > 2
  AND lo_discount < 4
  AND lo_quantity > 8
  AND lo_quantity < 10;