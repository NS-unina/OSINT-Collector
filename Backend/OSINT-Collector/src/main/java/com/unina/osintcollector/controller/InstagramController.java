package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.InstagramAccount;
import com.unina.osintcollector.repository.InstagramAccountRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/instagram")
public class InstagramController {

    private final InstagramAccountRepository instagramAccountRepository;

    public InstagramController(InstagramAccountRepository instagramAccountRepository) {
        this.instagramAccountRepository = instagramAccountRepository;
    }

    @GetMapping(value = { "/accounts" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<InstagramAccount> getAccounts() {
        return instagramAccountRepository.findAll();
    }

}
