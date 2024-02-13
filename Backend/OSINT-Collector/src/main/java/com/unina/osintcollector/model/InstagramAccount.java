package com.unina.osintcollector.model;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;
import org.springframework.stereotype.Indexed;

import java.util.Set;

import static org.springframework.data.neo4j.core.schema.Relationship.Direction.OUTGOING;

@Node("InstagramAccount")
public class InstagramAccount {

    @Id
    private final String id;
    private final String full_name;
    private final String username;
    private final String profile_pic_url;
    private final String[] bio_links;
    private final String biography;
    private final Long follow;
    private final Long followers;

    @Relationship(type = "PUBLISHED", direction = OUTGOING)
    private Set<InstagramPost> posts;

    public InstagramAccount(String id, String full_name, String username, String profile_pic_url, String[] bio_links, String biography, Long follow, Long followers) {
        this.id = id;
        this.full_name = full_name;
        this.username = username;
        this.profile_pic_url = profile_pic_url;
        this.bio_links = bio_links;
        this.biography = biography;
        this.follow = follow;
        this.followers = followers;
    }

    public String getId() {
        return id;
    }

    public String getFull_name() {
        return full_name;
    }

    public String getUsername() {
        return username;
    }

    public String getProfile_pic_url() {
        return profile_pic_url;
    }

    public String[] getBio_links() {
        return bio_links;
    }

    public String getBiography() {
        return biography;
    }

    public Long getFollow() {
        return follow;
    }

    public Long getFollowers() {
        return followers;
    }

    public Set<InstagramPost> getPosts() {
        return posts;
    }
}
