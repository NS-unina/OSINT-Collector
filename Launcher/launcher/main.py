#!/usr/bin/env python3

"""Main file"""

import logging
import os
import shutil
from flask import Flask, request
from flask_cors import CORS
from src.globals import Globals
from src.launcher import Launcher
from src.services.yaml_services import YAMLServices
from src.services.docker_services import DockerServices
# from src.starter import Starter


def copy_conf_files(source_folder, destination_folder):
    """Function to copy all logstash conf file """

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.conf'):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file)
                # Copy the file to the destination folder
                shutil.copy(source_file_path, destination_file_path)
                print(f"Copied {source_file_path} to {destination_file_path}")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    server = Flask(__name__)
    CORS(server)

    @server.route("/tools")
    def tools_help():
        """Gives the tool list"""
        return Globals.tools(), 200

    @server.route("/tools/<tool>")
    def tool_details_help(tool: str):
        """
        Gives the help message for a specific tool
        """

        tool_config = YAMLServices.read_tool_config(tool)
        tool_json = tool_config.to_json()

        return tool_json, 200

    @server.route("/launch", methods=['POST'])
    def launch():
        """Launcher"""
        data = request.json

        _image = data.get("image")
        _entrypoint = data.get("entrypoint")
        _inputs = data.get("inputs")

        launcher = Launcher(_image, _entrypoint, _inputs)
        launcher.launch_tool()

        return "OK", 200

    copy_conf_files("./tools", "/tools_conf")
    server.run(host='0.0.0.0', port=5000)

    # Help Section

    # if Starter.check_for_help():
    #     print(Globals.help_message())
    #     exit(0)

    # if Starter.check_for_tool_help():
    #     print(Globals.help_tool_message())
    #     exit(0)

    # Launch Section

    # image, entrypoint, inputs_str = Starter.fetch_launcher_params()
    # launcher = Launcher(image, entrypoint, inputs_str)
    # launcher.launch_tool()
