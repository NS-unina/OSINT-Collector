package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Platform;
import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.repository.PlatformRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/platforms")
public class PlatformController {
    private final PlatformRepository platformRepository;

    public PlatformController(PlatformRepository platformRepository) {
        this.platformRepository = platformRepository;
    }

    @GetMapping(value = { "", "/" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Platform> getPlatforms() {
        return platformRepository.getPlatforms();
    }
}
