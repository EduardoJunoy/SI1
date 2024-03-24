CREATE OR REPLACE FUNCTION getTopSales(year1 INT, year2 INT)
RETURNS TABLE(Year INT, MovieID INT, Sales BIGINT) AS $$
BEGIN
    RETURN QUERY
    WITH yearly_sales AS (
        SELECT
            CAST(EXTRACT(YEAR FROM o.orderdate) AS INT) AS sale_year, -- Convertir a INT
            p.movieid AS movie_id,
            COUNT(*) AS total_sales
        FROM 
            orders o
            JOIN orderdetail od ON o.orderid = od.orderid
            JOIN products p ON od.prod_id = p.prod_id
        WHERE 
            EXTRACT(YEAR FROM o.orderdate) IN (year1, year2)
        GROUP BY 
            sale_year, p.movieid
    ),
    ranked_sales AS (
        SELECT
            sale_year,
            movie_id,
            total_sales,
            RANK() OVER (PARTITION BY sale_year ORDER BY total_sales DESC) as rank 
        FROM 
            yearly_sales
    )
    SELECT 
        sale_year AS Year, 
        movie_id AS MovieID, 
        total_sales AS Sales
    FROM 
        ranked_sales
    WHERE 
        rank = 1;
END;
$$ LANGUAGE plpgsql;