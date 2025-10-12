from app.utils.models.tool_config import Input, EntrypointConfig, ToolConfig
import pytest

class TestInput:
    
    @pytest.fixture(autouse=True)
    def example_tool_dict(self):
        """Provide an example tool dictionary structure."""
        return {
            "snscrape": {
                "description": "Download telegram data",
                "image": "snscrape/image:latest",
                "entrypoints": [
                    {
                        "feature_key": "download-messages",
                        "name": "Download messages",
                        "description": "Download Telegram messages",
                        "command": "snscrape --max-results ${RESULTS} telegram-channel ${CHANNEL}",
                        "inputs": ["CHANNEL", "RESULTS"],
                    }
                ],
                "inputs": [
                    {"input_key": "CHANNEL", "description": "Telegram channel", "type": "string"},
                    {"input_key": "RESULTS", "description": "Number of results", "type": "int"},
                ],
            }
        }


    def test_input_repr(self):
        """Ensure Input class __repr__ outputs expected format."""
        input = Input("CHANNEL", "Telegram channel", "string")
        assert repr(input) == "Input(key=CHANNEL, type=string)"
        assert input.input_key == "CHANNEL"
        assert input.description == "Telegram channel"
        assert input.type == "string"

    
    def test_entrypoint_replace_input_in_command(self):
        """Verify that input placeholders are correctly replaced in the command string."""
        entry = EntrypointConfig(
            feature_key="download",
            name="Download messages",
            description="Download telegram messages",
            command="snscrape --max-results ${RESULTS} telegram-channel ${CHANNEL}",
            inputList=[
                Input("RESULTS", "Number of results", "int"),
                Input("CHANNEL", "Telegram channel", "string"),
            ],
        )

        inputs = {"RESULTS": 5, "CHANNEL": "ilpost_official"}
        replaced = entry.replace_input_in_command(inputs)

        assert "5" in replaced
        assert "ilpost_official" in replaced
        assert "${" not in replaced


    def test_entrypoint_repr(self):
        """Ensure EntrypointConfig __repr__ correctly lists feature and input keys."""
        entrypoint = EntrypointConfig(
            feature_key="fkey",
            name="test",
            description="desc",
            command="cmd",
            inputList=[Input("A", "desc", "string")],
        )
        
        assert repr(entrypoint) == "Entrypoint(feature=fkey, inputs=['A'])"
    
    
    def test_tool_config_init(self, example_tool_dict):
        """Ensure ToolConfig initializes correctly with entrypoints and inputs."""
        tool = ToolConfig(example_tool_dict)
        assert tool.toolName == "snscrape"
        assert len(tool.entrypointList) == 1
        ep = tool.entrypointList[0]
        assert isinstance(ep, EntrypointConfig)
        assert ep.feature_key == "download-messages"
        assert ep.inputList[0].input_key == "CHANNEL"


    def test_tool_config_get_feature_valid(self, example_tool_dict):
        """Ensure get_feature returns correct entrypoint."""
        tool = ToolConfig(example_tool_dict)
        ep = tool.get_feature("download-messages")
        assert isinstance(ep, EntrypointConfig)
        assert ep.feature_key == "download-messages"


    def test_tool_config_get_feature_invalid(self, example_tool_dict):
        """Expect ValueError when requesting non-existent feature."""
        tool = ToolConfig(example_tool_dict)
        with pytest.raises(ValueError) as excinfo:
            tool.get_feature("nonexistent-feature")
        assert "not found" in str(excinfo.value)


    def test_feature_validation(self, example_tool_dict):
        """Check that feature_validation correctly identifies existing feature keys."""
        tool = ToolConfig(example_tool_dict)
        assert tool.feature_validation("download-messages")
        assert not tool.feature_validation("invalid-feature")


    def test_input_validation_success(self, example_tool_dict):
        """Ensure input_validation passes when all required inputs are provided."""
        tool = ToolConfig(example_tool_dict)
        valid_inputs = {"CHANNEL": "news_channel", "RESULTS": 5}
        assert tool.input_validation("download-messages", valid_inputs)


    def test_input_validation_missing(self, example_tool_dict):
        """Ensure input_validation fails when inputs are missing."""
        tool = ToolConfig(example_tool_dict)
        invalid_inputs = {"CHANNEL": "only_channel"}
        assert not tool.input_validation("download-messages", invalid_inputs)


    def test_input_validation_invalid_feature(self, example_tool_dict):
        """Ensure input_validation fails for non-existent feature."""
        tool = ToolConfig(example_tool_dict)
        valid_inputs = {"CHANNEL": "test", "RESULTS": 1}
        assert not tool.input_validation("nonexistent", valid_inputs)


    def test_tool_repr(self, example_tool_dict):
        """Check ToolConfig __repr__ output format."""
        tool = ToolConfig(example_tool_dict)
        rep = repr(tool)
        assert "snscrape" in rep
        assert "entrypoints" in rep
