import argparse
from tool_manager import ToolManager
from tool_selector import ToolSelector

def main():
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password"

    tool_manager = ToolManager(uri, username, password)
    tool_selector = ToolSelector(tool_manager)

    parser = argparse.ArgumentParser(description='Best-fit algorithm to find the best OSINT tool!')
    parser.add_argument('-a', '--add-tool', action='store_true', required=False, help='Add a new tool to the database.')
    parser.add_argument('-y', '--yaml-file', type=str, required=False, help='Add a new tool to the database using a YAML file.')
    parser.add_argument('-r', '--remove-tool', type=str, required=False, help='Remove a tool from the database.')
    parser.add_argument('-s', '--select-tool', action='store_true', required=False, help='Select a tool from the database.')
    parser.add_argument('-p', '--platform', type=str, required=False, help='The platform on which runs the tool.')
    parser.add_argument('-i', '--input', type=str, action='append', required=False, help='Input parameters of the tool.')
    parser.add_argument('-o', '--output', type=str, action='append', required=False, help='Output parameter of the tool.')

    args = parser.parse_args()

    if args.add_tool:
        tool_manager.add_tool(args.add_tool, args.platform, args.input, args.output)
    elif args.remove_tool:
        tool_manager.remove_tool(args.remove_tool)
    elif args.select_tool:
        tool_selector.select_tool(args)
    elif args.yaml_file:
        tool_manager.add_tool_from_yaml(args.yaml_file)
    else:
        print("Please provide at least one parameter.")

    tool_manager.close()

if __name__ == "__main__":
    main()
