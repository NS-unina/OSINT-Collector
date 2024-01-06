"""
Tool Configuration Input Model
"""


class ToolInput:
    """
    Tool Configuration Model
    """

    def __init__(self, key: str, description: str, format_type: str):
        self.key = key
        self.description = description
        self.format_type = format_type

    def __str__(self):

        key = f"key={self.key}"
        desc = f"description={self.description}"
        format_type = f"format_type={self.format_type}"

        return f"ToolInput: {key}, {desc}, {format_type}"
