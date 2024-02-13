package com.unina.osintcollector.controller;

import com.unina.osintcollector.repository.TelegramPostRepository;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("logstash")
public class LogstashController {

    private final TelegramPostRepository telegramPostRepository;

    public LogstashController(TelegramPostRepository telegramPostRepository) {
        this.telegramPostRepository = telegramPostRepository;
    }

    @PostMapping("/snscrape-telegram")
    public String getSnscrapeResults(@RequestBody String post) {

        System.out.println(post);
        return "OK";

//        String[] parts = post.getUrl().split("/");
//        String channelName = parts[4];
//
//        System.out.println("DATA RECEIVED");
//        System.out.println(post);
//
//        return telegramPostRepository.saveChannelAndPost(channelName, post.getUrl(), post.getText());
    }

    @PostMapping("/instaloader")
    public String getInstaloaderResults(@RequestBody String post) {

        System.out.println(post);
        return "OK";

    }

    @PostMapping("/blackbird")
    public String getBlackbirdResults(@RequestBody String post) {

        System.out.println(post);
        return "OK";

    }

}
