package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Capability;
import com.unina.osintcollector.model.Platform;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;

public interface PlatformRepository extends ReactiveNeo4jRepository<Platform, String> {

    @Query("MATCH (t:Tool)-[:RUNS_ON]->(p:Platform) RETURN DISTINCT ID(p) as id, p.name as name")
    Flux<Platform> getPlatforms();

}
