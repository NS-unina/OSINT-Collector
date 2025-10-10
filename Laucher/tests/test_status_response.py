import os 
import yaml
import random
from pathlib import Path


class TestStatusResponse:
    
    
    def test_index_response(self, client):
        # 200 OK
        response = client.get("/")
        assert response.status_code == 200

    
    def test_tools_list_response(self, client, app):
        # 200 OK
        response = client.get("/tools")
        assert response.status_code == 200  

        # Expected JSON list of tools
        data = response.get_json()
        assert isinstance(data, list)

        # Compare both lists (sorted to avoid order issues)
        expected_tools = os.listdir(app.config["TOOLS_DIRECTORY"])
        assert sorted(data) == sorted(expected_tools), (
            f"Tools mismatch:\n Expected: {expected_tools}\n Got: {data}")


    def test_tool_positive_description_response(self, client, app):
        tools_dir = os.listdir(app.config["TOOLS_DIRECTORY"])
        tool_selected = random.choice(tools_dir)

        # 200 OK
        response = client.get(f"/tools/{tool_selected}")
        assert response.status_code == 200  

        # Expected JSON list of tools
        data = response.get_json()
        assert isinstance(data, dict)

        # Compare both yaml
        tool_config_path = Path(app.config["TOOLS_DIRECTORY"]) / tool_selected / f"{tool_selected}.yml"
        with open(tool_config_path) as file:
            expected_tools = yaml.safe_load(file)
        assert sorted(data) == sorted(expected_tools), (
            f"Tools mismatch:\n Expected: {expected_tools}\n Got: {data}")
