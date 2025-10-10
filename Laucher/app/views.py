from app.utils.models.tool_config import ToolConfig
from app.utils.services.tool_manager import ToolManager
from flask import Blueprint, request, jsonify
import yaml


views_bp = Blueprint('views', __name__)


@views_bp.route("/tools/<tool>", methods=['GET'])
def tool_details_help(tool: str):
    """
    Gives the help message for a specific tool
    """
    try:
        tool_config = ToolManager.read_tool_config(tool)
        return tool_config, 200
    except FileNotFoundError:
        return jsonify({"error": f"Configuration file for tool '{tool}' not found."}), 404
    except yaml.YAMLError:
        return jsonify({"error": f"Configuration file for tool '{tool}' is invalid."}), 500

@views_bp.route("/tools", methods=['GET'])
def tools_help():
    """
    Gives the tool list
    """

    return ToolManager.tools_list(), 200


# curl -X POST http://127.0.0.1:5000/launch -H "Content-Type: application/json" -d '{"tool": "instaloader", "feature_key": "download-public-profile", "inputs": {"CHANNEL": "ciccio"}}'
@views_bp.route("/launch", methods=['POST'])
def launch():
    """
    Launcher
    """

    tool_image = request.json["tool"] 
    feature_key = request.json["feature_key"]
    inputs = request.json["feature_key"]

    try:
        dict_tool = ToolManager.read_tool_config(tool_image)
        tool_config = ToolConfig(dict_tool)
        print(tool_config.toolName)
        # print(tool_config[tool_image]["entrypoints"][0])
        return "<p>It Works!</p>", 200
    except FileNotFoundError:
        return jsonify({"error": f"Configuration file for tool '{tool_image}' not found."}), 404
    except yaml.YAMLError:
        return jsonify({"error": f"Configuration file for tool '{tool_image}' is invalid."}), 500


@views_bp.route("/")
def start():
    """
    Index page
    """

    return "<p>It Works!</p>"
