package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;

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

    public TelegramUser(String id, String first_name, String last_name, String username, String phone, Boolean bot, Boolean verified, Boolean premium, Boolean flag) {
        this.id = id;
        this.first_name = first_name;
        this.last_name = last_name;
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

    public Boolean getFlag() {
        return flag;
    }
}

