package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.Location;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;

public interface LocationRepository extends ReactiveNeo4jRepository<Location, String> {
}
