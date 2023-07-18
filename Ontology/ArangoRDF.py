from arango import ArangoClient
import json

from arango_rdf import ArangoRDF

url = "http://localhost:8529/"
dbName = "OSINT"
username = "root"
password = "rootpassword"

# Connect to the db via the python-arango driver
db = ArangoClient(hosts=url).db(dbName, username, password, verify=True)

# Clean up existing data and collections
if db.has_graph("default_graph"):
    db.delete_graph("default_graph", drop_collections=True, ignore_missing=True)

# Initializes default_graph and sets RDF graph identifier (ArangoDB sub_graph)
# Optional: sub_graph (stores graph name as the 'graph' attribute on all edges in Statement collection)
# Optional: default_graph (name of ArangoDB Named Graph, defaults to 'default_graph',
#           is root graph that contains all collections/relations)
adb_rdf = ArangoRDF(db, sub_graph="Ontology/OSINT.owl")
print("initialized graph")
config = {"normalize_literals": False}  # default: False

# RDF Import
adb_rdf.init_rdf_collections(bnode="Blank")
print("initialized collections")

print("importing ontology...")
# Start with importing the ontology
# adb_rdf.import_rdf("Ontology/OSINT.owl", format="xml", config=config, save_config=True)
adb_rdf.import_rdf("Ontology/OSINT.owl", format="xml", config=config, save_config=True)
print("Ontology imported")





