package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Category;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;

public interface CategoryRepository extends ReactiveNeo4jRepository<Category, String> {
}
