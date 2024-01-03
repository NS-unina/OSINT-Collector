import yaml
from .constants import *
from .show_services import *

def read_compose_services():
    services_array = []

    try:
        with open(DOCKER_COMPOSE_PATH, 'r') as file:
            # Load YAML content
            data = yaml.safe_load(file)

            # Get services name
            if 'services' in data:
                services_array = list(data['services'].keys())
                services_array.remove('common')

    except FileNotFoundError:
        show_error("File {} not found".format(DOCKER_COMPOSE_PATH))
    except yaml.YAMLError as e:
        show_error("Error while parsing YAML file: {}".format(e))

    return services_array

def read_tool_config(tool: str):
    file_path = './tools/{}/{}.yml'.format(tool, tool)
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

        entrypoint = data.get(tool, {}).get('entrypoint', '')
        inputs = data.get(tool, {}).get('inputs', [])

        return entrypoint, inputs