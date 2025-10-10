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
        expected_tools = ["snscrape", "snscrape-invalid"]
        assert sorted(data) == expected_tools, (f"Tools mismatch:\n Expected: {expected_tools}\n Got: {data}")

    
    def test_tool_positive_description_response(self, client, app):
        tool_selected = "snscrape"

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
        assert sorted(data) == sorted(expected_tools), (f"Tools mismatch:\n Expected: {expected_tools}\n Got: {data}")

        # File not found test
        response = client.get(f"/tools/this_tool_does_not_exist")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'this_tool_does_not_exist' not found." in data["error"]

        # Invalid yaml
        response = client.get(f"/tools/snscrape-invalid")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'snscrape-invalid' is invalid." in data["error"]
