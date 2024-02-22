package com.unina.osintcollector.controller;

import com.unina.osintcollector.repository.InferenceRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

import java.util.Map;

@RestController
@RequestMapping("/inference")
public class InferenceController {

    private final InferenceRepository inferenceRepository;

    public InferenceController(InferenceRepository inferenceRepository) {
        this.inferenceRepository = inferenceRepository;
    }

    @GetMapping(value = {"/category" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Map<String, Object>> getPosts(@RequestParam String input1) {
        return inferenceRepository.inferenceByCategory(input1);
    }

    @GetMapping(value = {"/location" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Map<String, Object>> getUsers(@RequestParam String input1, String input2) {
        return inferenceRepository.inferenceByLocationAndCategory(input1, input2);
    }
}
