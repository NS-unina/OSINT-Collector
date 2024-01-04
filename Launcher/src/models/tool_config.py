from .tool_input import *

class ToolConfig:
    
    def __init__(self, name: str, data: dict):
        
        data = data[name]

        self.name =  name
        self.description = data['description']
        self.entrypoint = data['entrypoint']
        self.inputs = []
        
        for item in data['inputs']:

            tool_input = ToolInput(
                key=item['key'], 
                description=item['description'], 
                type=item['type'])

            self.inputs.append(tool_input)

    def __str__(self):

        string = "ToolConfig: name={}, description={}".format(self.name, self.description)
        string += "\nInputs:\n"

        for item in self.inputs:    
            string += "\t"
            string += item.__str__()
            string += "\n"
        
        return string