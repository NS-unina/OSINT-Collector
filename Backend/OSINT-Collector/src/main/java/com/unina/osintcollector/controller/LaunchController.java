package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Launch;
import com.unina.osintcollector.repository.LaunchRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

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

    @PostMapping(value = "/save")
    public Mono<Launch> saveLaunch(@RequestBody Launch tool) {
        return launchRepository.save(tool);
    }

    @PostMapping(value = "/update")
    public Mono<Launch> saveOrUpdateLaunch(@RequestBody Launch tool) {

        return launchRepository.findByImageAndEntrypointAndInputs(tool.getImage(), tool.getEntrypoint(), tool.getInputs())
                .switchIfEmpty(launchRepository.save(tool));

    }

}
