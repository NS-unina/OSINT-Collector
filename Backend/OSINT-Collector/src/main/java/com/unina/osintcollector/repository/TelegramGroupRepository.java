package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramGroup;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;

public interface TelegramGroupRepository extends ReactiveNeo4jRepository<TelegramGroup, String> {

}
