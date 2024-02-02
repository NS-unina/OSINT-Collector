package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;

@Node("Launch")
public class Launch {

    @Id
    @GeneratedValue
    private final Long id;

    private final String image;
    private final String entrypoint;
    private final String[] inputs;

    public Launch(Long id, String image, String entrypoint, String[] inputs) {
        this.id = id;
        this.image = image;
        this.entrypoint = entrypoint;
        this.inputs = inputs;
    }

    public Long getId() {
        return id;
    }

    public String getImage() {
        return image;
    }

    public String getEntrypoint() {
        return entrypoint;
    }

    public String[] getInputs() {
        return inputs;
    }
}
