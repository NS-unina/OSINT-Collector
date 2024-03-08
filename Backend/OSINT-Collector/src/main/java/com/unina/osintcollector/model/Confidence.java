package com.unina.osintcollector.model;

import com.unina.osintcollector.model.ModerationCategory;
import org.springframework.data.neo4j.core.schema.GeneratedValue;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.RelationshipProperties;
import org.springframework.data.neo4j.core.schema.TargetNode;

@RelationshipProperties
public class Confidence {

    @Id
    @GeneratedValue
    private Long id;

    private final Double confidence;

    @TargetNode
    private ModerationCategory moderationCategory;

    public Confidence(Double confidence) {
        this.confidence = confidence;
    }

    public Long getId() {
        return id;
    }

    public Double getConfidence() {
        return confidence;
    }

    public ModerationCategory getModerationCategory() {
        return moderationCategory;
    }
}
