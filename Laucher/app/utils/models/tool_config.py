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


    def __init__(self, toolName: str, description: str, image: str, entrypointList: list[EntrypointConfig]):
        self.toolName = toolName
        self.description = description
        self.image = image
        self.entrypointList = entrypointList

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
        return next((ep for ep in self.entrypointList if ep.feature_key == feature), None)


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


if __name__ == "__main__":
    yml_path = Path("/home/nda/Desktop/OSINT-Collector/Laucher/tools/snscrape-telegram/snscrape-telegram.yml")
    with open(yml_path, "r") as f:
        tool_dict = yaml.safe_load(f)

    tool = ToolConfig(tool_dict)

    print(f"\n🔧 Tool name: {tool.toolName}")
    print(f"📝 Description: {tool.description}")
    print(f"🪣 Image: {tool.image}")
    print("\n🚀 Entrypoints:")
    for ep in tool.entrypointList:
        print(f"  • Feature key: {ep.feature_key}")
        print(f"    Name: {ep.name}")
        print(f"    Description: {ep.description}")
        print(f"    Command: {ep.command}")
        print(f"    Inputs:")
        for inp in ep.inputList:
            print(f"       - {inp.input_key} ({inp.type}): {inp.description}")
    print("-----------------------------------------------------------------")

    print("Command replace")
    test_dict = {"CHANNEL": "prova1", "RESULTS": 5}
    feature = tool.get_feature("download-messages")
    print(feature)
    ciccio = feature.replace_input_in_command(test_dict)
    print(ciccio)
    
    # print(tool.get_feature("download-messages").replace_input_in_command(test_dict))

