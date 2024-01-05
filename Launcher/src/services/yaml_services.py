import yaml
from ..globals import *
from ..models.tool_config import *
from ..models.tool_input import *

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

