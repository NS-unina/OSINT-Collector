import sys
from ..services.show_services import *
from ..globals import *

def cmd_launcher():

    # Check invalid format
    if len(sys.argv) < 4:
        show_error("Invalid format")

    image = sys.argv[1]
    input_flag = sys.argv[2]
    inputs_str = sys.argv[3:]

    # Check if the tool is valid
    if (image not in tools()):
        show_error("Invalid tool")

    # Check if the input flag is present
    if input_flag != "-i":
        show_error("Invalid input")
    
    # Launch tool
    return image, inputs_str