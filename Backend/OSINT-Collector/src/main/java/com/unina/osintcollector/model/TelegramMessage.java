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

    @Relationship(type = "REPLY_TO", direction = OUTGOING)
    private TelegramMessage repliedMessage;

    public TelegramMessage(String id, String messageType, String peerId, String fromId, String date, String editDate, String message, Boolean pinned, String replyToId, Boolean processed) {
        this.id = id;
        this.messageType = messageType;
        peer_id = peerId;
        from_id = fromId;
        this.date = date;
        edit_date = editDate;
        this.message = message;
        this.pinned = pinned;
        reply_to_id = replyToId;
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
}
