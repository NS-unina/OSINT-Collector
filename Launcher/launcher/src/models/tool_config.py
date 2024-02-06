"""
Tool Configuration Model
"""

from src.models.tool_input import ToolInput
from src.models.tool_entrypoint import ToolEntrypoint


class ToolConfig:
    """
    Tool Configuration Model
    """

    def __init__(self, name: str, data: dict):

        data = data[name]

        self.name = name
        self.description = data['description']

        self.entrypoints = []
        self.inputs = []

        for item in data['inputs']:

            tool_input = ToolInput(key=item['key'],
                                   description=item['description'],
                                   format_type=item['type'])

            self.inputs.append(tool_input)

        for item in data['entrypoints']:

            tool_entry = ToolEntrypoint(key=item['key'],
                                        description=item['description'],
                                        inputs=item['inputs'],
                                        command=item['command'])

            self.entrypoints.append(tool_entry)

    def __str__(self):

        name = f"name={self.name}"
        desc = f"description={self.description}"
        string = f"ToolConfig: {name}, {desc}"

        string += "\nInputs:\n"
        for item in self.inputs:
            string += "\t"
            string += item.__str__()
            string += "\n"

        string += "\nEntrypoints:\n"
        for item in self.entrypoints:
            string += "\t"
            string += item.__str__()
            string += "\n"

        return string

    def to_json(self):
        """Return the tool configuration as a json object"""

        _inputs = []
        for item in self.inputs:
            _inputs.append(item.to_json())

        _entrypoints = []
        for item in self.entrypoints:
            _entrypoints.append(item.to_json())

        return {
            "name": self.name,
            "description": self.description,
            "inputs": _inputs,
            "entrypoints": _entrypoints
        }
