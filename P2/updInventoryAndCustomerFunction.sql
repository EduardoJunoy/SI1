CREATE OR REPLACE FUNCTION updInventoryAndCustomerFunction() 
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si el estado del pedido ha cambiado a 'Paid'
    IF OLD.status IS DISTINCT FROM NEW.status AND NEW.status = 'Paid' THEN
        -- Actualizar la tabla inventory
        UPDATE inventory
        SET stock = stock - od.quantity,
            sales = sales + od.quantity
        FROM orderdetail od
        WHERE od.orderid = NEW.orderid AND inventory.prod_id = od.prod_id;

        -- Descontar el precio total de la compra del balance del cliente
        UPDATE customers
        SET balance = balance - NEW.totalamount
        WHERE customerid = NEW.customerid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updInventoryAndCustomer
AFTER UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION updInventoryAndCustomerFunction();