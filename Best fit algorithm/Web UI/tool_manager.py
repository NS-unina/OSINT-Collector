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
        
    def get_tools(self):
        tools = []

        with self.driver.session() as session:
            query = "MATCH (t:Tool) RETURN DISTINCT t.name as output"
            result = session.run(query)
            tools = [record["output"] for record in result.data()]

        return tools

    #Add a tool to the database
    def add_tool(self, tool_name, platform, capabilities):
        with self.driver.session() as session:
            
            input_params = []
            output_params = []
            query = f"""MERGE (t:Tool {{name: '{tool_name}', platform: '{platform}'}})
            MERGE (t)-[:RUNS_ON]->(p:Platform {{name: '{platform}'}})
            \n"""
            for c, params in capabilities.items():
                #print(c, params['input'], params['output'])
                input_params = params['input']
                output_params = params['output']
                if not isinstance(input_params, list):
                    input_params = [input_params]
                if not isinstance(output_params, list):
                    output_params = [output_params]
                query = query + f"""MERGE ({c}:Capability {{name: '{c}'}})
                MERGE (t)-[:HAS_CAPABILITY]->({c})
                
                WITH {c}, t, {input_params} AS inputs
                UNWIND inputs AS input
                MATCH (i:Resource {{name: input}})-[*]->(:Resource {{name: '{platform}'}})
                FOREACH (ignore IN CASE WHEN i IS NOT NULL THEN [1] ELSE [] END | MERGE ({c})-[:NEEDS]->(i))
                
                WITH {c}, t, {output_params} AS outputs
                UNWIND outputs AS output
                MATCH (o:Resource {{name: output}})-[*]->(:Resource {{name: '{platform}'}})
                FOREACH (ignore IN CASE WHEN o IS NOT NULL THEN [1] ELSE [] END | MERGE ({c})-[:PRODUCES]->(o))
                """
                
            #print(query)
            result = session.run(query)
            
            # Checks if there are modified nodes
            records_modified = result.consume().counters.nodes_created
            
            if records_modified == 0:
                print(f"{tool_name} already exists")
                return False
            else:
                print(f"{tool_name} has been added!")
                return True

    #Add a tool to the database using a YAML file
    def add_tool_from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

            tool_name = data.get('name')
            platform = data.get('platform')
            capabilities = data.get('capabilities', [])

            if tool_name and platform:
                #for capability, params in capabilities.items():
                #    print(capability, params['input'], params['output'])
                return self.add_tool(tool_name, platform, capabilities)
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
                return False
            else:
                print(f"{tool_name} has been deleted!")
                return True