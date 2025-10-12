from app.utils.models.tool_config import ToolConfig
from app.utils.services.tool_manager import ToolManager
from app.utils.services.docker_service import DockerServices
from flask import Blueprint, request, jsonify, current_app
import yaml


views_bp = Blueprint('views', __name__)


@views_bp.route("/tools/<tool>", methods=['GET'])
def tool_details_help(tool: str):
    """Gives the help message for a specific tool"""
    try:
        tools_base_path = current_app.config.get("TOOLS_DIRECTORY")
        tool_config = ToolManager.read_tool_config(tools_base_path, tool)
        return tool_config, 200
    except FileNotFoundError:
        return jsonify({"error": f"Configuration file for tool '{tool}' not found."}), 404
    except yaml.YAMLError:
        return jsonify({"error": f"Configuration file for tool '{tool}' is invalid."}), 500


@views_bp.route("/tools", methods=['GET'])
def tools_help():
    """Gives the tool list"""
    return ToolManager.tools_list(current_app.config["TOOLS_DIRECTORY"]), 200


# curl -X POST http://127.0.0.1:5000/launch -H "Content-Type: application/json" -d '{"tool": "instaloader", "feature_key": "download-public-profile", "inputs": {"CHANNEL": "ciccio"}}'
@views_bp.route("/launch", methods=['POST'])
def launch():
    """Tool Launcher"""
    tool_name = request.json["tool"] 
    feature_key = request.json["feature_key"]
    inputs = request.json["inputs"]

    try:
        tools_base_path = current_app.config.get("TOOLS_DIRECTORY")
        tool_dict = ToolManager.read_tool_config(tools_base_path, tool_name)
        tool = ToolConfig(tool_dict)
    except FileNotFoundError:
        return jsonify({"error": f"Configuration file for tool '{tool_name}' not found."}), 404
    except yaml.YAMLError:
        return jsonify({"error": f"Configuration file for tool '{tool_name}' is invalid."}), 500
    
    try:
        feature = tool.get_feature(feature_key)
    except ValueError:
        return jsonify({"error": f"Provided feature_key '{feature_key}' does not exist for tool '{tool_name}'"}), 404
    if not tool.input_validation(feature_key, inputs):
        return jsonify({"error": f"'{inputs}' is not a valid input key."}), 404
    
    docker_client = DockerServices()
    
    try:
        docker_client.pull_image(tool.image)
    except Exception as e:
        return jsonify({"error": f"Failed to pull image: {tool.image}"}), 500
    
    entrypoint = feature.replace_input_in_command(inputs)
    # TODO: Manage execution
    docker_client.run_tool_container(tool.image, current_app.config["OUTOUT_DIRECTORY"], entrypoint)
    
    return jsonify({"status": "success", "tool": tool_name, "feature_key": feature_key, "entrypoint": entrypoint,}), 200
        

@views_bp.route("/", methods=['GET'])
def start():
    """Index page"""
    return "<p>It Works!</p>"
