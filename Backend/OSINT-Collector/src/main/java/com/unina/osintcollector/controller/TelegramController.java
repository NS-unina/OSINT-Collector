package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.TelegramChannel;
import com.unina.osintcollector.repository.TelegramChannelRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/telegram")
public class TelegramController {

    private final TelegramChannelRepository telegramChannelRepository;

    public TelegramController(TelegramChannelRepository telegramChannelRepository) {
        this.telegramChannelRepository = telegramChannelRepository;
    }

    @GetMapping(value = { "/channels" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<TelegramChannel> getChannels() {
        return telegramChannelRepository.findAll();
    }

}
