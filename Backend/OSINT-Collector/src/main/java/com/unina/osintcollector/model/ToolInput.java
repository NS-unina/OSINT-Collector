package com.unina.osintcollector.model;

import java.util.List;

public class ToolInput {
    private final Tool tool;
    private final Capability capability;
    private final List<Input> inputs;

    public ToolInput(Tool tool, Capability capability, List<Input> inputs) {
        this.tool = tool;
        this.capability = capability;
        this.inputs = inputs;
    }

    public Tool getTool() {
        return tool;
    }

    public List<Input> getInputs() {
        return inputs;
    }

    public Capability getCapability() {
        return capability;
    }
}
