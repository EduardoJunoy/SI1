CREATE OR REPLACE FUNCTION updOrdersFunction() 
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar orders después de insertar en orderdetail
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        UPDATE orders
        SET netamount = (SELECT SUM(price * quantity) FROM orderdetail WHERE orderid = NEW.orderid),
            totalamount = (SELECT SUM(price * quantity) FROM orderdetail WHERE orderid = NEW.orderid) + (SELECT tax FROM orders WHERE orderid = NEW.orderid)
        WHERE orderid = NEW.orderid;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE orders
        SET netamount = (SELECT SUM(price * quantity) FROM orderdetail WHERE orderid = OLD.orderid),
            totalamount = (SELECT SUM(price * quantity) FROM orderdetail WHERE orderid = OLD.orderid) + (SELECT tax FROM orders WHERE orderid = OLD.orderid)
        WHERE orderid = OLD.orderid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updOrders
AFTER INSERT OR UPDATE OR DELETE ON orderdetail
FOR EACH ROW EXECUTE FUNCTION updOrdersFunction();