package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.*;
import com.unina.osintcollector.repository.*;
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
    private final TelegramPostRepository telegramPostRepository;
    private final TelegramChannelRepository telegramChannelRepository;
    private final LaunchRepository launchRepository;
    private final InstagramAccountRepository instagramAccountRepository;

    public ResultsController(UsernameRepository usernameRepository, TelegramPostRepository telegramPostRepository, TelegramChannelRepository telegramChannelRepository, LaunchRepository launchRepository, InstagramAccountRepository instagramAccountRepository) {
        this.usernameRepository = usernameRepository;
        this.telegramPostRepository = telegramPostRepository;
        this.telegramChannelRepository = telegramChannelRepository;
        this.launchRepository = launchRepository;
        this.instagramAccountRepository = instagramAccountRepository;
    }

    @PostMapping("/blackbird")
    public Mono<Username> getBlackbirdResult(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return usernameRepository.findUsernameByUsername(inputs[0]);
    }

    @PostMapping("/instaloader")
    public Mono<InstagramAccount> getInstaloaderResults(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return instagramAccountRepository.findInstagramAccountByUsername(inputs[0]);
    }

    @PostMapping("/snscrape-telegram")
    public Mono<TelegramChannel> getSnscrapeResult(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return telegramChannelRepository.findTelegramChannelByName(inputs[0]);
    }

}