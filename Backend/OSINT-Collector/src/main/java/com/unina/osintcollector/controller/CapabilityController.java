package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Capability;
import com.unina.osintcollector.repository.CapabilityRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/capabilities")
public class CapabilityController {
    private final CapabilityRepository capabilityRepository;

    public CapabilityController(CapabilityRepository capabilityRepository) {
        this.capabilityRepository = capabilityRepository;
    }

    @GetMapping(value = { "", "/" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<Capability> getCapabilities(@RequestParam(required = false) String platform) {
        return capabilityRepository.findCapabilitiesByPlatform(platform);
    }
}
