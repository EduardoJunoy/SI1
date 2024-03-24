from sqlalchemy import create_engine, text
from pymongo import MongoClient
import re

DATABASE_TYPE = 'postgresql'
USERNAME = 'alumnodb'
PASSWORD = 'alumnodb'
HOST = 'localhost'
DATABASE_NAME = 'si1'
PORT = '5432'


db_engine = create_engine(
    f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}')
connection = db_engine.connect()

mongo_client = MongoClient()
mongo_db = mongo_client.si1
france_collection = mongo_db.france


def get_french_movies():
    with db_engine.connect() as conn:
        french_movies = conn.execute(text("""
        SELECT im.movietitle,
            im.year
        FROM   imdb_movies im
            JOIN imdb_moviecountries imc
                ON im.movieid = imc.movieid
        WHERE  imc.country = 'France'  
        """)).fetchall()

    return french_movies


def get_movie_actors(movie_title):
    with db_engine.connect() as conn:
        movie_actors = conn.execute(text("""
        SELECT a.actorname
        FROM   imdb_actors a
            JOIN imdb_actormovies am
                ON a.actorid = am.actorid
            JOIN imdb_movies m
                ON am.movieid = m.movieid
        WHERE  m.movietitle = :movie_title;  
        """), {'movie_title': movie_title}).fetchall()

    return [actor[0] for actor in movie_actors]


def get_movie_directors(movie_title):
    with db_engine.connect() as conn:
        movie_directors = conn.execute(text("""
        SELECT d.directorname
        FROM   imdb_directors d
            JOIN imdb_directormovies dm
                ON d.directorid = dm.directorid
            JOIN imdb_movies m
                ON dm.movieid = m.movieid
        WHERE  m.movietitle = :movie_title;  
        """), {'movie_title': movie_title}).fetchall()

    return [director[0] for director in movie_directors]


def get_movie_genres(movie_title):
    with db_engine.connect() as conn:
        movie_genres = conn.execute(text("""
        SELECT mg.genre
        FROM   imdb_moviegenres mg
            JOIN imdb_movies m
                ON mg.movieid = m.movieid
        WHERE  m.movietitle = :movie_title;  
        """), {'movie_title': movie_title}).fetchall()

    return [genre[0] for genre in movie_genres]


def find_mostRelated_movies(movie_title):
    with db_engine.connect() as conn:
        mostRelated_movies = conn.execute(text("""
        SELECT DISTINCT m.movietitle,
                        m.year
        FROM   imdb_movies m
            JOIN imdb_moviegenres mg
                ON m.movieid = mg.movieid
            JOIN imdb_moviecountries imc
                ON imc.movieid = m.movieid
        WHERE  m.movieid != (SELECT movieid
                            FROM   imdb_movies
                            WHERE  movietitle = :movie_title)
            AND imc.country = 'France'
        GROUP  BY m.movieid,
                m.movietitle,
                m.year
        HAVING Count(mg.genre) = (SELECT Count(genre)
                                FROM   imdb_moviegenres
                                WHERE  movieid = (SELECT movieid
                                                    FROM   imdb_movies
                                                    WHERE  movietitle = :movie_title))
            AND Count(mg.genre) = (SELECT Count(DISTINCT mg1.genre)
                                    FROM   imdb_moviegenres mg1
                                            INNER JOIN imdb_moviegenres mg2
                                                    ON mg1.genre = mg2.genre
                                    WHERE  mg2.movieid = (SELECT movieid
                                                            FROM   imdb_movies
                                                            WHERE
                                            movietitle = :movie_title)
                                            AND mg1.movieid = m.movieid);  
        """), {'movie_title': movie_title}).fetchall()

    return [{'movietitle': movie[0], 'year': movie[1]} for movie in mostRelated_movies]


def find_related_movies(movie_title):
    with db_engine.connect() as conn:
        mostRelated_movies = conn.execute(text("""
        WITH moviegenrecount
            AS (SELECT Count(*) AS GenreCount
                FROM   imdb_moviegenres
                WHERE  movieid = (SELECT movieid
                                FROM   imdb_movies
                                WHERE  movietitle = :movie_title)),
            relatedmovies
            AS (SELECT m.movieid,
                        m.movietitle,
                        m.year,
                        Count(mg.genre) AS SharedGenreCount
                FROM   imdb_movies m
                        JOIN imdb_moviegenres mg
                        ON m.movieid = mg.movieid
                        JOIN imdb_moviecountries imc
                        ON m.movieid = imc.movieid
                WHERE  m.movieid != (SELECT movieid
                                    FROM   imdb_movies
                                    WHERE  movietitle = :movie_title)
                        AND imc.country = 'France'
                GROUP  BY m.movieid)
        SELECT rm.movietitle,
            rm.year
        FROM   relatedmovies rm,
            moviegenrecount mgc
        WHERE  rm.sharedgenrecount >= mgc.genrecount / 2
            AND rm.sharedgenrecount < mgc.genrecount  
        """), {'movie_title': movie_title}).fetchall()

    return [{'movietitle': movie[0], 'year': movie[1]} for movie in mostRelated_movies]


def clean_title(title):
    return re.sub(r'\s+\(\d{4}\)$', '', title)


def transform_and_insert_data():
    movies = get_french_movies()
    for movie in movies:
        title, year = movie
        title_withoutYear = clean_title(title)
        year_int = int(year)
        document = {
            "title": title_withoutYear,
            "genres": get_movie_genres(title),
            "year": year_int,
            "directors": get_movie_directors(title),
            "actors": get_movie_actors(title),
            "most_related_movies": find_mostRelated_movies(title),
            "related_movies": find_related_movies(title)
        }

        france_collection.insert_one(document)


def main():
    try:
        transform_and_insert_data()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mongo_client.close()


if __name__ == "__main__":
    main()
