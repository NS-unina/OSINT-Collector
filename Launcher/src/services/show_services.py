"""
Show Services to properly manage prints
"""

import sys
from src.services.yaml_services import read_tool_config
from src.globals import tools


def show_usage():
    """
    Print the launcher usage message
    """

    print("Usage:")
    print("    launcher.py <tool> -i <input1> <input2> ...")
    print("\nParameters:")
    print("    <tool>: Choose a tool from options:", ", ".join(tools()))
    print("    -i <input>: Specify the input list.")
    print("\nExample:")
    print("    python launcher.py the-harvester -i unina.it duckduckgo")

    sys.exit(0)


def show_tool_usage(tool: str):
    """
    Print the tool usage message
    """

    tool_config = read_tool_config(tool)

    input_key = map(lambda item: item.key, tool_config.inputs)
    inputs = " ".join(input_key)

    print("Usage:")
    print(f"    launcher.py {tool} -i {inputs}")
    print("\nInputs:")

    for item in tool_config.inputs:
        print(f"    {item.key}: {item.description}")

    sys.exit(0)


def show_error(error: str):
    """
    Print error message
    """

    print(f"[LauncherError] {error}")
    sys.exit(1)
