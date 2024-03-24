UPDATE orderdetail od
SET price = ROUND(p.price * POW(1.02, EXTRACT(YEAR FROM age(o.orderdate))), 2)
FROM orders o, products p
WHERE od.orderid = o.orderid AND od.prod_id = p.prod_id AND o.orderdate <= CURRENT_DATE;