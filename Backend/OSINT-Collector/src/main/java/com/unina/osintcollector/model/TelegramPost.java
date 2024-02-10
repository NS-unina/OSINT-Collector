package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Property;

import java.util.Date;

@Node("TelegramPost")
public class TelegramPost {
    @Id
    private final String url;

    private final Date date;
    private final String content;

    public TelegramPost(String url, Date date, String content) {
        this.url = url;
        this.date = date;
        this.content = content;
    }

    public String getUrl() {
        return url;
    }

    public Date getDate() {
        return date;
    }

    public String getContent() {
        return content;
    }
}
