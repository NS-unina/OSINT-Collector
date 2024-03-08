package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.TelegramGroup;
import com.unina.osintcollector.model.TelegramMessage;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

public interface TelegramGroupRepository extends ReactiveNeo4jRepository<TelegramGroup, String> {
    @Query("""
            MATCH (g:TelegramGroup)-[:PUBLISHED]->(m)
            RETURN {messages: COLLECT(properties(m)), group: properties(g)} as result
            """)
    Flux<Map<String, Object>> getGroups();

    @Query("""
            MATCH (telegramGroup:`TelegramGroup`) RETURN telegramGroup{.about, .date, .flag, .id, .participants_count, .title, .username, __nodeLabels__: labels(telegramGroup), __elementId__: id(telegramGroup), TelegramGroup_PUBLISHED_TelegramMessage: [(telegramGroup)-[:`PUBLISHED`]->(telegramGroup_messages:`TelegramMessage`) | telegramGroup_messages{.date, .edit_date, .from_id, .id, .message, .messageType, .peerId, .pinned, .processed, .reply_to_id, __nodeLabels__: labels(telegramGroup_messages), __elementId__: id(telegramGroup_messages), TelegramMessage_REFERS_TO_MODERATION_ModerationCategory: [(telegramGroup_messages)-[r:`REFERS_TO_MODERATION`]->(telegramGroup_messages_moderationCategories:`ModerationCategory`) | telegramGroup_messages_moderationCategories{confidence: r.confidence, .name, __nodeLabels__: labels(telegramGroup_messages_moderationCategories), __elementId__: id(telegramGroup_messages_moderationCategories)}], TelegramMessage_SENT_BY_TelegramUser: [(telegramGroup_messages)-[:`SENT_BY`]->(telegramGroup_messages_user:`TelegramUser`) | telegramGroup_messages_user{.bot, .first_name, .flag, .id, .last_name, .phone, .premium, .username, .verified, __nodeLabels__: labels(telegramGroup_messages_user), __elementId__: id(telegramGroup_messages_user)}], TelegramMessage_REFERS_TO_Category: [(telegramGroup_messages)-[:`REFERS_TO`]->(telegramGroup_messages_categories:`Category`) | telegramGroup_messages_categories{.alsoKnownAs, .name, .uri, __nodeLabels__: labels(telegramGroup_messages_categories), __elementId__: id(telegramGroup_messages_categories)}]}]}
            """)
    Flux<TelegramGroup> getTelegramGroups();
}
