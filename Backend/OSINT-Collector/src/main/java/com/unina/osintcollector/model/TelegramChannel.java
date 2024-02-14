package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("TelegramChannel")
public class TelegramChannel {

    @Id
    private final String name;
    private final Boolean flag;

    @Relationship(type = "PUBLISHED", direction = OUTGOING)
    private Set<TelegramPost> posts;

    public TelegramChannel(String name, Boolean flag) {
        this.name = name;
        this.flag = flag;
    }

    public String getName() {
        return name;
    }

    public Boolean getFlag() {
        return flag;
    }

    public Set<TelegramPost> getPosts() {
        return posts;
    }
}