package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Launch;
import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import com.unina.osintcollector.repository.LaunchRepository;
import com.unina.osintcollector.repository.ToolRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import reactor.core.publisher.Flux;

import org.yaml.snakeyaml.Yaml;
import reactor.core.publisher.Mono;

import java.util.*;

@RestController
@RequestMapping("/tools")
public class ToolController {
    private final ToolRepository toolRepository;
    private final LaunchRepository launchRepository;

    private final RestTemplate restTemplate;

    public ToolController(ToolRepository toolRepository, LaunchRepository launchRepository, RestTemplate restTemplate) {
        this.toolRepository = toolRepository;
        this.launchRepository = launchRepository;
        this.restTemplate = restTemplate;
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
    public Mono<String> runTools(@RequestBody Launch tool) {
        Mono<Launch> saveMono = launchRepository.save(tool);
        Mono<Void> postMono = Mono.fromRunnable(() -> {
            String launcherUrl = "http://localhost:5000/launch";
            restTemplate.postForEntity(launcherUrl, tool, Void.class);
        });

        return saveMono.then(postMono).then(Mono.just("OK"));
    }

}
