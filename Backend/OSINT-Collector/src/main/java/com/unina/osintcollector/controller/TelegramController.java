package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.TelegramChannel;
import com.unina.osintcollector.model.TelegramGroup;
import com.unina.osintcollector.repository.TelegramChannelRepository;
import com.unina.osintcollector.repository.TelegramGroupRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/telegram")
public class TelegramController {

    private final TelegramChannelRepository telegramChannelRepository;
    private final TelegramGroupRepository telegramGroupRepository;

    public TelegramController(TelegramChannelRepository telegramChannelRepository, TelegramGroupRepository telegramGroupRepository) {
        this.telegramChannelRepository = telegramChannelRepository;
        this.telegramGroupRepository = telegramGroupRepository;
    }

    @GetMapping(value = { "/channels" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramChannel> getChannels() {
        return telegramChannelRepository.findAll();
    }

    @GetMapping(value = { "/groups" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramGroup> getGroups() {
        return telegramGroupRepository.findAll();
    }

}
