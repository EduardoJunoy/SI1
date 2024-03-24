ALTER TABLE customers
ADD COLUMN p numeric;

CREATE OR REPLACE FUNCTION update_cart_discount()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_sleep(10);
    UPDATE orderdetail
    SET price = price * (1-NEW.p / 100)
    FROM orders
    WHERE orders.customerid = NEW.customerid AND orderdetail.orderid = orders.orderid AND orders.status IS NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_update_cart_discount
AFTER UPDATE OF p ON customers
FOR EACH ROW
EXECUTE FUNCTION update_cart_discount();