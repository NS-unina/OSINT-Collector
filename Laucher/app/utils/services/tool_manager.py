import yaml
from pathlib import Path
from flask import current_app


class ToolManager:
    """Class containing all function required to manage tool configuration."""

    @staticmethod
    def tools_list(tools_path):
        """Return a list of available tools.

        This method retrieves the names of folders located within the 'tools'
        directory in the current working directory.

        Returns:
            list: A list containing the names of available tools (folders).
        """
        
        complete_path = Path(tools_path)

        folders = [p.name for p in complete_path.iterdir() if p.is_dir()]

        return folders
    

    @staticmethod
    def read_tool_config(tools_base_path: str, tool: str):
        """Reads the YAML configuration for a specific tool.

        Args:
            tool (str): The name of the tool whose config should be read.

        Returns:
            dict: Parsed YAML content as a dictionary.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            yaml.YAMLError: If the YAML content is invalid.
        """

        tool_config_path = Path.cwd() / tools_base_path / tool / f"{tool}.yml"

        if not tool_config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {tool_config_path}")

        try:
            with tool_config_path.open("r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {tool_config_path}: {e}")
