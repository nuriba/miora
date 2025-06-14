package com.miora.repository;

import com.miora.domain.model.Avatar;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface AvatarRepository extends R2dbcRepository<Avatar, Long> {
    
    Flux<Avatar> findByUserId(Long userId);
    
    @Query("SELECT COUNT(*) FROM avatars WHERE user_id = :userId")
    Mono<Long> countByUserId(Long userId);
    
    Flux<Avatar> findByUserIdAndIsPublic(Long userId, Boolean isPublic);
    
    @Query("SELECT * FROM avatars WHERE user_id = :userId AND is_active = true LIMIT 1")
    Mono<Avatar> findActiveByUserId(Long userId);
    
    @Query("SELECT * FROM avatars WHERE is_public = true ORDER BY created_at DESC LIMIT :limit OFFSET :offset")
    Flux<Avatar> findPublicAvatars(int limit, int offset);
} 