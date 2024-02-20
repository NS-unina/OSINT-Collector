package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.InstagramPost;
import com.unina.osintcollector.model.TelegramPost;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public interface InstagramPostRepository extends ReactiveNeo4jRepository<InstagramPost, String> {

    @Query("""
        MERGE (account:InstagramAccount {id: $account.id, full_name: $account.full_name, username: $account.username})
        ON CREATE SET account.profile_pic_url = $account.profile_pic_url, account.bio_links = $account.bio_links, account.biography = $account.biography, account.follow = $account.follow, account.followers = $account.followers
        ON MATCH SET account.profile_pic_url = $account.profile_pic_url, account.bio_links = $account.bio_links, account.biography = $account.biography, account.follow = $account.follow, account.followers = $account.followers
        MERGE (account)-[:PUBLISHED]->(p:InstagramPost {id: $post.id})
        ON CREATE SET p.url = $post.url, p.shortcode = $post.shortcode, p.likes = $post.likes, p.comments = $post.comments, p.taggedAccounts = $post.taggedAccounts, p.timestamp = $post.timestamp, p.text = $post.text
        ON MATCH SET p.url = $post.url, p.shortcode = $post.shortcode, p.likes = $post.likes, p.comments = $post.comments, p.taggedAccounts = $post.taggedAccounts, p.timestamp = $post.timestamp, p.text = $post.text
        MERGE (p)-[:TAKEN_AT]->(l:Location {name: $post.location.name})
        WITH account, collect(p) AS posts
        CALL apoc.nlp.gcp.entities.stream(posts, {
            nodeProperty: 'text',
            key: 'AIzaSyC_RV2nb7vjC32i1jd6mj92p1ww6BPga0g'
        })
        YIELD node, value
        WITH node, value, account
        UNWIND value.entities AS entity
        WITH entity, node, account
        MATCH (cat:Category) WHERE cat.name = entity.name OR cat.alsoKnownAs = entity.name
        MERGE (node)-[:REFERS_TO]->(cat)
        WITH node, count(cat) as matchedCategories, account
        FOREACH (ignoreMe IN CASE WHEN matchedCategories > 0 THEN [1] ELSE [] END |
            SET node.processed = true, account.flag = true
        )
        """)
    Mono<InstagramPost> saveAccountAndPost(Map<String, Object> account, Map<String, Object> post);


}
