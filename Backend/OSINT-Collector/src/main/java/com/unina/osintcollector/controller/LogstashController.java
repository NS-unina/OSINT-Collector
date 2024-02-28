package com.unina.osintcollector.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.unina.osintcollector.model.*;
import com.unina.osintcollector.repository.InstagramPostRepository;
import com.unina.osintcollector.repository.SiteAccountRepository;
import com.unina.osintcollector.repository.TelegramMessageRepository;
import com.unina.osintcollector.repository.TelegramPostRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import com.fasterxml.jackson.core.type.TypeReference;

import java.util.*;

@RestController
@RequestMapping("logstash")
public class LogstashController {

    private final TelegramPostRepository telegramPostRepository;
    private final InstagramPostRepository instagramPostRepository;
    private final SiteAccountRepository siteAccountRepository;
    private final TelegramMessageRepository telegramMessageRepository;

    public LogstashController(TelegramPostRepository telegramPostRepository, InstagramPostRepository instagramPostRepository, SiteAccountRepository siteAccountRepository, TelegramMessageRepository telegramMessageRepository) {
        this.telegramPostRepository = telegramPostRepository;
        this.instagramPostRepository = instagramPostRepository;
        this.siteAccountRepository = siteAccountRepository;
        this.telegramMessageRepository = telegramMessageRepository;
    }

    @PostMapping("telegram-tracker")
    public Mono<ResponseEntity<Object>> getTelegramTrackerResults(@RequestBody TelegramRecord telegramRecord) {

        TelegramMessage[] telegramMessages = telegramRecord.messages();
        TelegramGroup telegramGroup = telegramRecord.channel();
        TelegramUser[] telegramUsers = telegramRecord.users();

        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> telegramMessagesMapList = new ArrayList<>();
        for (TelegramMessage message : telegramMessages) {
            Map<String, Object> messageMap = mapper.convertValue(message, new TypeReference<Map<String, Object>>() {});
            telegramMessagesMapList.add(messageMap);
        }

        Map<String, Object> telegramGroupMap = mapper.convertValue(telegramGroup, Map.class);

        List<Map<String, Object>> telegramUsersMapList = new ArrayList<>();
        for (TelegramUser user : telegramUsers) {
            Map<String, Object> userMap = mapper.convertValue(user, new TypeReference<Map<String, Object>>() {});
            telegramUsersMapList.add(userMap);
        }

        return telegramMessageRepository.saveMessagesChannelUser(telegramMessagesMapList, telegramGroupMap, telegramUsersMapList).thenReturn(ResponseEntity.status(HttpStatus.OK).build());
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
    public Mono<ResponseEntity<Object>> getInstaloaderResults(@RequestBody InstagramRecord instagramRecord) {

        InstagramAccount instagramAccount = instagramRecord.owner();
        InstagramPost instagramPost = instagramRecord.post();

        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> accountMap = mapper.convertValue(instagramAccount, Map.class);
        Map<String, Object> postMap = mapper.convertValue(instagramPost, Map.class);

        return instagramPostRepository.saveAccountAndPost(accountMap, postMap).thenReturn(ResponseEntity.status(HttpStatus.OK).build());

    }

    @PostMapping("/blackbird")
    public Mono<ResponseEntity<Object>> getBlackbirdResults(@RequestBody SiteAccountList sitesList) {

        String[] parts = sitesList.sites().get(0).getUrl().split("/");
        String username = parts[3];

        List<SiteAccount> sites = sitesList.sites();
        List<Map<String, Object>> siteMaps = new ArrayList<>();

        WebClient webClient = WebClient.create(); // create a WebClient instance

        for (SiteAccount site : sites) {
            Map<String, Object> siteMap = new HashMap<>();
            siteMap.put("id", site.getId());
            siteMap.put("site", site.getSite());
            siteMap.put("url", site.getUrl());
            siteMap.put("status", site.getStatus());
            siteMaps.add(siteMap);

            if (Objects.equals(site.getSite(), "Instagram") && Objects.equals(site.getStatus(), "FOUND")) {
                String url = "http://localhost:5000/launch";

                // Create the body of the request
                Map<String, Object> body = new HashMap<>();
                body.put("image", "instaloader");
                body.put("entrypoint", "download-public-profile");
                body.put("inputs", Collections.singletonList(username));

                System.out.print("INSTALOADER SEND: " + body);

                Mono<String> response = webClient.post()
                        .uri(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(body)
                        .retrieve()
                        .bodyToMono(String.class);

                response.subscribe(result -> {
                    System.out.println(result); // print the result to the console
                }, error -> {
                    System.err.println(error.getMessage()); // print the error message to the console
                });
            }
        }

        return siteAccountRepository.saveSites(username, siteMaps).thenReturn(ResponseEntity.status(HttpStatus.OK).build());
    }


}
