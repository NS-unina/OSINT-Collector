package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.InstagramPost;
import com.unina.osintcollector.model.SiteAccount;
import com.unina.osintcollector.model.SiteAccountList;
import com.unina.osintcollector.model.TelegramPost;
import com.unina.osintcollector.repository.InstagramPostRepository;
import com.unina.osintcollector.repository.SiteAccountRepository;
import com.unina.osintcollector.repository.TelegramPostRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.*;

@RestController
@RequestMapping("logstash")
public class LogstashController {

    private final TelegramPostRepository telegramPostRepository;
    private final InstagramPostRepository instagramPostRepository;
    private final SiteAccountRepository siteAccountRepository;

    public LogstashController(TelegramPostRepository telegramPostRepository, InstagramPostRepository instagramPostRepository, SiteAccountRepository siteAccountRepository) {
        this.telegramPostRepository = telegramPostRepository;
        this.instagramPostRepository = instagramPostRepository;
        this.siteAccountRepository = siteAccountRepository;
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
    public Mono<ResponseEntity<Object>> getInstaloaderResults(@RequestBody InstagramPost post) {
        System.out.println(post.getId());
        return instagramPostRepository.save(post).thenReturn(ResponseEntity.status(HttpStatus.OK).build());
    }

    @PostMapping("/blackbird")
    public Mono<ResponseEntity<Object>> getBlackbirdResults(@RequestBody SiteAccountList sitesList) {

        String[] parts = sitesList.sites().get(0).getUrl().split("/");
        String username = parts[3];

        List<SiteAccount> sites = sitesList.sites();
        List<Map<String, Object>> siteMaps = new ArrayList<>();

        for (SiteAccount site : sites) {
            Map<String, Object> siteMap = new HashMap<>();
            siteMap.put("id", site.getId());
            siteMap.put("site", site.getSite());
            siteMap.put("url", site.getUrl());
            siteMap.put("status", site.getStatus());
            siteMaps.add(siteMap);
        }

        return siteAccountRepository.saveSites(username, siteMaps).thenReturn(ResponseEntity.status(HttpStatus.OK).build());
    }


}
