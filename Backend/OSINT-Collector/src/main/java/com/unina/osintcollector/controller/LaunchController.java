package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Launch;
import com.unina.osintcollector.repository.LaunchRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/launches")
public class LaunchController {
    private final LaunchRepository launchRepository;

    public LaunchController(LaunchRepository launchRepository) {
        this.launchRepository = launchRepository;
    }

    @GetMapping(value = { "", "/" }, produces = MediaType.APPLICATION_JSON_VALUE)
    Flux<Launch> getPlatforms() {
        return launchRepository.getLaunches();
    }

}
