from app.utils.services.tool_manager import ToolManager
from app.configuration import TestingConfig
from pathlib import Path
import yaml
import pytest

class TestToolManager:
    """Unit tests for ToolManager class."""


    def test_tools_list(self):
        """Check that tools_list() correctly returns all available tool folders."""
        tools_path = TestingConfig.TOOLS_DIRECTORY
        complete_path = Path(tools_path)
        expected_tools = ['snscrape-invalid', 'snscrape-invalid-image', 'snscrape-telegram']
        tool_list = ToolManager.tools_list(complete_path)
        
        assert sorted(tool_list) == sorted(expected_tools), (f"Tools mismatch:\n Expected: {expected_tools}\n Got: {tool_list}")
    
        
    def test_tool_detail(self):
        """Check that read_tool_config() loads valid configs and handles errors properly."""
        tools_path = Path(TestingConfig.TOOLS_DIRECTORY)
        tool_name = "snscrape-telegram"
        expected_path = tools_path / tool_name / f"{tool_name}.yml"
        with open(expected_path, "r") as f:
            expected_dict = yaml.safe_load(f)

        config_dict = ToolManager.read_tool_config(tools_path, "snscrape-telegram")
        
        # 1) Compare expected and actual configuration content
        assert config_dict == expected_dict, (
            f"Configuration mismatch for tool '{tool_name}':\n"
            f"Expected: {expected_dict}\nGot: {config_dict}")

        # 2) tool folder or YAML file does not exist
        with pytest.raises((FileNotFoundError)) as excinfo:
            ToolManager.read_tool_config(tools_path, "invalid")
        assert f"Configuration file not found: {tools_path}" in str(excinfo.value)

        # 3) YAML file exists but is malformed or invalid
        with pytest.raises((FileNotFoundError, ValueError, yaml.YAMLError)) as excinfo:
            ToolManager.read_tool_config(tools_path, "snscrape-invalid")
        assert f"Error parsing YAML file {tools_path}" in str(excinfo.value)
