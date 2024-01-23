package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import com.unina.osintcollector.repository.ToolRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import org.yaml.snakeyaml.Yaml;
import reactor.core.publisher.Mono;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

            capabilities.add(capability);
        });

        //System.out.println("Name: " + name + "; Platform: " + platform + "; Capabilities: " + capabilities);

        return toolRepository.addTool(name, platform, capabilities);
    }

    @PostMapping("/run")
    public boolean runTools(@RequestBody String toolsInputs) {

        // Test to verify execution of Python code

        try {
            // Specify the path to the Python script
            String scriptPath = "/Users/ciromarrazzo/OSINT/OSINT-Collector/test.py";

            // Set up the process builder for executing the Python script
            ProcessBuilder processBuilder = new ProcessBuilder("python3.7", scriptPath, toolsInputs);

            // Set the working directory for the process to the location of the Python script
            processBuilder.directory(new File("/Users/ciromarrazzo/OSINT/OSINT-Collector/"));

            // Start the external process (Python script)
            Process process = processBuilder.start();

            // Capture and print the output of the Python script
            InputStream inputStream = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // Wait for the completion of the Python script execution
            int exitCode = process.waitFor();

            // Return true if the Python script executed successfully (exit code 0)
            return exitCode == 0;
        } catch (IOException | InterruptedException e) {
            // Print stack trace in case of IOException or InterruptedException
            e.printStackTrace();

            // Return false if an exception occurs during the execution of the Python script
            return false;
        }
    }

}
