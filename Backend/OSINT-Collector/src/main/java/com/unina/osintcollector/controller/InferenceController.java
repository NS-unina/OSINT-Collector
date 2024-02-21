package com.unina.osintcollector.controller;

import com.unina.osintcollector.repository.InferenceRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/inference")
public class InferenceController {

    private final InferenceRepository inferenceRepository;

    public InferenceController(InferenceRepository inferenceRepository) {
        this.inferenceRepository = inferenceRepository;
    }

    @GetMapping(value = {"/category" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Map<String, Object>> getPosts(@RequestParam String input) {
        return inferenceRepository.inferenceByCategory(input);
    }
}
