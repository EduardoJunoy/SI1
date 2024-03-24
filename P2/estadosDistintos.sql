CREATE INDEX INDEX_ORDERDATE ON public.orders(EXTRACT(YEAR FROM ORDERDATE));
CREATE INDEX INDEX_COUNTRY ON public.customers(COUNTRY);

--DROP INDEX INDEX_ORDERDATE;
--DROP INDEX INDEX_COUNTRY;

EXPLAIN
SELECT COUNT(DISTINCT c.state)
FROM public.customers c
JOIN public.orders o ON c.customerid = o.customerid
WHERE c.country = 'Peru' AND EXTRACT(YEAR FROM o.orderdate) = 2017;

SELECT COUNT(DISTINCT c.state)
FROM public.customers c
JOIN public.orders o ON c.customerid = o.customerid
WHERE c.country = 'Peru' AND EXTRACT(YEAR FROM o.orderdate) = 2017;