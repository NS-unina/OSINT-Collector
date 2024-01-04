from ..services.show_services import *
from ..globals import *

def interactive_launcher():

    for index, elem in enumerate(TOOLS):
        print("[{}] {}".format(index, elem))
    
    tool_index = int(input("Select tool (integer): "))

    tool = TOOLS[tool_index]
    tool_config = read_tool_config(tool)

    input_strings = []
    for item in tool_config.inputs:    
        input_strings.append(input("Insert {} ({}): ".format(item.key, item.description)))

    # Launch tool
    return TOOLS[tool_index], input_strings