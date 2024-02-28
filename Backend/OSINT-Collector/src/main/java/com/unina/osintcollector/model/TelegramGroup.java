package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("TelegramGroup")
public class TelegramGroup {

    @Id
    private final String id;
    private final String about;
    private final String title;
    private final String username;
    private final String date;
    private final String participants_count;
    private final Boolean flag;

    @Relationship(type = "PUBLISHED", direction = OUTGOING)
    private Set<TelegramMessage> messages;

    public TelegramGroup(String id, String about, String title, String username, String date, String participants_count, Boolean flag) {
        this.id = id;
        this.about = about;
        this.title = title;
        this.username = username;
        this.date = date;
        this.participants_count = participants_count;
        this.flag = flag;
    }

    public String getId() {
        return id;
    }

    public String getAbout() {
        return about;
    }

    public String getTitle() {
        return title;
    }

    public String getUsername() {
        return username;
    }

    public String getDate() {
        return date;
    }

    public String getParticipants_count() {
        return participants_count;
    }

    public Set<TelegramMessage> getMessages() {
        return messages;
    }

    public Boolean getFlag() {
        return flag;
    }
}
