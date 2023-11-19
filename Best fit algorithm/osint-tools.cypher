// Creazione dei nodi per gli strumenti
CALL apoc.load.json("https://raw.githubusercontent.com/ciro-99/OSINT/main/osint%20best-fit%20alg/osint-tools-copy.json") YIELD value
UNWIND value.osint_tools as tool
MERGE (t:Tool {name: tool.name, platform: tool.platform})

// Creazione dei nodi per gli input
FOREACH (input IN tool.input | MERGE (i:Input {name: input}) MERGE (t)-[:USES]->(i))

// Creazione dei nodi per gli output e collegamento con l'Ontologia
FOREACH (output IN tool.output | MERGE (o:Resource {label: output}) MERGE (t)-[:PRODUCES]->(o))

// Creazione dei nodi per le capabilities
FOREACH (capability IN tool.capability | MERGE (c:Capability {name: capability}) MERGE (t)-[:HAS_CAPABILITY]->(c))

// Creazione dei nodi per le piattaforme
FOREACH (platform IN CASE WHEN NOT tool.platform IS NULL THEN [tool.platform] ELSE [] END | MERGE (p:Platform {name: platform}) MERGE (t)-[:RUNS_ON]->(p))