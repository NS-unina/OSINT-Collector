package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.HashSet;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("Tool")
public class Tool {

    private final Integer id;
    @Id
    private final String name;
    @Property
    private String platform;
    @Relationship(type = "HAS_CAPABILITY", direction = OUTGOING)
    private Set<Capability> capabilities = new HashSet<>();

    public Tool(Integer id, String name, String platform) {
        this.id = id;
        this.name = name;
        this.platform = platform;
    }

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getPlatform() {
        return platform;
    }

    public Set<Capability> getCapabilities() {
        return capabilities;
    }
}
