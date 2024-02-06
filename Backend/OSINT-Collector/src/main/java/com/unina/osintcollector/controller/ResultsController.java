package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Launch;
import com.unina.osintcollector.model.Username;
import com.unina.osintcollector.repository.UsernameRepository;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.Arrays;

@RestController
@RequestMapping("results")
public class ResultsController {

    private final UsernameRepository usernameRepository;

    public ResultsController(UsernameRepository usernameRepository) {
        this.usernameRepository = usernameRepository;
    }

    @PostMapping("/blackbird")
    public Mono<Username> getBlackbirdResult(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return usernameRepository.findUsernameByUsername(inputs[0]);
    }
}