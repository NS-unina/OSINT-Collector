package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Username;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface UsernameRepository extends ReactiveNeo4jRepository<Username, String> {

    Mono<Username> findUsernameByUsername(String username);

}