package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Input;
import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import com.unina.osintcollector.repository.ToolRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import org.yaml.snakeyaml.Yaml;
import reactor.core.publisher.Mono;

import java.io.*;
import java.util.*;

@RestController
@RequestMapping("/tools")
public class ToolController {
    private final ToolRepository toolRepository;

    public ToolController(ToolRepository toolRepository) {
        this.toolRepository = toolRepository;
    }

    @GetMapping(value = { "", "/" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Tool> getTools() {
        return toolRepository.getTools();
    }

    @PostMapping("/remove")
    public Flux<Tool> removeTool(@RequestBody Map<String, String> requestBody) {
        String toolNameToRemove = requestBody.get("remove_tool");
        return toolRepository.deleteTool(toolNameToRemove)
                .thenMany(toolRepository.getTools());
    }

    @PostMapping("/requiredInputs")
    public Flux<ToolInput> getRequiredInputs(@RequestBody Map<String, List<String>> requestBody) {
        List<String> capabilities = requestBody.get("capabilities");
        System.out.println("Capabilities: " + capabilities);
        return toolRepository.getRequiredInputs(capabilities);
    }

    @PostMapping("/add")
    public Mono<Void> addTool(@RequestBody String fileContent) {
        Yaml yaml = new Yaml();
        Map<String, Object> yamlMap = yaml.load(fileContent);

        String name = (String) yamlMap.get("name");
        String platform = (String) yamlMap.get("platform");

        @SuppressWarnings("unchecked")
        Map<String, Map<String, Map<String, List<String>>>> capabilitiesMap = (Map<String, Map<String, Map<String, List<String>>>>) yamlMap.get("capabilities");

        List<Map<String, Object>> capabilities = new ArrayList<>();
        capabilitiesMap.forEach((capabilityName, ioMap) -> {
            Map<String, Object> capability = new HashMap<>();
            capability.put("name", capabilityName);
            capability.put("inputs", ioMap.get("input"));
            capability.put("outputs", ioMap.get("output"));
            capability.put("description", ioMap.get("description"));

            capabilities.add(capability);
        });

        //System.out.println("Name: " + name + "; Platform: " + platform + "; Capabilities: " + capabilities);

        if (Objects.equals(platform, "Multi Platform")) {
            return toolRepository.addMultiPlatformTool(name, platform, capabilities);
        }

        return toolRepository.addTool(name, platform, capabilities);
    }

    @PostMapping("/run")
    public boolean runTools(@RequestBody ToolInput[] tools) {

        for (ToolInput tool : tools) {

            String toolName = tool.getTool().getName();
            String entrypoint = tool.getCapability().getName();
            String inputs = "";

            System.out.println("Tool: " + toolName);
            System.out.println("Entrypoint: " + entrypoint);
            System.out.println("Inputs:");
            for (Input input : tool.getInputs()) {
                System.out.println("- " + input.getLabel() + ": " + input.getValue());
                if (!inputs.isEmpty()) {
                    inputs = inputs + " ";
                }
                inputs = inputs + input.getValue();
            }
            System.out.println("Command: ./main.py " +  toolName + " -e " + entrypoint + " -i " + inputs);
            System.out.println("------------------------");

        }

        return true;
    }

}
