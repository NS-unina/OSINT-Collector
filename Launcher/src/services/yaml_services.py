"""
Module containing class to properly manage yaml file
"""

import logging
import yaml
from src.models.tool_config import ToolConfig


class _Exceptions:
    """Manage yaml services errors"""

    unable_to_read_file = ("An exception occured while reading "
                           "file %s")

    unable_to_parse_file = ("An exception occured while parsing "
                            "file %s: %s")


class YAMLServices:
    """
    Facilitator class to properly manage yaml file
    """

    _log = logging.getLogger(__name__)

    @staticmethod
    def read_tool_config(tool: str):
        """
        Read the configuration yaml file relative to the provided
        tool to retrive the tool informations
        """

        file_path = f'./tools/{tool}/{tool}.yml'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Load YAML content
                data = yaml.safe_load(file)

                # Object convertion
                return ToolConfig(name=tool, data=data)

        except FileNotFoundError:
            YAMLServices._log.error(_Exceptions.unable_to_read_file, file_path)
            exit(1)

        except yaml.YAMLError as e:
            YAMLServices._log.error(_Exceptions.unable_to_parse_file,
                                    file_path, e)
            exit(1)
        return None
