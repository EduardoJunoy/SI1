MATCH (hattie:Person {name: "Winston, Hattie"})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coactor)
WITH coactor, collect(m) AS hattieMovies, hattie
MATCH (coactor)-[:ACTED_IN]->(m2:Movie)<-[:ACTED_IN]-(actor)
WHERE NOT (actor)-[:ACTED_IN]->()<-[:ACTED_IN]-(hattie)
AND actor.name <> "Winston, Hattie"
AND NOT m2 IN hattieMovies
WITH actor
RETURN DISTINCT actor.name AS ActorName
ORDER BY actor.name
LIMIT 10
