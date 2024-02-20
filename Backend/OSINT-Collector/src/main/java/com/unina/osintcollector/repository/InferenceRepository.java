package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Category;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;

import java.util.Map;

public interface InferenceRepository extends ReactiveNeo4jRepository<Category, String> {

    @Query("""
        MATCH (c:Category {name: $category})
        CALL n10s.inference.nodesInCategory(c, { inCatRel: "REFERS_TO", subCatRel: "SUB_CAT_OF"}) yield node as post
        MATCH (post)<-[:PUBLISHED]-(user)
        RETURN post
        """)
    Flux<Map<String, Object>> inferenceByCategory(String category);

}

