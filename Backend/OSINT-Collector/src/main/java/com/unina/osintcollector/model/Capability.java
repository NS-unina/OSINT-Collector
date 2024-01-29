package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.HashSet;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("Capability")
public class Capability {

    private final Integer id;

    @Id
    private final String name;
    @Relationship(type = "NEEDS", direction = OUTGOING)
    private Set<Input> inputs = new HashSet<>();
    @Relationship(type = "PRODUCES", direction = OUTGOING)
    private Set<Output> outputs = new HashSet<>();

    public Capability(Integer id, String name) {
        this.id = id;
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Set<Input> getInputs() {
        return inputs;
    }

    public Set<Output> getOutputs() {
        return outputs;
    }
}
