package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Tool;
import com.unina.osintcollector.model.ToolInput;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public interface ToolRepository extends ReactiveNeo4jRepository<Tool, String> {
    @Query("MATCH (t:Tool) RETURN DISTINCT ID(t) as id, t.name as name")
    Flux<Tool> getTools();
    Mono<Void> deleteToolByName(String toolName);

    @Query("MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability) WHERE t.name = $toolName DETACH DELETE t, c")
    Mono<Void> deleteTool(String toolName);

    @Query("""
            MATCH (t:Tool)-[:HAS_CAPABILITY]->(c:Capability)-[:NEEDS]->(i:Resource)
            WHERE ANY(substring IN $capabilities WHERE c.name CONTAINS substring)
            RETURN COLLECT(DISTINCT properties(t)) as tool, COLLECT(DISTINCT properties(i)) as inputs, c as capability
            """)
    Flux<ToolInput> getRequiredInputs(List<String> capabilities);

    @Query("""
    MERGE (t:Tool {name: $toolName, platform: $platform})
    MERGE (p:Platform {name: $platform})
    MERGE (t)-[:RUNS_ON]->(p)
    WITH t, p
    UNWIND $capabilities AS cap
    MERGE (c:Capability {name: cap.name})
    MERGE (t)-[:HAS_CAPABILITY]->(c)
    WITH c, t, cap, cap.inputs AS inputs
    UNWIND inputs AS input
    MATCH (i:Resource {name: input})-[*]->(:Resource {name: $platform})
    FOREACH (ignore IN CASE WHEN i IS NOT NULL THEN [1] ELSE [] END | MERGE (c)-[:NEEDS]->(i))
    WITH c, t, cap, cap.outputs AS outputs
    UNWIND outputs AS output
    MATCH (o:Resource {name: output})-[*]->(:Resource {name: $platform})
    FOREACH (ignore IN CASE WHEN o IS NOT NULL THEN [1] ELSE [] END | MERGE (c)-[:PRODUCES]->(o))
    """)
    Mono<Void> addTool(String toolName, String platform, List<Map<String, Object>> capabilities);

}

