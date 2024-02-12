package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Date;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("TelegramPost")
public class TelegramPost {
    @Id
    private final String url;

    private final Date date;
    private final String text;
    private final Boolean processed;

    @Relationship(type = "REFERS_TO", direction = OUTGOING)
    private Set<Category> categories;

    public TelegramPost(String url, Date date, String text, Boolean processed) {
        this.url = url;
        this.date = date;
        this.text = text;
        this.processed = processed;
    }

    public String getUrl() {
        return url;
    }

    public Date getDate() {
        return date;
    }

    public String getText() {
        return text;
    }

    public Boolean getProcessed() {
        return processed;
    }

    public Set<Category> getCategories() {
        return categories;
    }
}
