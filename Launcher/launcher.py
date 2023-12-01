#!/usr/bin/env python3

import sys
import subprocess

tools = {
    1: 'instaloader'
}

def show_usage():
    print("Usage: export INPUT=uninait && {} <tool>".format(sys.argv[0]))
    print("Available tools:", ", ".join(tools.values()))
    

def launch_tool(tool):
    try:
        subprocess.run(['docker-compose', '-f', './{}/docker-compose.yml'.format(tool), 'up', '-d'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching {tool}: {e}")

def interactive_main():
    print("Select the tool to launch:")
    for key, value in tools.items():
        print(f"[{key}] {value}")

    try:
        tool_number = int(input("Enter the number of the tool: "))
        selected_tool = tools.get(tool_number)

        if selected_tool:
            launch_tool(selected_tool)
        else:
            print("Invalid tool number. Please select a valid tool.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def headless_main():
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)

    # Primo argomento è l'immagine Docker
    image = sys.argv[1]

    if (image in tools.values()):
        launch_tool(image)
    else:
        print("Invalid input. Please enter a valid tool.")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_usage()
            sys.exit(0)

    if len(sys.argv) == 1:
        interactive_main()
    else:
        headless_main()
