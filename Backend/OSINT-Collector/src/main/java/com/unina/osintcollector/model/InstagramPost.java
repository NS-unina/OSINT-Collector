package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Date;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.INCOMING;
import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("InstagramPost")
public class InstagramPost {

    @Id
    private final String id;

    private final String url;
    private final String shortcode;
    private final Long likes;
    private final Long comments;
    private final String[] taggedAccounts;
    private final Long timestamp;
    private final String text;
    private final Boolean processed;

    @Relationship(type = "REFERS_TO", direction = OUTGOING)
    private Set<Category> categories;
    @Relationship(type = "TAKEN_AT", direction = OUTGOING)
    private Location location;

    public InstagramPost(String id, String url, String shortcode, Long likes, Long comments, String[] taggedAccounts, Long timestamp, String text, Boolean processed, Location location) {
        this.id = id;
        this.url = url;
        this.shortcode = shortcode;
        this.likes = likes;
        this.comments = comments;
        this.taggedAccounts = taggedAccounts;
        this.timestamp = timestamp;
        this.text = text;
        this.processed = processed;
        this.location = location;
    }

    public String getId() {
        return id;
    }

    public String getUrl() {
        return url;
    }

    public String getShortcode() {
        return shortcode;
    }

    public Long getLikes() {
        return likes;
    }

    public Long getComments() {
        return comments;
    }

    public String[] getTaggedAccounts() {
        return taggedAccounts;
    }

    public Long getTimestamp() {
        return timestamp;
    }

    public String getText() {
        return text;
    }

    public Set<Category> getCategories() {
        return categories;
    }

    public Boolean getProcessed() {
        return processed;
    }

    public Location getLocation() {
        return location;
    }

}
