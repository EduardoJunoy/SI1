-- Incluir las claves foráneas ausentes en las tablas orderdetail, imdb_actormovies, inventory y orders.
ALTER TABLE 
  imdb_actormovies 
ADD 
  CONSTRAINT fk_actorid FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);
ALTER TABLE 
  imdb_actormovies 
ADD 
  CONSTRAINT fk_movieid FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);
ALTER TABLE 
  inventory 
ADD 
  CONSTRAINT fkey_inventory_prod_id FOREIGN KEY (prod_id) REFERENCES products(prod_id);
ALTER TABLE 
  orderdetail 
ADD 
  CONSTRAINT fkey_orderid FOREIGN KEY (orderid) REFERENCES orders(orderid);
ALTER TABLE 
  orderdetail 
ADD 
  CONSTRAINT fkey_prodid FOREIGN KEY (prod_id) REFERENCES products(prod_id);
ALTER TABLE 
  orders 
ADD 
  CONSTRAINT fkey_orders_orderid FOREIGN KEY (customerid) REFERENCES customers(customerid);
 
-- Creamos una tabla countries
CREATE TABLE countries (
  countryid serial4 PRIMARY KEY, 
  countryname VARCHAR(32) UNIQUE NOT NULL
);

-- Pasamos el atributo country a la nueva tabla countries 
INSERT INTO countries(countryname) 
SELECT 
  DISTINCT country 
FROM 
  imdb_moviecountries;
 
-- Modificamos la tabla imdb_moviecountries para que use countryid
ALTER TABLE 
  imdb_moviecountries 
ADD 
  COLUMN countryid INT;
ALTER TABLE 
  imdb_moviecountries 
ADD 
  CONSTRAINT fk_countryid FOREIGN KEY (countryid) REFERENCES countries(countryid);
 
-- Actualizar la columna countryid de imdb_moviecountries
UPDATE 
  imdb_moviecountries mc 
SET 
  countryid = c.countryid 
FROM 
  countries c 
WHERE 
  mc.country = c.countryname;
 
-- Eliminamos la columna que ha pasado a la tabla countries
ALTER TABLE 
  imdb_moviecountries 
DROP 
  COLUMN country;
-- Creamos una tabla languages
CREATE TABLE languages (
  languageid serial4 PRIMARY KEY, 
  language VARCHAR(32) UNIQUE NOT NULL
);

-- Pasamos el atributo language a la nueva tabla lenguage 
INSERT INTO languages(language) 
SELECT 
  DISTINCT language 
FROM 
  imdb_movielanguages 
  
 -- Modificamos la tabla imdb_moviecountries para que use languageid
ALTER TABLE 
  imdb_movielanguages 
ADD 
  COLUMN languageid INT;
ALTER TABLE 
  imdb_movielanguages 
ADD 
  CONSTRAINT fk_languageid FOREIGN KEY (languageid) REFERENCES languages(languageid);
 
-- Actualizar la columna languageid de imdb_movielanguages
UPDATE 
  imdb_movielanguages ml 
SET 
  languageid = l.languageid 
FROM 
  languages l 
WHERE 
  ml.language = l.language;
 
-- Eliminamos la columna que ha pasado a la tabla languages
ALTER TABLE 
  imdb_movielanguages 
DROP 
  COLUMN language;
 
-- Creamos una tabla genres
CREATE TABLE genres (
  genreid serial4 PRIMARY KEY, 
  genrename VARCHAR(32) UNIQUE NOT NULL
);

-- Pasamos el atributo genre a la nueva tabla genres 
INSERT INTO genres(genrename) 
SELECT 
  DISTINCT genre 
FROM 
  imdb_moviegenres 
 
-- Modificamos la tabla imdb_moviegenres para que use genreid
ALTER TABLE 
  imdb_moviegenres 
ADD 
  COLUMN genreid INTEGER;
ALTER TABLE 
  imdb_moviegenres 
ADD 
  CONSTRAINT fk_genreid FOREIGN KEY (genreid) REFERENCES genres(genreid);
 
-- Actualizar la columna genreid de imdb_moviegenre
UPDATE 
  imdb_moviegenres mg 
SET 
  genreid = g.genreid 
FROM 
  genres g 
WHERE 
  g.genrename = mg.genre;
 
-- Eliminamos la columna que ha pasado a la tabla genre
ALTER TABLE 
  imdb_moviegenres 
DROP 
  COLUMN genre;
------------------------------------------------------------
ALTER TABLE 
  customers 
ADD 
  BALANCE NUMERIC;
 
CREATE TABLE ratings (
  movieid serial4 NOT NULL, 
  customerid serial4 NOT NULL, 
  rating NUMERIC NOT NULL CHECK (
    rating > 1 
    AND rating < 10
  ), 
  CONSTRAINT fk_movie FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid), 
  CONSTRAINT fk_customerid FOREIGN KEY (customerid) REFERENCES customers(customerid), 
  CONSTRAINT unique_rating UNIQUE (movieid, customerid)
);

ALTER TABLE 
  imdb_movies 
ADD 
  ratingmean NUMERIC;
ALTER TABLE 
  imdb_movies 
ADD 
  ratingcount INTEGER;
ALTER TABLE 
  customers ALTER COLUMN password TYPE CHARACTER VARYING(96);
 
CREATE OR REPLACE PROCEDURE setCustomersBalance(IN initialBalance BIGINT) 
LANGUAGE plpgsql 
AS $$
BEGIN 
    UPDATE customers 
    SET BALANCE = RANDOM() * (initialBalance);
END;
$$;


--------------------------------------------------------------------



