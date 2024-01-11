import argparse
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from tool_manager import ToolManager
from tool_selector import ToolSelector

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173"}})

@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html')

@app.route('/add', methods=['GET', 'POST'])
def add_tool():
    addResult = None
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'yaml_file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['yaml_file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith(('.yaml', '.yml')):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            addResult = tool_manager.add_tool_from_yaml(file_path)
            print(addResult)
            
            os.remove(file_path)
    
    return render_template('add.html', result=addResult)

@app.route('/remove', methods=['GET', 'POST'])
def remove_tool():
    tools = tool_manager.get_tools();
    removeResult = None;
    
    if request.method == 'POST':
        remove_tool = request.form.get('remove_tool')
        print(remove_tool)
        removeResult = tool_manager.remove_tool(remove_tool)
        tools = tool_manager.get_tools();

    return render_template('remove.html', tools=tools, result=removeResult)

@app.route('/process', methods=['GET', 'POST'])
def run_tools():
    data = None
    
    if request.method == 'POST':
        # Estrai i parametri dalla richiesta WebUI
        data = request.form.get('json_data')
        print(data)

    return render_template('index2.html')


@app.route('/select', methods=['GET', 'POST'])
def select_tool():
    data = None
    platform = None
    output_parameters, input_parameters = tool_selector.get_parameters();
    capabilities = tool_selector.get_capabilities(platform);
    
    if request.method == 'POST':
        # Estrai i parametri dalla richiesta WebUI
        data = request.json
        platform = data.get('platform')
        capabilities = data.get('capabilities')
        print(platform)
        print(capabilities)
        platform = request.form.get('platform')
        input_params = request.form.getlist('input')
        capability_params = request.form.get('capabilities')
        output_params = request.form.getlist('output')

        # Costruisci un oggetto argparse.Namespace
        args = argparse.Namespace(platform=platform, input=input_params, capability=capability_params, output=output_params)

        # Esegui la query Neo4j con i parametri forniti
        #data = tool_selector.select_tool(args)
        data = tool_selector.select_too_by_capabilities(capabilities)
        tools = [record["output"] for record in data]
        required = tool_selector.get_required_inputs(tools, capabilities);
        print(required);
        
        return required
        #return render_template('required_inputs.html', tools=required)

    return render_template('select.html', data=data, capability_parameters=capabilities, output_parameters=output_parameters, input_parameters=input_parameters)

@app.route('/get_capabilities', methods=['GET', 'POST'])
def get_capabilities():
    platform = None
    if request.method == 'GET':
        platform = request.args.get('platform', None)
    capability_parameters = tool_selector.get_capabilities(platform)
    # Costruisci l'oggetto JSON di risposta utilizzando jsonify
    response = {'capability_parameters': capability_parameters}

    return response

if __name__ == '__main__':
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password"

    tool_manager = ToolManager(uri, username, password)
    tool_selector = ToolSelector(tool_manager)
    
    app.run(debug=True)