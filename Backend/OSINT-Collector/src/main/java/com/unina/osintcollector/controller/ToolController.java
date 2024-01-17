package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import com.unina.osintcollector.repository.ToolRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

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
        return toolRepository.deleteToolByName(toolNameToRemove)
                .thenMany(toolRepository.getTools());
    }

    @PostMapping("/requiredInputs")
    public Flux<ToolInput> getRequiredInputs(@RequestBody Map<String, List<String>> requestBody) {
        List<String> capabilities = requestBody.get("capabilities");
        System.out.println("Capabilities: " + capabilities);
        return toolRepository.getRequiredInputs(capabilities);
    }

    @PostMapping("/add")
    public void addTool(@RequestBody String fileYAML) {
        //TO_DO
        System.out.println(fileYAML);
    }

}
