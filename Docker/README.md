## Configuring Neo4j to use RDF data

- Pre-requisite: Create uniqueness constraint

```bash
  CREATE CONSTRAINT n10s_unique_uri ON (r:Resource)
  ASSERT r.uri IS UNIQUE;
```

- Setting the configuration of the graph

```bash
  CALL n10s.graphconfig.init({handleVocabUris: "MAP"})
```

The method n10s.graphconfig.init() can help us initialising the Graph Config. Calling the procedure without parameters will set all the default values.

## Importing Ontologies

Ontologies are serialised as RDF, so they can be imported using plain n10s.rdf.import.fetch but the n10s.onto.import.fetch method will give us a higher level of control over how an RDFS or OWL ontology is imported into Neo4j.

- Configuration:

```bash
  CALL n10s.nsprefixes.add('owl','http://www.w3.org/2002/07/owl#');
  CALL n10s.nsprefixes.add('rdfs','http://www.w3.org/2000/01/rdf-schema#');
  CALL n10s.mapping.add("http://www.w3.org/2000/01/rdf-schema#subClassOf","SUB_CAT_OF");
  CALL n10s.mapping.add("http://www.w3.org/2000/01/rdf-schema#label","name");
  CALL n10s.mapping.add("http://www.w3.org/2002/07/owl#Class","Category");
```

- Import:

```bash
  CALL n10s.onto.import.fetch("https://www.astrowood.it/Ontology/OSINT_v3","Turtle")
```
