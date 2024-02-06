package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Launch;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface LaunchRepository extends ReactiveNeo4jRepository<Launch, Long> {

    @Query("MATCH (l:Launch) RETURN DISTINCT l")
    Flux<Launch> getLaunches();

    Mono<Launch> findByImageAndEntrypointAndInputs(String image, String entrypoint, String[] inputs);

}
