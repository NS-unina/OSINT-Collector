package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramGroup;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

public interface TelegramGroupRepository extends ReactiveNeo4jRepository<TelegramGroup, String> {
    @Query("""
            MATCH (g:TelegramGroup)-[:PUBLISHED]->(m)
            RETURN {messages: COLLECT(properties(m)), group: properties(g)} as result
            """)
    Flux<Map<String, Object>> getGroups();
}
