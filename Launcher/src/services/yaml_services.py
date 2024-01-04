import yaml
from ..globals import *
from ..models.tool_config import *
from ..models.tool_input import *

def read_compose_services():
    services_array = []

    try:
        with open('./docker-compose.yml', 'r') as file:
            # Load YAML content
            data = yaml.safe_load(file)

            # Get services name
            if 'services' in data:
                services_array = list(data['services'].keys())
                services_array.remove('common')

    except FileNotFoundError:
        print(f"File {'./docker-compose.yml'} not found")
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML file: {e}")

    return services_array

def read_tool_config(tool: str):
    
    file_path = './tools/{}/{}.yml'.format(tool, tool)

    try:
        with open(file_path, 'r') as file:
            # Load YAML content
            data = yaml.safe_load(file)

            # Object convertion
            return ToolConfig(name=tool, data=data)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
    return None

