from neo4j import GraphDatabase
import yaml

class ToolManager:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def close(self):
        self.driver.close()

    #Add a tool to the database
    def add_tool(self, tool_name, platform, input_params, output_params):
        with self.driver.session() as session:
            query = f"""MERGE (t:Tool {{name: '{tool_name}', platform: '{platform}'}})
            FOREACH (input IN {input_params} | MERGE (i:Input {{name: input}}) MERGE (t)-[:USES]->(i))
            FOREACH (output IN {output_params} | MERGE (o:Resource {{label: output}}) MERGE (t)-[:PRODUCES]->(o))
            FOREACH (platform IN CASE WHEN NOT '{platform}' IS NULL THEN ['{platform}'] ELSE [] END | MERGE (p:Platform {{name: platform}}) MERGE (t)-[:RUNS_ON]->(p));
            """
            result = session.run(query)
            
            # Checks if there are modified nodes
            records_modified = result.consume().counters.nodes_deleted
            
            if records_modified == 0:
                print(f"{tool_name} already exists")
            else:
                print(f"{tool_name} has been added!")

    #Add a tool to the database using a YAML file
    def add_tool_from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

            tool_name = data.get('name')
            platform = data.get('platform')
            input_params = data.get('input', [])
            output_params = data.get('output', [])

            if tool_name and platform:
                self.add_tool(tool_name, platform, input_params, output_params)
            else:
                print("Invalid YAML file format. Please make sure 'name' and 'platform' are specified.")

    def remove_tool(self, tool_name):
        with self.driver.session() as session:
            query = f"MATCH (t:Tool) WHERE t.name = '{tool_name}' DETACH DELETE t"
            result = session.run(query)
            
            # Checks if there are modified nodes
            records_modified = result.consume().counters.nodes_deleted
            
            if records_modified == 0:
                print(f"{tool_name} not found")
            else:
                print(f"{tool_name} has been deleted!")