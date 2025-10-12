"""class for model tool"""
from typing import List
from pathlib import Path
import yaml

class Input:
    input_key: str
    description: str
    type: str

    def __init__(self, input_key: str, description: str, type: str):
        self.input_key = input_key
        self.description = description
        self.type = type

    def __repr__(self):
        return f"Input(key={self.input_key}, type={self.type})"
    

class EntrypointConfig:
    feature_key: str
    name: str
    description: str
    inputList: list[Input]

    def __init__(self, feature_key: str, name: str, description: str, command: str, inputList: list[Input]):
        self.feature_key = feature_key
        self.name = name
        self.description = description
        self.command = command
        self.inputList = inputList

    def replace_input_in_command(self, inputs: dict):
        replaced_command = self.command
        
        for key, value in inputs.items():
            placeholder = f"${{{key}}}"
            replaced_command = replaced_command.replace(placeholder, str(value))

        return replaced_command

    def __repr__(self):
        return f"Entrypoint(feature={self.feature_key}, inputs={[i.input_key for i in self.inputList]})"


class ToolConfig:
    toolName: str
    description: str
    image: str
    type: str
    entrypointList: list[EntrypointConfig]


    def __init__(self, tool_config: dict):
        self.toolName = next(iter(tool_config))
        tool_data = tool_config[self.toolName]

        self.description = tool_data.get("description", "")
        self.image = tool_data.get("image", "")
        self.entrypointList: List[EntrypointConfig] = []

        for ep in tool_data.get("entrypoints", []):
            entry_inputs = []

            for input_key in ep.get("inputs", []):
                input_def = next((i for i in tool_data["inputs"] if i["input_key"] == input_key),None)                
                if input_def:
                    entry_inputs.append(Input(input_def["input_key"], input_def["description"], input_def["type"]))

            entry = EntrypointConfig(
                feature_key=ep["feature_key"],
                name=ep["name"],
                description=ep["description"],
                command=ep["command"],
                inputList=entry_inputs)

            self.entrypointList.append(entry)


    def get_feature(self, feature: str):
        """
        Retrieve the EntrypointConfig object corresponding to the given feature key.

        Args:
            feature (str): The feature_key identifying the desired entrypoint.

        Returns:
            EntrypointConfig: The matching entrypoint configuration.

        Raises:
            ValueError: If no entrypoint with the given feature_key exists.
        """

        for ep in self.entrypointList:
            if ep.feature_key == feature:
                return ep
        
        raise ValueError(f"Feature '{feature}' not found in tool '{self.toolName}'.")


    def feature_validation(self, feature: str) -> bool:
        """Check whether a given feature_key exists among the tool's entrypoints.
        Args:
            feature (str): The feature_key identifying a specific entrypoint.
        Returns:
            bool: True if the feature exists, False otherwise.
        """
        return any(ep.feature_key == feature for ep in self.entrypointList)
    

    def input_validation(self, feature: str, user_inputs: dict) -> bool:
        """Validate that all required inputs for the given feature are provided.

        Args:
            feature (str): The feature_key of the entrypoint to validate.
            user_inputs (dict): Dictionary of user-provided inputs.

        Returns:
            bool: True if all required inputs are provided, False otherwise.
        """
        entrypoint = next((ep for ep in self.entrypointList if ep.feature_key == feature), None)
        if not entrypoint:
            return False

        expected_inputs = [i.input_key for i in entrypoint.inputList]
        provided_inputs = list(user_inputs.keys())

        missing = [key for key in expected_inputs if key not in provided_inputs]

        if missing:
            return False

        return True

    def __repr__(self):
        return f"ToolConfig(name={self.toolName}, entrypoints={self.entrypointList})"
