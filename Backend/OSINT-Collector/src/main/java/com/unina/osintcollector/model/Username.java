package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.*;

import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("Username")
public class Username {

    @Id
    private final String username;

    @Relationship(type = "ASSOCIATED_WITH", direction = OUTGOING)
    private Set<SiteAccount> sites;

    public Username(String username) {
        this.username = username;
    }

    public String getUsername() {
        return username;
    }

    public Set<SiteAccount> getSites() {
        return sites;
    }
}