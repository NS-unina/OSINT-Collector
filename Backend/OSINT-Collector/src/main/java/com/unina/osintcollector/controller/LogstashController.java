package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.TelegramPost;
import com.unina.osintcollector.repository.TelegramPostRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("logstash")
public class LogstashController {

    private final TelegramPostRepository telegramPostRepository;

    public LogstashController(TelegramPostRepository telegramPostRepository) {
        this.telegramPostRepository = telegramPostRepository;
    }

    @PostMapping("/snscrape-telegram")
    public Mono<ResponseEntity<Object>> getSnscrapeResults(@RequestBody TelegramPost post) {

        String[] parts = post.getUrl().split("/");
        String channelName = parts[4];

        System.out.println("DATA RECEIVED");
        System.out.println(post);

        return telegramPostRepository.saveChannelAndPost(channelName, post.getUrl(), post.getText(), post.getDate())
                .thenReturn(ResponseEntity.status(HttpStatus.OK).build());
    }

    @PostMapping("/instaloader")
    public ResponseEntity<String> getInstaloaderResults(@RequestBody String post) {
        System.out.println(post);
        return ResponseEntity.status(HttpStatus.OK).build();
    }

    @PostMapping("/blackbird")
    public ResponseEntity<Object> getBlackbirdResults(@RequestBody String site) {

        System.out.println(site);
        return ResponseEntity.status(HttpStatus.OK).build();
    }

}
