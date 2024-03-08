package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.InstagramPost;
import com.unina.osintcollector.model.TelegramMessage;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public interface TelegramMessageRepository extends ReactiveNeo4jRepository<TelegramMessage, String> {

    @Query("""
         UNWIND $users AS user
         MERGE (u:TelegramUser {id: user.id})
         ON CREATE SET u.first_name = user.first_name, u.last_name = user.last_name, u.username = user.username, u.phone = user.phone, u.bot = user.bot, u.verified = user.verified, u.premium = user.premium
         ON MATCH SET u.first_name = user.first_name, u.last_name = user.last_name, u.username = user.username, u.phone = user.phone, u.bot = user.bot, u.verified = user.verified, u.premium = user.premium
         MERGE (ch:TelegramGroup {id: $channel.id})
         ON CREATE SET ch.about = $channel.about, ch.title = $channel.title, ch.username = $channel.username, ch.date = $channel.date, ch.participants_count = $channel.participants_count
         ON MATCH SET ch.about = $channel.about, ch.title = $channel.title, ch.username = $channel.username, ch.date = $channel.date, ch.participants_count = $channel.participants_count
         WITH ch
         UNWIND $messages AS message
         MERGE (m:TelegramMessage {id: message.id, peer_id: message.peer_id, from_id: message.from_id})
         ON CREATE SET m.messageType = message.messageType, m.peer_id = message.peer_id, m.from_id = message.from_id, m.date = message.date, m.edit_date = message.edit_date, m.message = message.message, m.pinned = message.pinned, m.reply_to_id = message.reply_to_id, m.processed = message.processed
         ON MATCH SET m.messageType = message.messageType, m.peer_id = message.peer_id, m.from_id = message.from_id, m.date = message.date, m.edit_date = message.edit_date, m.message = message.message, m.pinned = message.pinned, m.reply_to_id = message.reply_to_id, m.processed = message.processed
         WITH ch, m
         OPTIONAL MATCH(repliedMess:TelegramMessage {id: m.reply_to_id})
         FOREACH(ignoreMe IN CASE WHEN m.reply_to_id IS NOT NULL THEN [1] ELSE [] END |
            MERGE (m)-[:REPLY_TO]->(repliedMess)
         )
         WITH ch, m
         MATCH (user:TelegramUser {id: m.from_id})
         MERGE (m)-[:SENT_BY]->(user)
         MERGE (ch)-[:PUBLISHED]->(m)
         SET m.lowercase_message = toLower(m.message)
         WITH user, ch, m AS messages
         CALL apoc.nlp.gcp.entities.stream(messages, {
            nodeProperty: 'lowercase_message',
            key: 'AIzaSyC_RV2nb7vjC32i1jd6mj92p1ww6BPga0g'
         })
         YIELD node, value
         WITH node, value, user, ch
         UNWIND value.entities AS entity
         WITH entity, node, user, ch
         MATCH (cat:Category) WHERE cat.name = entity.name OR cat.alsoKnownAs = entity.name
         MERGE (node)-[:REFERS_TO]->(cat)
         WITH node, count(cat) as matchedCategories, user, ch
         FOREACH (ignoreMe IN CASE WHEN matchedCategories > 0 THEN [1] ELSE [] END |
            SET node.processed = true, user.flag = true, ch.flag = true
         )
        """)
    Mono<TelegramMessage> saveMessagesChannelUser(List<Map<String, Object>> messages, Map<String, Object> channel, List<Map<String, Object>> users);

    @Query("""
            MATCH (t:TelegramGroup {id: $peerId})-[:PUBLISHED]->(m)
            WITH t, m as messages
            CALL apoc.nlp.gcp.moderate.stream(messages, {
              nodeProperty: 'lowercase_message',
              key: 'AIzaSyC_RV2nb7vjC32i1jd6mj92p1ww6BPga0g'
            })
            YIELD node, value
            WITH node, value, t
            UNWIND value.moderationCategories AS category
            WITH category, node, t WHERE category.confidence > 0.7
            MERGE (cat:ModerationCategory {name: category.name})
            MERGE (node)-[:REFERS_TO_MODERATION {confidence: category.confidence}]->(cat)
            WITH node, count(cat) as matchedCategories, t
            FOREACH (ignoreMe IN CASE WHEN matchedCategories > 0 THEN [1] ELSE [] END |
                SET t.flag = true, node.processed = true
            )
            """)
    Flux<TelegramMessage> ModerateGroup(String peerId);

    @Query("""
            MATCH (telegramMessage:`TelegramMessage`) WHERE telegramMessage.peer_id = $peerId RETURN telegramMessage{.date, .edit_date, .from_id, .id, .message, .messageType, .peer_id, .pinned, .processed, .reply_to_id, __nodeLabels__: labels(telegramMessage), __elementId__: id(telegramMessage), TelegramMessage_SENT_BY_TelegramUser: [(telegramMessage)-[:`SENT_BY`]->(telegramMessage_user:`TelegramUser`) | telegramMessage_user{.bot, .first_name, .flag, .id, .last_name, .phone, .premium, .username, .verified, __nodeLabels__: labels(telegramMessage_user), __elementId__: id(telegramMessage_user)}], TelegramMessage_REFERS_TO_MODERATION_ModerationCategory: [(telegramMessage)-[TelegramMessage__relationship__ModerationCategory:`REFERS_TO_MODERATION`]->(telegramMessage_moderationCategories:`ModerationCategory`) | telegramMessage_moderationCategories{.name, __nodeLabels__: labels(telegramMessage_moderationCategories), __elementId__: id(telegramMessage_moderationCategories), TelegramMessage__relationship__ModerationCategory}], TelegramMessage_REFERS_TO_Category: [(telegramMessage)-[:`REFERS_TO`]->(telegramMessage_categories:`Category`) | telegramMessage_categories{.alsoKnownAs, .name, .uri, __nodeLabels__: labels(telegramMessage_categories), __elementId__: id(telegramMessage_categories)}]}  
            """)
    Flux<TelegramMessage> findTelegramMessageByPeerId(String peerId);
}
