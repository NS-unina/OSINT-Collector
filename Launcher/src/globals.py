"""
Module containing all the globally accessible propertins and functions
"""

import os


def tools():
    """Return the available tool"""
    complete_path = os.path.join(os.getcwd(), 'tools')
    path_content = os.listdir(complete_path)

    folders = []
    for elem in path_content:
        if os.path.isdir(os.path.join(complete_path, elem)):
            folders.append(elem)

    return folders
