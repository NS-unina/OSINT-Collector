package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.InstagramPost;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;

public interface InstagramPostRepository extends ReactiveNeo4jRepository<InstagramPost, String> {
}
