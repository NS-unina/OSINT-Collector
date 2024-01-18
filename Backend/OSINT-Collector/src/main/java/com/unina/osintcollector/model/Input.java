package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;

@Node("Input")
public class Input {

    private final Integer id;

    @Id
    private final String name;

    @Property
    private final String label;
    private final String uri;

    public Input(Integer id, String name, String label, String uri) {
        this.id = id;
        this.name = name;
        this.label = label;
        this.uri = uri;
    }

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getLabel() {
        return label;
    }

    public String getUri() {
        return uri;
    }
}