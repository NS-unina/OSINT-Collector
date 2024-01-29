package com.unina.osintcollector.model;

import java.util.List;

public class ToolInput {
    private final Tool tool;
    private final List<Input> inputs;

    public ToolInput(Tool tool, List<Input> inputs) {
        this.tool = tool;
        this.inputs = inputs;
    }

    public Tool getTool() {
        return tool;
    }

    public List<Input> getInputs() {
        return inputs;
    }
}
