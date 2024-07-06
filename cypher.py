import requests
from neo4j import GraphDatabase

response = requests.get('http://localhost:7474')
if response.status_code == 200:
    print('Connected to Neo4j server')
else:
    print(
        f'Error connecting to Neo4j server. Status code: {response.status_code}. Response content: {response.content}')
    exit()


def print_(tx, name):
    query = "MATCH (start)-[r]->(end) WHERE start.name = $name AND r.property = '描述' RETURN start, end, end.name"
    for record in tx.run(query, name=name):
        print(record['end.name'])


driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))

with driver.session(database="neo4j") as session:
    session.execute_read(print_, "大龙湫")
driver.close()