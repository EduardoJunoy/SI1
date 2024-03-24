from pymongo import MongoClient

mongo_client = MongoClient()
mongo_db = mongo_client.si1
france_collection = mongo_db.france

science_fiction_movies = france_collection.find({
    'genres': {'$in': ['Sci-Fi']},  
    'year': {'$gte': 1994, '$lte': 1998}
})

print("Science Fiction Movies from 1994 to 1998:")
for movie in science_fiction_movies:
    print(movie)

drama_movies = france_collection.find({
    'genres': {'$in': ['Drama']}, 
    'year': 1998,
    'title': {'$regex': ', The$'}
})

print("Drama Movies from 1998 starting with 'The':")
for movie in drama_movies:
    print(movie)

movies_with_actors = france_collection.find({
    'actors': {'$all': ['Dunaway, Faye', 'Mortensen, Viggo']}
})

print("Movies with Faye Dunaway and Viggo Mortensen:")
for movie in movies_with_actors:
    print(movie)

mongo_client.close()