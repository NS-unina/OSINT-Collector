package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.InstagramAccount;
import com.unina.osintcollector.model.Username;
import com.unina.osintcollector.repository.UsernameRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/usernames")
public class UsernameController {

    private final UsernameRepository usernameRepository;

    public UsernameController(UsernameRepository usernameRepository) {
        this.usernameRepository = usernameRepository;
    }

    @GetMapping(value = { "/", "" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<Username> getAccounts() {
        return usernameRepository.findAll();
    }

}
