package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;

@Node("ModerationCategory")
public class ModerationCategory {
    @Id
    private final String name;

    public ModerationCategory(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
