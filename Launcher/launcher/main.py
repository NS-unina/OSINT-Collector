#!/usr/bin/env python3

"""Main file"""

import logging
from flask import Flask, request
from src.globals import Globals
from src.launcher import Launcher
from flask_cors import CORS
# from src.starter import Starter

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    server = Flask(__name__)
    CORS(server)

    @server.route("/help")
    def help_message():
        """Help message"""
        return Globals.help_message(), 200

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
