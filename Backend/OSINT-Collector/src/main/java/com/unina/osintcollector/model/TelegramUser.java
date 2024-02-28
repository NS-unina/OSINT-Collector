package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;

import java.util.Date;
import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("TelegramUser")
public class TelegramUser {

    @Id
    private final String id;

    private final String first_name;
    private final String last_name;
    private final String username;
    private final String phone;
    private final Boolean bot;
    private final Boolean verified;
    private final Boolean premium;
    private final Boolean flag;

    @Relationship(type = "SENT", direction = OUTGOING)
    private Set<TelegramMessage> messages;

    public TelegramUser(String id, String firstName, String lastName, String username, String phone, Boolean bot, Boolean verified, Boolean premium, Boolean flag) {
        this.id = id;
        first_name = firstName;
        last_name = lastName;
        this.username = username;
        this.phone = phone;
        this.bot = bot;
        this.verified = verified;
        this.premium = premium;
        this.flag = flag;
    }

    public String getId() {
        return id;
    }

    public String getFirst_name() {
        return first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public String getUsername() {
        return username;
    }

    public String getPhone() {
        return phone;
    }

    public Boolean getBot() {
        return bot;
    }

    public Boolean getVerified() {
        return verified;
    }

    public Boolean getPremium() {
        return premium;
    }

    public Set<TelegramMessage> getMessages() {
        return messages;
    }

    public Boolean getFlag() {
        return flag;
    }
}

