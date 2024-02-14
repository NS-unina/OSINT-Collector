package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.InstagramAccount;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import reactor.core.publisher.Mono;

public interface InstagramAccountRepository extends ReactiveNeo4jRepository<InstagramAccount, String> {

    Mono<InstagramAccount> findInstagramAccountByUsername(String username);

}
