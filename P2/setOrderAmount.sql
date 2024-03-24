CREATE OR REPLACE PROCEDURE setOrderAmount() 
LANGUAGE plpgsql 
AS $$
BEGIN
    -- Actualizar netamount y totalamount solo para los pedidos que no tienen estos valores
    UPDATE orders
    SET netamount = COALESCE(orders.netamount, od.net_amount),
        totalamount = COALESCE(orders.totalamount, od.net_amount + orders.tax)
    FROM (
        -- Calcular la suma de los precios de los productos para cada pedido
        SELECT orderid, SUM(price * quantity) AS net_amount
        FROM orderdetail
        GROUP BY orderid
    ) AS od
    WHERE orders.orderid = od.orderid 
    AND (orders.netamount IS NULL OR orders.totalamount IS NULL);
END;
$$;