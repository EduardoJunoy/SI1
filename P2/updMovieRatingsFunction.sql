CREATE OR REPLACE FUNCTION updMovieRatingsFunction() 
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular el nuevo promedio y conteo de ratings
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        UPDATE imdb_movies
        SET ratingmean = (SELECT AVG(rating) FROM ratings WHERE movieid = NEW.movieid),
            ratingcount = (SELECT COUNT(*) FROM ratings WHERE movieid = NEW.movieid)
        WHERE movieid = NEW.movieid;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE imdb_movies
        SET ratingmean = (SELECT AVG(rating) FROM ratings WHERE movieid = OLD.movieid),
            ratingcount = (SELECT COUNT(*) FROM ratings WHERE movieid = OLD.movieid)
        WHERE movieid = OLD.movieid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER updRatings
AFTER INSERT OR UPDATE OR DELETE ON ratings
FOR EACH ROW EXECUTE FUNCTION updMovieRatingsFunction();