package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramChannel;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import reactor.core.publisher.Mono;

public interface TelegramChannelRepository extends ReactiveNeo4jRepository<TelegramChannel, String> {

    Mono<TelegramChannel> findTelegramChannelByName(String name);

}
