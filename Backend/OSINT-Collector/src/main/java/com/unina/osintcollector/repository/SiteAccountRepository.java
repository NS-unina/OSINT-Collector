package com.unina.osintcollector.repository;

import com.unina.osintcollector.model.SiteAccount;
import org.springframework.data.neo4j.repository.ReactiveNeo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public interface SiteAccountRepository extends ReactiveNeo4jRepository<SiteAccount, Long> {

    @Query("""
     MERGE (u:Username {username: $username})
     WITH u
     UNWIND $sites AS site
     MERGE (s:SiteAccount {id: site.id, site: site.site, url: site.url, status: site.status})
     MERGE (u)-[:ASSOCIATED_WITH]->(s)
     """)
    Mono<SiteAccount> saveSites(String username, List<Map<String, Object>> sites);

}
