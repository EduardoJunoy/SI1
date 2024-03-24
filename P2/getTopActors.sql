CREATE OR REPLACE FUNCTION getTopActors(genreNameInput VARCHAR)
RETURNS TABLE(ActorName VARCHAR, NumMovies INT, DebutYear INT, DebutFilm VARCHAR, DirectorName VARCHAR) AS $$
BEGIN
    RETURN QUERY
    WITH actor_genre_performance AS (
        SELECT
            a.actorid,
            a.actorname AS actor_name,
            CAST(m.year AS INTEGER) AS debut_year, -- Convertir a integer
            m.movietitle AS debut_film,
            CAST(COUNT(*) OVER (PARTITION BY a.actorid) AS INT) AS num_movies
        FROM 
            imdb_actors a
            JOIN imdb_actormovies am ON a.actorid = am.actorid
            JOIN imdb_movies m ON am.movieid = m.movieid
            JOIN imdb_moviegenres mg ON m.movieid = mg.movieid
            JOIN genres g ON mg.genreid = g.genreid
        WHERE 
            g.genrename = genreNameInput
        GROUP BY 
            a.actorid, a.actorname, m.year, m.movietitle
    ),
    actor_debut_films AS (
        SELECT
            actorid,
            actor_name,
            MIN(debut_year) AS debut_year,
            debut_film,
            num_movies
        FROM 
            actor_genre_performance
        GROUP BY 
            actorid, actor_name, debut_film, num_movies
    ),
    actor_directors AS (
        SELECT
            adf.actor_name,
            adf.num_movies,
            adf.debut_year,
            adf.debut_film,
            d.directorname AS director_name
        FROM 
            actor_debut_films adf
            JOIN imdb_actormovies am ON adf.actorid = am.actorid
            JOIN imdb_directormovies md ON am.movieid = md.movieid
            JOIN imdb_directors d ON md.directorid = d.directorid
        WHERE 
            adf.num_movies > 4
    )
    SELECT 
        actor_name AS ActorName,
        num_movies AS NumMovies, 
        debut_year AS DebutYear, 
        debut_film AS DebutFilm, 
        director_name AS DirectorName
    FROM 
        actor_directors
    ORDER BY 
        num_movies DESC, debut_year, debut_film, director_name;
END;
$$ LANGUAGE plpgsql;
