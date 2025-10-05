"""
Tool Configuration Entrypoint Model
"""


class ToolEntrypoint:
    """
    Tool Configuration Model
    """

    def __init__(self, key: str, description: str,
                 inputs: [str], command: str):

        self.key = key
        self.description = description
        self.inputs = inputs
        self.command = command

    def help_string(self):
        """
        Returns a string describing the entrypoint,
        used in help message
        """

        req_inputs = " ".join(self.inputs)
        req_inputs_str = f"(required inputs: {req_inputs})"

        return f"{self.key}: {self.description} {req_inputs_str}"

    def __str__(self):

        key = f"key={self.key}"
        desc = f"description={self.description}"
        inputs = f"inputs={self.inputs}"
        command = f"command={self.command}"

        return f"ToolEntrypoint: {key}, {desc}, {inputs}, {command}"

    def to_json(self):
        """Return the tool entrypoints as a json object"""

        return {
            "key": self.key,
            "description": self.description,
            "inputs": self.inputs,
            "command": self.command,
        }
