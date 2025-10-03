from flask import Blueprint


views_bp = Blueprint('views', __name__)


@views_bp.route("/tools/<tool>")
def tool_details_help(tool: str):
    """
    Gives the help message for a specific tool
    """
    return "<p>It Works!</p>"


@views_bp.route("/tools")
def tools_help():
    """
    Gives the tool list
    """
    return "<p>It Works!</p>"


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
