MATCH (director:Person {name: "Reiner, Carl"}), (actress:Person {name: "Smyth, Lisa (I)"})
MATCH path = shortestPath((director)-[:ACTED_IN|DIRECTED*]-(actress))
RETURN path
