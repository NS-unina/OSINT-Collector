package com.unina.osintcollector.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.neo4j.core.schema.Node;

@Node("Category")
public class Category {

    @Id
    private final String uri;

    private final String name;
    private final String alsoKnownAs;

    public Category(String uri, String name, String alsoKnownAs) {
        this.uri = uri;
        this.name = name;
        this.alsoKnownAs = alsoKnownAs;
    }

    public String getUri() {
        return uri;
    }

    public String getName() {
        return name;
    }

    public String getAlsoKnownAs() {
        return alsoKnownAs;
    }
}
