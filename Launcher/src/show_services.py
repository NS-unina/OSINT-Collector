import sys
from .yaml_services import *

def show_usage():

    tools = read_compose_services()

    print("Usage:")
    print("    launcher.py <tool> -i <input>")
    print("\nParameters:")
    print("    <tool>: Choose a tool from options:", ", ".join(tools))
    print("    -i <input>: Specify the input as a string.")
    print("\nExample:")
    print("    python launcher.py instaloader -i uninait")
    
    sys.exit(0)

def show_error(error: str):
    print("[LauncherError] {}".format(error))
    sys.exit(1)

