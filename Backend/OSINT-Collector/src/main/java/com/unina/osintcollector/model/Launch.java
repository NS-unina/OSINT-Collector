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
    private final String timestamp;

    private final Boolean completed;

    public Launch(Long id, String image, String entrypoint, String[] inputs, String timestamp, Boolean completed) {
        this.id = id;
        this.image = image;
        this.entrypoint = entrypoint;
        this.inputs = inputs;
        this.timestamp = timestamp;
        this.completed = completed;
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

    public String getTimestamp() {
        return timestamp;
    }

    public Boolean getCompleted() {
        return completed;
    }
}
