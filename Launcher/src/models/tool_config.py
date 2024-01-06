"""
Tool Configuration Model
"""

from src.models.tool_input import ToolInput


class ToolConfig:
    """
    Tool Configuration Model
    """

    def __init__(self, name: str, data: dict):

        data = data[name]

        self.name = name
        self.description = data['description']
        self.entrypoint = data['entrypoint']
        self.inputs = []

        for item in data['inputs']:

            tool_input = ToolInput(key=item['key'],
                                   description=item['description'],
                                   format_type=item['type'])

            self.inputs.append(tool_input)

    def __str__(self):

        name = f"name={self.name}"
        desc = f"description={self.description}"
        string = f"ToolConfig: {name}, {desc}"
        string += "\nInputs:\n"

        for item in self.inputs:
            string += "\t"
            string += item.__str__()
            string += "\n"

        return string
