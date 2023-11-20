from flask import Flask, render_template, request
import argparse
from neo4j import GraphDatabase

app = Flask(__name__)

def query_neo4j(args):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    data = None

    with driver.session() as session:
        
        print(args.platform, args.input, args.output)
        if args.platform and args.input and args.output:
            print(args.platform, args.input, args.output)
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
            query = f"MATCH g=(t:Tool)-[:RUNS_ON]->(p:Platform) WHERE p.name = '{args.platform}' RETURN DISTINCT t.name as output, g"
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

    driver.close()

    return data

def get_parameters():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

    output_parameters = []

    with driver.session() as session:
        query = "MATCH (t:Tool)-[:PRODUCES]->(r:Resource) RETURN DISTINCT r.name as output"
        result = session.run(query)
        output_parameters = [record["output"] for record in result.data()]
        
        query = "MATCH (t:Tool)-[:USES]->(i:Input) RETURN DISTINCT i.name as output"
        result = session.run(query)
        input_parameters = [record["output"] for record in result.data()]

    driver.close()

    return output_parameters, input_parameters

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    output_parameters, input_parameters = get_parameters();

    if request.method == 'POST':
        # Estrai i parametri dalla richiesta WebUI
        platform = request.form.get('platform')
        input_params = request.form.getlist('input')
        capability_params = request.form.get('capability')
        output_params = request.form.getlist('output')

        # Costruisci un oggetto argparse.Namespace
        args = argparse.Namespace(platform=platform, input=input_params, capability=capability_params, output=output_params)

        # Esegui la query Neo4j con i parametri forniti
        data = query_neo4j(args)

    return render_template('index.html', data=data, output_parameters=output_parameters, input_parameters=input_parameters)

if __name__ == '__main__':
    app.run(debug=True)