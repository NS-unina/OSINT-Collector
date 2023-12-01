class ToolSelector:
    def __init__(self, tool_manager):
        self.tool_manager = tool_manager
    
    def get_parameters(self):
        output_parameters = []

        with self.tool_manager.driver.session() as session:
            query = "MATCH (t:Tool)-[:PRODUCES]->(r:Resource) RETURN DISTINCT r.name as output"
            result = session.run(query)
            output_parameters = [record["output"] for record in result.data()]
            
            query = "MATCH (t:Tool)-[:USES]->(i:Input) RETURN DISTINCT i.name as output"
            result = session.run(query)
            input_parameters = [record["output"] for record in result.data()]

        return output_parameters, input_parameters
    
    def get_required_inputs(self, tools):

        with self.tool_manager.driver.session() as session:
            query = f"MATCH (t:Tool)-[u:USES]->(i:Input) WHERE ANY(substring IN {tools} WHERE t.name CONTAINS substring) RETURN t as tool, COLLECT(i) as input"
            result = session.run(query)
            data = result.data()

        return data
    
    def select_tool(self, args):
        data = None
        
        with self.tool_manager.driver.session() as session:
            if args.platform and args.input and args.output:
                #print(args.platform, args.input, args.output)
                if len(args.input) == 1 and len(args.output) == 1:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:USES]->(i:Input) WHERE t.platform CONTAINS '{args.platform}' AND o.name CONTAINS '{args.output[0]}' AND i.name CONTAINS '{args.input[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:USES]->(i:Input) WHERE t.platform CONTAINS '{args.platform}' AND ANY(substring IN {args.output} WHERE o.name CONTAINS substring) AND ANY(substring IN {args.input} WHERE i.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.platform and args.input:
                #print(args.platform, args.input, args.output)
                if len(args.input) == 1:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:USES]->(i:Input) WHERE p.name CONTAINS '{args.platform}' AND i.name CONTAINS '{args.input[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:USES]->(i:Input) WHERE p.name CONTAINS '{args.platform}' AND ANY(substring IN {args.input} WHERE i.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.platform and args.output:
                #print(args.platform, args.input, args.output)
                if len(args.output) == 1:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:PRODUCES]->(o:Resource) WHERE p.name CONTAINS '{args.platform[0]}' AND o.name CONTAINS '{args.output[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (p:Platform)<-[:RUNS_ON]-(t:Tool)-[:PRODUCES]->(o:Resource) WHERE p.name CONTAINS '{args.platform[0]}' AND ANY(substring IN {args.output} WHERE o.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.input and args.output:
                #print(args.platform, args.input, args.output)
                if len(args.input) == 1 and len(args.output) == 1:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:USES]->(i:Input) WHERE i.name CONTAINS '{args.input[0]}' AND o.name CONTAINS '{args.output[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (o:Resource)<-[:PRODUCES]-(t:Tool)-[:USES]->(i:Input) WHERE ANY(substring IN {args.input} WHERE i.name CONTAINS substring) AND ANY(substring IN {args.output} WHERE o.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.input:
                #print(args.platform, args.input, args.output)
                if len(args.input) == 1:
                    query = f"MATCH (t:Tool)-[:USES]->(i:Input) WHERE i.name CONTAINS '{args.input[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (t:Tool)-[:USES]->(i:Input) WHERE ANY(substring IN {args.input} WHERE i.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.output:
                #print(args.platform, args.input, args.output)
                if len(args.output) == 1:
                    query = f"MATCH (t:Tool)-[:PRODUCES]->(r:Resource) WHERE r.name CONTAINS '{args.output[0]}' RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
                else:
                    query = f"MATCH (t:Tool)-[:PRODUCES]->(r:Resource) WHERE ANY(substring IN {args.output} WHERE r.name CONTAINS substring) RETURN DISTINCT t.name as output"
                    result = session.run(query)
                    data = result.data()
                    if data:
                        for record in data:
                            tool = record["output"]
                            print(f"Tool name: {tool}")
                    else:
                        print("No tool available!")
            elif args.platform:
                #print(args.platform, args.input, args.output)
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