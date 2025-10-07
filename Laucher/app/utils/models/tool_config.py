"""class for model tool"""

class Input:
    input_key: str
    description: str
    type: str


    def __init__(self, input_key: str, description: str, type: str):
        self.input_key = input_key
        self.description = description
        self.type = type


class EntrypointConfig:
    feature_key: str
    name: str
    description: str
    inputList: list[Input]


    def __init__(self, feature_key: str, name: str, description: str, inputList: list[Input]):
        self.feature_key = feature_key
        self.name = name
        self.description = description
        self.inputList = inputList


class ToolConfig:
    toolName: str
    description: str
    image: str
    type: str
    entrypointList: list[EntrypointConfig]


    def __init__(self, toolName: str, description: str, image: str.type, type: str, entrypointList: list[EntrypointConfig]):
        self.toolName = toolName
        self.description = description
        self.image = image
        self.type = type
        self.entrypointList = entrypointList


