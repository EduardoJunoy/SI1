from sqlalchemy import create_engine, text
from neo4j import GraphDatabase
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

neo4j_engine = GraphDatabase.driver(
    'bolt://localhost:7687', auth=('neo4j', 'si1-password'))


def get_american_movies():
    with db_engine.connect() as conn:
        american_movies = conn.execute(text("""
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
    """)).fetchall()

    return [{"movieid": movie[0], "movietitle": movie[1]} for movie in american_movies]


def get_movie_actors(movie_title):
    with db_engine.connect() as conn:
        movie_actors = conn.execute(text("""
        SELECT a.actorname, a.actorid
        FROM   imdb_actors a
            JOIN imdb_actormovies am
                ON a.actorid = am.actorid
            JOIN imdb_movies m
                ON am.movieid = m.movieid
        WHERE  m.movietitle = :movie_title;  
        """), {'movie_title': movie_title}).fetchall()

    return [{"actorname": actor[0], "actorid": actor[1]} for actor in movie_actors]


def get_movie_directors(movie_title):
    with db_engine.connect() as conn:
        movie_directors = conn.execute(text("""
        SELECT d.directorname, d.directorid
        FROM   imdb_directors d
            JOIN imdb_directormovies dm
                ON d.directorid = dm.directorid
            JOIN imdb_movies m
                ON dm.movieid = m.movieid
        WHERE  m.movietitle = :movie_title;  
        """), {'movie_title': movie_title}).fetchall()

    return [{"directorname": director[0], "directorid": director[1]} for director in movie_directors]


def clean_title(title):
    return re.sub(r'\s+\(\d{4}\)$', '', title)


def create_movie_nodes(session, movie):
    movie_title = clean_title(movie['movietitle'])
    session.run("CREATE (:Movie {movieId: $movieid, title: $movietitle})",
                movieid=movie['movieid'], movietitle=movie_title)


def create_actor_node(session, actor_name, actor_id):
    session.run("MERGE (a:Actor {actorId: $actorId}) ON CREATE SET a.name = $actorName RETURN a",
                actorId=actor_id, actorName=actor_name)


def create_director_node(session, director_name, director_id):
    session.run("MERGE (d:Director {directorId: $directorId}) ON CREATE SET d.name = $directorName RETURN d",
                directorId=director_id, directorName=director_name)


def create_person_node(session, person_name, person_id):
    session.run("MERGE (p:Person {personId: $personId}) ON CREATE SET p.name = $personName RETURN p",
                personId=person_id, personName=person_name)

def create_acted_in_relationship(session, person_id, movie_id):
    session.run("MATCH (p:Person {personId: $personId}), (m:Movie {movieId: $movieId}) "
                "MERGE (p)-[:ACTED_IN]->(m)",
                personId=person_id, movieId=movie_id)

def create_directed_relationship(session, person_id, movie_id):
    session.run("MATCH (p:Person {personId: $personId}), (m:Movie {movieId: $movieId}) "
                "MERGE (p)-[:DIRECTED]->(m)",
                personId=person_id, movieId=movie_id)

def main():
    try:
        movies = get_american_movies()
        with neo4j_engine.session() as session:
            for movie in movies:
                movie_id = movie['movieid']
                movie_title = movie['movietitle']

                # Create the movie node
                create_movie_nodes(session, movie)

                # Create nodes and relationships for actors
                actors = get_movie_actors(movie_title)
                for actor in actors:
                    create_person_node(session, actor['actorname'], actor['actorid'])
                    create_acted_in_relationship(session, actor['actorid'], movie_id)

                # Create nodes and relationships for directors
                directors = get_movie_directors(movie_title)
                for director in directors:
                    # Re-use the same person node creation function
                    create_person_node(session, director['directorname'], director['directorid'])
                    create_directed_relationship(session, director['directorid'], movie_id)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        neo4j_engine.close()

if __name__ == "__main__":
    main()
