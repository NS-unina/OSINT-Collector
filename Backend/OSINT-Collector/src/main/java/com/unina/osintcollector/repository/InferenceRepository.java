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
        MATCH (post)<-[:PUBLISHED]-(account)
        RETURN DISTINCT {post: properties(post), account: properties(account)} as result
        """)
    Flux<Map<String, Object>> inferenceByCategory(String category);

    @Query("""
        MATCH (c:Category {name: $category})
        CALL n10s.inference.nodesInCategory(c, { inCatRel: "REFERS_TO", subCatRel: "SUB_CAT_OF"}) yield node as post
        MATCH (post)<-[:PUBLISHED]-(account)
        WITH account
        MATCH (l:Location {name: $location})
        CALL n10s.inference.nodesInCategory(l, { inCatRel: "TAKEN_AT", subCatRel: "SUB_CAT_OF"}) yield node as post
        MATCH (post)<-[:PUBLISHED]-(account)
        RETURN DISTINCT {account: properties(account)} as result
        """)
    Flux<Map<String, Object>> inferenceByLocationAndCategory(String location, String category);
}

