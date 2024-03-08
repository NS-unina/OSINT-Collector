package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.TelegramChannel;
import com.unina.osintcollector.model.TelegramGroup;
import com.unina.osintcollector.model.TelegramMessage;
import com.unina.osintcollector.repository.TelegramChannelRepository;
import com.unina.osintcollector.repository.TelegramGroupRepository;
import com.unina.osintcollector.repository.TelegramMessageRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/telegram")
public class TelegramController {

    private final TelegramChannelRepository telegramChannelRepository;
    private final TelegramGroupRepository telegramGroupRepository;
    private final TelegramMessageRepository telegramMessageRepository;

    public TelegramController(TelegramChannelRepository telegramChannelRepository, TelegramGroupRepository telegramGroupRepository, TelegramMessageRepository telegramMessageRepository) {
        this.telegramChannelRepository = telegramChannelRepository;
        this.telegramGroupRepository = telegramGroupRepository;
        this.telegramMessageRepository = telegramMessageRepository;
    }

    @GetMapping(value = { "/channels" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramChannel> getChannels() {
        return telegramChannelRepository.findAll();
    }

    @GetMapping(value = { "/groups" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramGroup> getGroups() {
        return telegramGroupRepository.findAll();
    }

    @GetMapping(value = { "/moderate" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramMessage> getModeration(@RequestParam(required = false) String id) {
        return telegramMessageRepository.ModerateGroup(id);
    }

    @GetMapping(value = { "/messages" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramMessage> getMessages(@RequestParam(required = false) String id) {
        return telegramMessageRepository.findTelegramMessageByPeerId(id);
    }

}
