package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Capability;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;
import reactor.core.publisher.Flux;

public interface CapabilityRepository extends ReactiveNeo4jRepository<Capability, String> {
    @Query("MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability) WHERE t.platform = $platform OR $platform = 'All' RETURN DISTINCT ID(c) as id, c.name as name, c.description as description")
    Flux<Capability> findCapabilitiesByPlatform(@Param("platform") String platform);
}
