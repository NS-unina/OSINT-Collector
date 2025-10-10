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
                input_def = next((i for i in tool_data["inputs"] if i["key"] == input_key), None)
                if input_def:
                    entry_inputs.append(Input(input_def["key"], input_def["description"], input_def["type"]))
                else:
                    print(f" Warning: input '{input_key}' not defined in tool inputs.")

            entry = EntrypointConfig(
                feature_key=ep["feature_key"],
                name=ep["name"],
                description=ep["description"],
                command=ep["command"],
                inputList=entry_inputs)

            self.entrypointList.append(entry)

    def __repr__(self):
        return f"ToolConfig(name={self.toolName}, entrypoints={self.entrypointList})"

