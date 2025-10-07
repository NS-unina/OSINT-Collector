from app.utils.parser.yaml_parser import YAMLServices
from app.utils.services.tool_manager import ToolManager
from flask import Blueprint


views_bp = Blueprint('views', __name__)


@views_bp.route("/tools/<tool>", methods=['GET'])
def tool_details_help(tool: str):
    """
    Gives the help message for a specific tool
    """

    tool_config = ToolManager.read_tool_config(tool)    

    return tool_config, 200


@views_bp.route("/tools", methods=['GET'])
def tools_help():
    """
    Gives the tool list
    """

    return ToolManager.tools_list(), 200


@views_bp.route("/launch", methods=['POST'])
def launch():
    """
    Launcher
    """

    return "<p>It Works!</p>"


@views_bp.route("/")
def start():
    """
    Index page
    """

    return "<p>It Works!</p>"
