import sys
from .yaml_services import *

def show_usage():

    tools = read_compose_services()

    print("Usage:")
    print("    launcher.py <tool> -i <input1> <input2> ...")
    print("\nParameters:")
    print("    <tool>: Choose a tool from options:", ", ".join(tools))
    print("    -i <input>: Specify the input list.")
    print("\nExample:")
    print("    python launcher.py the-harvester -i unina.it duckduckgo")
    
    sys.exit(0)

def show_tool_usage(tool: str):

    tool_config = read_tool_config(tool)

    input_key = map(lambda item: item.key, tool_config.inputs)
    inputs = " ".join(input_key)

    print("Usage:")
    print("    launcher.py {} -i {}".format(tool, inputs))
    print("\nInputs:")

    for item in tool_config.inputs:
        print("    {}: {}".format(item.key, item.description))

    sys.exit(0)

def show_error(error: str):
    print("[LauncherError] {}".format(error))
    sys.exit(1)
