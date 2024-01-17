package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;

public interface ToolRepository extends ReactiveNeo4jRepository<Tool, String> {
    @Query("MATCH (t:Tool) RETURN DISTINCT ID(t) as id, t.name as name")
    Flux<Tool> getTools();
    Mono<Void> deleteToolByName(String toolName);

    @Query("""
            MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource)
            WHERE ANY(substring IN $capabilities WHERE c.name CONTAINS substring)
            RETURN properties(t) as tool, COLLECT(DISTINCT properties(i)) as inputs
            """)
    Flux<ToolInput> getRequiredInputs(List<String> capabilities);

}

