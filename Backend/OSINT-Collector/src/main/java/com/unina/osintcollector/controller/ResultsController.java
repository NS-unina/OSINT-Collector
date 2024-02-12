package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Launch;
import com.unina.osintcollector.model.TelegramChannel;
import com.unina.osintcollector.model.TelegramPost;
import com.unina.osintcollector.model.Username;
import com.unina.osintcollector.repository.LaunchRepository;
import com.unina.osintcollector.repository.TelegramChannelRepository;
import com.unina.osintcollector.repository.TelegramPostRepository;
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
    private final TelegramPostRepository telegramPostRepository;
    private final TelegramChannelRepository telegramChannelRepository;
    private final LaunchRepository launchRepository;

    public ResultsController(UsernameRepository usernameRepository, TelegramPostRepository telegramPostRepository, TelegramChannelRepository telegramChannelRepository, LaunchRepository launchRepository) {
        this.usernameRepository = usernameRepository;
        this.telegramPostRepository = telegramPostRepository;
        this.telegramChannelRepository = telegramChannelRepository;
        this.launchRepository = launchRepository;
    }

    @PostMapping("/blackbird")
    public Mono<Username> getBlackbirdResult(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return usernameRepository.findUsernameByUsername(inputs[0]);
    }

    @PostMapping("/snscrape-telegram")
    public Mono<TelegramChannel> getSnscrapeResult(@RequestBody Launch requestBody) {
        String image = requestBody.getImage();
        String[] inputs = requestBody.getInputs();
        System.out.println(image + " > " + Arrays.toString(inputs));
        return telegramChannelRepository.findTelegramChannelByName(inputs[0]);
    }

    @PostMapping("/test")
    public Mono<TelegramPost> getResults(@RequestBody TelegramPost post) {

        String[] parts = post.getUrl().split("/");
        String channelName = parts[4];

        System.out.println("DATA RECEIVED");
        System.out.println(post);
        return telegramPostRepository.saveChannelAndPost(channelName, post.getUrl(), post.getText());
    }

}