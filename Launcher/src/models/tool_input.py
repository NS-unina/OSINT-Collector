class ToolInput:
    def __init__(self, key: str, description: str, type: str):
        self.key = key
        self.description = description
        self.type = type

    def __str__(self):
        return "ToolInput: key={}, description={}, type={}".format(self.key, self.description, self.type)
