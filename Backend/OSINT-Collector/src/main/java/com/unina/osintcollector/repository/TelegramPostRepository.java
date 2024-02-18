package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramPost;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Mono;

public interface TelegramPostRepository extends ReactiveNeo4jRepository<TelegramPost, String> {

    @Query("""
            MERGE (channel:TelegramChannel {name: $channel})
            MERGE (channel)-[:PUBLISHED]->(p:TelegramPost {url: $url, text: $content, date: $date})
            WITH channel, collect(p) AS posts
            CALL apoc.nlp.gcp.entities.stream(posts, {
                nodeProperty: 'text',
                key: 'AIzaSyC_RV2nb7vjC32i1jd6mj92p1ww6BPga0g'
            })
            YIELD node, value
            WITH node, value, channel
            UNWIND value.entities AS entity
            WITH entity, node, channel
            MATCH (cat:Category) WHERE cat.name = entity.name OR cat.alsoKnownAs = entity.name
            MERGE (node)-[:REFERS_TO]->(cat)
            WITH node, count(cat) as matchedCategories, channel
            FOREACH (ignoreMe IN CASE WHEN matchedCategories > 0 THEN [1] ELSE [] END |
                SET node.processed = true, channel.flag = true
            )
            """)
    Mono<TelegramPost> saveChannelAndPost(String channel, String url, String content, String date);

}
