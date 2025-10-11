import yaml
import json
from pathlib import Path


class TestStatusResponse:


    def test_index_response(self, client):
        """Test that the index route responds correctly."""
        # 200 OK 
        response = client.get("/")
        assert response.status_code == 200


    def test_disallowed_methods(self, client):
        """Test that all methods except GET return 405 Method Not Allowed."""
        disallowed_methods = ["POST", "PUT", "PATCH", "DELETE"]
        paths = ["/", "/tools", "/tools/invalid"]

        for path in paths:
            for method in disallowed_methods:
                response = client.open(path, method=method)
                assert response.status_code == 405, f"{method} should return 405"


    def test_tools_list_response(self, client):
        """Test that the /tools endpoint returns the correct list of available tools."""
        # 200 OK
        response = client.get("/tools")
        assert response.status_code == 200  

        # Expected JSON list of tools
        data = response.get_json()
        assert isinstance(data, list)

        # Compare both lists (sorted to avoid order issues)
        expected_tools = ['snscrape-invalid', 'snscrape-invalid-image', 'snscrape-telegram']
        assert sorted(data) == expected_tools, (f"Tools mismatch:\n Expected: {expected_tools}\n Got: {data}")

    
    def test_tool_description_valid_response(self, client, app):
        """Test that /tools/<tool> returns valid configuration data for existing tools,
        and returns appropriate error messages for non-existent or invalid ones.
        """
        # 1) Test a valid tool request
        tool_selected = "snscrape-telegram"

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

        # 2) Test non-existent tool (should return 404)
        # File not found test
        response = client.get(f"/tools/this_tool_does_not_exist")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'this_tool_does_not_exist' not found." in data["error"]

        # 3) Test invalid YAML configuration (should return 500)
        # Invalid yaml
        response = client.get(f"/tools/snscrape-invalid")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'snscrape-invalid' is invalid." in data["error"]



    def test_launch_lauch(self, client):
        invalid_tool_payload = {
            "tool": "invalid",
            "feature_key": "download-messages",
            "inputs": {
                "CHANNEL": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(invalid_tool_payload),
            content_type="application/json")
        
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'invalid' not found." in data["error"]

        invalid_yaml_tool_payload = {
            "tool": "snscrape-invalid",
            "feature_key": "download-messages",
            "inputs": {
                "CHANNEL": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(invalid_yaml_tool_payload),
            content_type="application/json")
        
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Configuration file for tool 'snscrape-invalid' is invalid." in data["error"]

        invalid_feature_payload = {
            "tool": "snscrape-telegram",
            "feature_key": "invalid",
            "inputs": {
                "CHANNEL": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(invalid_feature_payload),
            content_type="application/json")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "Provided feature_key 'invalid' does not exist for tool 'snscrape-telegram'" in data["error"]

        invalid_feature_payload = {
            "tool": "snscrape-telegram",
            "feature_key": "download-messages",
            "inputs": {
                "INVALID": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(invalid_feature_payload),
            content_type="application/json")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "'{'INVALID': 'ilpost_official', 'RESULTS': 5}' is not a valid input key." in data["error"]

        invalid_input_payload = {
            "tool": "snscrape-invalid-image",
            "feature_key": "download-messages",
            "inputs": {
                "CHANNEL": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(invalid_input_payload),
            content_type="application/json")
        
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Failed to pull image: invalid" in data["error"]

        att_response =  {"entrypoint": "sh -c \"snscrape --jsonl --max-results 5 telegram-channel ilpost_official > /output/snscrape-telegram-ilpost_official.json\"",
            "feature_key": "download-messages",
            "status": "success",
            "tool": "snscrape-telegram"}
        
        valid_payload = {
            "tool": "snscrape-telegram",
            "feature_key": "download-messages",
            "inputs": {
                "CHANNEL": "ilpost_official",
                "RESULTS": 5
            }
        }

        response = client.post(
            "/launch",
            data=json.dumps(valid_payload),
            content_type="application/json")

        assert response.status_code == 200
        
        data = response.get_json()
        if data != att_response:
            print("\nExpected JSON:\n", json.dumps(att_response, indent=2))
            print("\nActual JSON:\n", json.dumps(data, indent=2))

        assert data == att_response, "Response JSON does not match expected output"