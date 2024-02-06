package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;

@Node("SiteAccount")
public class SiteAccount {

    @Id
    private final Long id;

    @Property
    private final String site;
    private final String status;
    private final String url;

    public SiteAccount(Long id, String site, String status, String url) {
        this.id = id;
        this.site = site;
        this.status = status;
        this.url = url;
    }

    public Long getId() {
        return id;
    }

    public String getSite() {
        return site;
    }

    public String getStatus() {
        return status;
    }

    public String getUrl() {
        return url;
    }
}
