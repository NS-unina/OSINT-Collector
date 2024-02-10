package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramPost;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Mono;

public interface TelegramPostRepository extends ReactiveNeo4jRepository<TelegramPost, String> {

    @Query("""
            MERGE (c:TelegramChannel {name: $channel})
            MERGE (c)-[:PUBLISHED]->(p:TelegramPost {url: $url, text: $content})
            """)
    Mono<TelegramPost> saveChannelAndPost(String channel, String url, String content);
}
