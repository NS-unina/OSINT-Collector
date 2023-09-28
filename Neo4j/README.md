# Semantic Search in a Knowledge Graph using NLP and Ontologies (with Neo4j)

## Installing Neo4j (docker)

- Create a docker container using the docker-compose file:

```bash
  docker compose up -d
```

Access the Web UI at http://localhost:7474/ with the following credentials:

- Username: "neo4j"
- Password: "password"

[Docs: https://neo4j.com/docs/operations-manual/current/docker/]

## Configuring Neo4j to use RDF data

- Pre-requisite: create uniqueness constraint; in RDF everything is uniquely identified by URI. And the way to store it efficiently in Neo4j is by creating an index (a constraint) that guarantees both the uniqueness, but also gives a fast access to it.

```bash
  CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;
```

- Setting the configuration of the graph; with this option we can map the Ontolgy URIs with custom names, more human readble. 

```bash
  CALL n10s.graphconfig.init({handleVocabUris: "MAP"});
```

The method n10s.graphconfig.init() can help us initialising the Graph Config. Calling the procedure without parameters will set all the default values.

```bash
CALL n10s.nsprefixes.add('osint','osint://voc#');
CALL n10s.mapping.add("osint://voc#subCatOf","SUB_CAT_OF");
CALL n10s.mapping.add("osint://voc#about","ABOUT");
```

[Docs: https://neo4j.com/labs/neosemantics/4.3/config/]

## Importing Ontologies

Ontologies are serialised as RDF, so they can be imported using plain n10s.rdf.import.fetch but the n10s.onto.import.fetch method will give us a higher level of control over how an RDFS or OWL ontology is imported into Neo4j.

- Import the OSINT Ontology:

```bash
  CALL n10s.onto.import.fetch("https://raw.githubusercontent.com/ciro-99/OSINT/main/OSINT.ttl","Turtle")
```

- To see a preview of the ontology without importing it, use the following function:

```bash
  CALL n10s.onto.preview.fetch("https://raw.githubusercontent.com/ciro-99/OSINT/main/OSINT.ttl","Turtle")
```

![](https://i.postimg.cc/ryHkR3V4/preview-ontology.png)

[Docs: https://neo4j.com/labs/neosemantics/4.3/importing-ontologies/]

## Extending our knowledge with Wikidata

Wikidata is a free and open knowledge base that can be read and edited by both humans and machines. It acts as central storage for the structured data of its Wikimedia sister projects including Wikipedia.

Wikidata stores data as RDF and offers a SPARQL API (https://query.wikidata.org/; we can write a query and convert the results to an RDF endpoint. With the following (https://w.wiki/7akt) we are asking Wikidata to return anything, all the concepts that ultimately are a subcategory (P279) or instances (P31) of the wikidata object "drug" (that is identified with this alphanumeric string: Q8386), and returning it in the form of triples, which is the way RDF is represented.

```bash
prefix osint: <osint://voc#> 
#SELECT ?item ?label 
CONSTRUCT {
?item a osint:Category ; osint:subCatOf ?parentItem .  
  ?item osint:name ?label .
  ?parentItem a osint:Category; osint:name ?parentLabel .
  ?article a osint:WikipediaPage; osint:about ?item ;
}
WHERE 
{
  ?item (wdt:P31|wdt:P279)* wd:Q8386 .
  ?item wdt:P31|wdt:P279 ?parentItem .
  ?item rdfs:label ?label .
  filter(lang(?label) = "it")
  ?parentItem rdfs:label ?parentLabel .
  filter(lang(?parentLabel) = "it")
  
  OPTIONAL {
      ?article schema:about ?item ;
            schema:inLanguage "it" ;
            schema:isPartOf <https://it.wikipedia.org/> .
    }
}
```

At this point we can import the Wikidata’s Drug Ontolgy into Neo4j, using the SPARQL Endpoint URI:

![](https://i.postimg.cc/XvnS008R/sparql.png)

```bash
WITH "<SPARQL Endpoint>" AS drugsUri
CALL n10s.rdf.import.fetch(drugsUri, 'Turtle' , { headerParams: { Accept: "application/x-turtle" } })
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

We can iterate this process for all the category of interest of our domain, like "weapon", "crime", ecc.

## Importing data

We can import Instagram posts and users in the following way:

```bash
CALL apoc.load.json("https://raw.githubusercontent.com/ciro-99/OSINT/main/guardiadifinanza_feed.json") YIELD value
UNWIND value.items as p
MERGE (post:igPost {id:p.pk}) ON CREATE SET post.caption = p.caption.text
MERGE (user:igUser {id:p.caption.user.pk_id}) ON CREATE SET user.fullName = p.caption.user.full_name, user.username = p.caption.user.username
MERGE (user)-[:published]->(post)
```

where the .json file is generated from the OSINT-IG API. As an example the file refers to the Instagram account of "Guardia di Finanza".

[Docs: https://neo4j.com/labs/apoc/4.1/import/load-json/]

[Note: this manual phase will be replaced with an automatic one. The idea is to create a Data Ingestion Pipeline that will be able to create the KG in an automatic way, guided by the Ontology.]

## Entity extraction with APOC NLP

APOC is Neo4j’s standard utility library. It includes over 450 standard procedures, providing functionality for utilities, conversions, graph updates, and more. It has procedures that wrap the Natural Language Processing APIs for the major cloud providers, AWS, GCP, and Azure.

In this project it has been used the Natural Language AI tool of Google Cloud Platform (https://cloud.google.com/natural-language?hl=it).

First above all is important to create a project on GCP and enable the API related to the Language AI Tool; then create the corresponding API key to use as credentials.

- Create the key parameter:

```bash
:params key => ("AIzaSyBW32oUedSW2c8FTCG9EzsXZfPUCCmTssA")
```

- Connecting posts and the Drug Ontology

```bash
CALL apoc.periodic.iterate(
  "MATCH (p:igPost)
   WHERE not(exists(p.processed))
   RETURN p",
  "CALL apoc.nlp.gcp.entities.stream([item in $_batch | item.p], {
     nodeProperty: 'caption',
     key: $key
   })
   YIELD node, value
   SET node.processed = true
   WITH node, value
   UNWIND value.entities AS entity
   WITH entity, node
   MATCH (c:Category {name: entity.name})
   MERGE (node)-[:refers_to]->(c)",
  {batchMode: "BATCH_SINGLE", batchSize: 10, params: {key: $key}})
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```

This cypher code iterate on all the igPosts that are not been processed. The NLP function extracts the entities from the caption of the post and for each entity it try to find a match with an existing category in the Ontology and (if exist) creates a relationship between them:

![](https://i.postimg.cc/vZFw3n6H/after-nlp.png)

[Docs: https://neo4j.com/labs/apoc/4.1/nlp/gcp/]

## Semantic Search

We can write a query that starts from a top level category and finds all the posts attached to the underlying taxonomy and make inferences on our KG. The n10s.inference.nodesInCategory procedure automates this process. For example, we can find "all the post published on Instagram that refers directly or indirectly to the category "hashish":

```bash
MATCH (c:Category {name: "hashish"})
CALL n10s.inference.nodesInCategory(c, {
	inCatRel: "refers_to"
})
YIELD node as post
MATCH (post)<-[:published]-(u)
RETURN DISTINCT post.id, post.caption, u.username
```

![](https://i.postimg.cc/yYSzmjxb/inference1.png)

[Docs: https://neo4j.com/labs/neosemantics/4.0/inference/]

Or, more general "all the post published on Instagram that refers to "drug":

```bash
MATCH path = (:Category {name: "droga"})-[:SUB_CAT_OF*0..]->()<-[:SUB_CAT_OF*0..]-()-[:refers_to]-(p:igPost)
return path
```

![](https://i.postimg.cc/cLRyjJQ7/inference2.png)

And so on...