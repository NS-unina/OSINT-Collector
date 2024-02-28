package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Date;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("TelegramMessage")
public class TelegramMessage {

    @Id
    private final String id;
    private final String messageType; //"_":"Message", "_":"MessageService"
    private final String peer_id;
    private final String from_id;
    private final String date;
    private final String edit_date;
    private final String message;
    private final Boolean pinned;
    private final String reply_to_id;
    private final Boolean processed;

    @Relationship(type = "REFERS_TO", direction = OUTGOING)
    private Set<Category> categories;

    public TelegramMessage(String id, String messageType, String peer_id, String from_id, String date, String edit_date, String message, Boolean pinned, String reply_to_id, Boolean processed) {
        this.id = id;
        this.messageType = messageType;
        this.peer_id = peer_id;
        this.from_id = from_id;
        this.date = date;
        this.edit_date = edit_date;
        this.message = message;
        this.pinned = pinned;
        this.reply_to_id = reply_to_id;
        this.processed = processed;
    }

    public String getId() {
        return id;
    }

    public String getMessageType() {
        return messageType;
    }

    public String getPeer_id() {
        return peer_id;
    }

    public String getFrom_id() {
        return from_id;
    }

    public String getDate() {
        return date;
    }

    public String getEdit_date() {
        return edit_date;
    }

    public String getMessage() {
        return message;
    }

    public Boolean getPinned() {
        return pinned;
    }

    public String getReply_to_id() {
        return reply_to_id;
    }

    public Boolean getProcessed() {
        return processed;
    }

    public Set<Category> getCategories() {
        return categories;
    }
}
