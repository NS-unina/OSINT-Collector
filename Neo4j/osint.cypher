#Load new user with published posts:

call apoc.load.json("https://raw.githubusercontent.com/ciro-99/OSINT/main/guardiadifinanza_feed.json") YIELD value
UNWIND value.items as p
MERGE (post:igPost {id:p.pk}) ON CREATE SET post.caption = p.caption.text
MERGE (user:igUser {id:p.caption.user.pk_id}) ON CREATE SET user.fullName = p.caption.user.full_name, user.username = p.caption.user.username
MERGE (user)-[:published]->(post)

#Load user following:

call apoc.load.json("https://raw.githubusercontent.com/ciro-99/OSINT/main/nasa_following.json") YIELD value
UNWIND value.users as u
MATCH (user:igUser {id:"245649574"})
MERGE (newUser:igUser {id:u.pk_id}) ON CREATE SET newUser.full_name = u.fullName, newUser.username = u.username
MERGE (user)-[:Follows]->(newUser)

The above section will be replaced with a "Data Ingestion Pipeline" that is based on the Ontology driven KG construction

# Micro-Inferencer

match (from:Resource)<-[:RANGE]-(r:Relationship)-[:DOMAIN]->(to:Resource)
match (x)-[rel]->(y)
where type(rel) = r.name
call apoc.create.addLabels(x,[from.name]) yield node as xs
call apoc.create.addLabels(y,[to.name]) yield node as ys
return count(xs) + count(ys) + " nodes updated"

#NLP entity extraction process:

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
   WHERE not(entity.metadata.wikipedia_url is null)
   MATCH (wp:WikipediaPage {uri: entity.metadata.wikipedia_url})
   MERGE (node)-[:parla_di]->(wp)",
  {batchMode: "BATCH_SINGLE", batchSize: 10, params: {key: $key}})
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;


#SEMANTICH SEARCH:

MATCH (c:Category {name: "drug"})
CALL n10s.inference.nodesInCategory(c, {
	inCatRel: "ABOUT",
    subCatRel: "SUB_CAT_OF"
})
YIELD node
MATCH (node)<-[:parla_di]-(post)
RETURN DISTINCT post.id, post.caption, collect(n10s.rdf.getIRILocalName(node.uri)) as explicitTopics