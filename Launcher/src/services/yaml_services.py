"""
YAML Services to properly manage yaml file
"""

import yaml
from src.models.tool_config import ToolConfig


def read_tool_config(tool: str):
    """
    Read the configuration yaml file relative to the provided
    tool to retrive the tool informations
    """

    file_path = f'./tools/{tool}/{tool}.yml'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Load YAML content
            data = yaml.safe_load(file)

            # Object convertion
            return ToolConfig(name=tool, data=data)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
    return None
