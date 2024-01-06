"""
Launcher used interactively by user
"""

from src.services.show_services import read_tool_config
from src.globals import tools


def interactive_launcher():
    """
    Launcher used interactively by user
    """

    tool_list = tools()

    for index, elem in enumerate(tool_list):
        print(f"[{index}] {elem}")

    tool_index = int(input("Select tool (integer): "))

    tool = tool_list[tool_index]
    tool_config = read_tool_config(tool)

    input_strings = []
    for item in tool_config.inputs:
        input_strings.append(
            input(f"Insert {item.key} ({item.description}): ")
        )

    # Launch tool
    return tool_list[tool_index], input_strings
