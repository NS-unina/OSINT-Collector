class ToolSelector:
    def __init__(self, tool_manager):
        self.tool_manager = tool_manager
    
    def get_parameters(self):
        output_parameters = []

        with self.tool_manager.driver.session() as session:
            query = "MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:PRODUCES]->(o:Resource) RETURN DISTINCT o.name as output"
            result = session.run(query)
            output_parameters = [record["output"] for record in result.data()]
            
            query = "MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) RETURN DISTINCT i.name as output"
            result = session.run(query)
            input_parameters = [record["output"] for record in result.data()]

        return output_parameters, input_parameters
    
    def get_capabilities(self):
        capabilities = []

        with self.tool_manager.driver.session() as session:
            query = "MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability) RETURN DISTINCT c.name as output"
            result = session.run(query)
            capabilities = [record["output"] for record in result.data()]

        return capabilities
    
    def get_required_inputs(self, tools, capabilities_params):

        capabilities = capabilities_params
        if not isinstance(capabilities, list):
            capabilities = [capabilities]

        print(tools)
        with self.tool_manager.driver.session() as session:
            #query = f"MATCH (t:Tool)-[u:USES]->(i:Input) WHERE ANY(substring IN {tools} WHERE t.name CONTAINS substring) RETURN t as tool, COLLECT(i) as input"
            query = f"MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) WHERE ANY(substring IN {capabilities} WHERE c.name CONTAINS substring) RETURN t as tool, COLLECT(i) as input"
            print(query + "\n")
            result = session.run(query)
            data = result.data()
            print(data)

        return data
    
    def select_tool(self, args):
        data = None
        
        with self.tool_manager.driver.session() as session:
            if args.platform and args.input and args.output:
                if len(args.input) == 1 and len(args.output) == 1:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) WHERE t.platform CONTAINS '{args.platform}' AND o.name CONTAINS '{args.output[0]}' AND i.name CONTAINS '{args.input[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")

            elif args.platform and args.input:
                if len(args.input) == 1:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) WHERE p.name CONTAINS '{args.platform}' AND i.name CONTAINS '{args.input[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")

            elif args.platform and args.output:
                if len(args.output) == 1:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:PRODUCES]->(o:Resource) WHERE p.name CONTAINS '{args.platform[0]}' AND o.name CONTAINS '{args.output[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")

            elif args.input and args.output:
                if len(args.input) == 1 and len(args.output) == 1:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) WHERE i.name CONTAINS '{args.input[0]}' AND o.name CONTAINS '{args.output[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")

            elif args.input:
                query = f"MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource) WHERE ANY(substring IN {args.input} WHERE i.name CONTAINS substring) RETURN DISTINCT t.name as output"
                result = session.run(query)
                data = result.data()
                if data:
                    for record in data:
                        tool = record["output"]
                        print(f"Tool name: {tool}")
                else:
                    print("No tool available!")

            elif args.output:
                query = f"MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:PRODUCES]->(o:Resource) WHERE ANY(substring IN {args.output} WHERE o.name CONTAINS substring) RETURN DISTINCT t.name as output"
                result = session.run(query)
                data = result.data()
                if data:
                    for record in data:
                        tool = record["output"]
                        print(f"Tool name: {tool}")
                else:
                    print("No tool available!")

            elif args.platform:
                query = f"MATCH (t:Tool)-[:RUNS_ON]->(p:Platform) WHERE p.name CONTAINS '{args.platform}' RETURN DISTINCT t.name as output"
                result = session.run(query)
                data = result.data()
                if data:
                    for record in data:
                        tool = record["output"]
                        print(f"Tool name: {tool}")
                else:
                    print("No tool available!")

            else:
                print("Please provide at least one parameter.")

        return data
    
    def select_too_by_capabilities(self, capabilities_params):
        data = None
        
        with self.tool_manager.driver.session() as session:

            capabilities = capabilities_params
            if not isinstance(capabilities, list):
                capabilities = [capabilities]

            if capabilities:
                query = f"MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability) WHERE ANY(substring IN {capabilities} WHERE c.name CONTAINS substring) RETURN DISTINCT t.name as output"
                result = session.run(query)
                data = result.data()
                if data:
                    for record in data:
                        tool = record["output"]
                        print(f"Tool name: {tool}")
                else:
                    print("No tool available!")

            else:
                print("Please provide at least one parameter.")

        return data