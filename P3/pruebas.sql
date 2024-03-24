SELECT im.movietitle,
       im.year
FROM   imdb_movies im
       JOIN imdb_moviecountries imc
         ON im.movieid = imc.movieid
WHERE  imc.country = 'France' 


            SELECT DISTINCT m.movietitle, m.year
            FROM imdb_movies m
            JOIN imdb_moviegenres mg ON m.movieid = mg.movieid join 
                 imdb_moviecountries imc on imc.movieid = m.movieid
            WHERE m.movieid != (
                SELECT movieid
                FROM imdb_movies
                WHERE movietitle = 'Ran (1985)'
            ) AND imc.country = 'France'
GROUP  BY m.movieid,
          m.movietitle,
          m.year
HAVING Count(mg.genre) = (SELECT Count(genre)
                          FROM   imdb_moviegenres
                          WHERE  movieid = (SELECT movieid
                                            FROM   imdb_movies
                                            WHERE
                                 movietitle = 'Ran (1985)'))
       AND Count(mg.genre) = (SELECT Count(DISTINCT mg1.genre)
                              FROM   imdb_moviegenres mg1
                                     INNER JOIN imdb_moviegenres mg2
                                             ON mg1.genre = mg2.genre
                                                AND mg2.movieid = (SELECT
                                                    movieid
                                                                   FROM
                                                    imdb_movies
                                                                   WHERE
                                     movietitle = 'Ran (1985)')
                              WHERE  mg1.movieid = m.movieid);  
WITH MovieGenreCount AS (
    SELECT COUNT(*) AS GenreCount
    FROM imdb_moviegenres
    WHERE movieid = (
        SELECT movieid
        FROM imdb_movies
        WHERE movietitle = 'Ran (1985)'
    )
),
RelatedMovies AS (
    SELECT m.movieid, m.movietitle, m.year, COUNT(mg.genre) AS SharedGenreCount
    FROM imdb_movies m
    JOIN imdb_moviegenres mg ON m.movieid = mg.movieid
    JOIN imdb_moviecountries imc ON m.movieid = imc.movieid
    WHERE m.movieid != (
        SELECT movieid
        FROM imdb_movies
        WHERE movietitle = 'Ran (1985)'
    )
    AND imc.country = 'France'
    GROUP BY m.movieid
)
SELECT rm.movietitle, rm.year
FROM RelatedMovies rm, MovieGenreCount mgc
WHERE rm.SharedGenreCount >= mgc.GenreCount / 2
AND rm.SharedGenreCount < mgc.GenreCount                    

SELECT genre
FROM imdb_moviegenres
WHERE movieid = (
    SELECT movieid
    FROM imdb_movies
    WHERE movietitle = '''Breaker'' Morant (1980)'
);

SELECT a.actorname
FROM imdb_actors a
JOIN imdb_actormovies am ON a.actorid = am.actorid
JOIN imdb_movies m ON am.movieid = m.movieid
WHERE m.movietitle = '''Breaker'' Morant (1980)';

SELECT d.directorname
FROM imdb_directors d
JOIN imdb_directormovies dm ON d.directorid = dm.directorid
JOIN imdb_movies m ON dm.movieid = m.movieid
WHERE m.movietitle = '''Breaker'' Morant (1980)';

SELECT im.movieid,
       im.movietitle
FROM   imdb_movies im
       JOIN imdb_moviecountries imc
         ON im.movieid = imc.movieid
       JOIN products p
         ON im.movieid = p.movieid
       JOIN orderdetail o
         ON p.prod_id = o.prod_id
WHERE  imc.country = 'USA'
GROUP  BY im.movieid
ORDER  BY Sum(o.quantity) DESC
LIMIT  20;  

SELECT c.email, c.firstname, c.lastname, c.phone
FROM   customers c
WHERE  c.country = 'Spain'  

select *
from imdb_movies im join imdb_moviegenres im2 
	 on im.movieid = im2.movieid join imdb_moviecountries im3 
	 on im.movieid = im3.movieid 
where im3.country = 'France' and im2.genre = 'Sci-Fi'

