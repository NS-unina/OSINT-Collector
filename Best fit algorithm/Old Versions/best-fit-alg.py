import argparse
from neo4j import GraphDatabase

def main(args):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    
    with driver.session() as session:
        
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
            query = f"MATCH (t:Tool)-[:RUNS_ON]->(p:Platform) WHERE p.name = '{args.platform}' RETURN DISTINCT t.name as output"
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
        
    #print(args.output)
    #print(args.platform)
    #print(args.capability)

    driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Best-fit algorithm to find the best OSINT tool!')
    parser.add_argument('-p', '--platform', type=str, required=False, help='The platform on which runs the tool.')
    parser.add_argument('-i', '--input', type=str, action='append', required=False, help='Input parameters of the tool. This option can be specified multiple times to request multiple inputs.')
    parser.add_argument('-c', '--capability', type=str, action='append', required=False, help='Capabilities required from the tool. This option can be specified multiple times to request multiple capabilities.')
    parser.add_argument('-o', '--output', type=str, action='append', required=False, help='Output parameter of the tool. This option can be specified multiple times to request multiple outputs.')

    args = parser.parse_args()
    main(args)
