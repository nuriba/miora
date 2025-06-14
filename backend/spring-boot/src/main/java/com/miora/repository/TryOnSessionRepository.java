package com.miora.repository;

import com.miora.domain.model.TryOnSession;
import com.miora.domain.model.ProcessingStatus;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;

/**
 * Repository interface for TryOnSession entity operations
 */
@Repository
public interface TryOnSessionRepository extends R2dbcRepository<TryOnSession, Long> {

    // Find sessions by user
    Flux<TryOnSession> findByUserIdOrderByCreatedAtDesc(Long userId);
    
    // Find user's saved sessions
    Flux<TryOnSession> findByUserIdAndIsSavedTrueOrderByCreatedAtDesc(Long userId);
    
    // Find user's public sessions
    Flux<TryOnSession> findByUserIdAndIsPublicTrueOrderByCreatedAtDesc(Long userId);
    
    // Find sessions by avatar
    Flux<TryOnSession> findByAvatarIdOrderByCreatedAtDesc(Long avatarId);
    
    // Find sessions by garment
    Flux<TryOnSession> findByGarmentIdOrderByCreatedAtDesc(Long garmentId);
    
    // Find sessions by processing status
    Flux<TryOnSession> findByProcessingStatusOrderByCreatedAtAsc(ProcessingStatus status);
    
    // Find user's sessions by processing status
    Flux<TryOnSession> findByUserIdAndProcessingStatusOrderByCreatedAtAsc(Long userId, ProcessingStatus status);
    
    // Find public sessions (for discovery)
    @Query("SELECT * FROM try_on_sessions WHERE is_public = true ORDER BY created_at DESC LIMIT :limit OFFSET :offset")
    Flux<TryOnSession> findPublicSessions(int limit, int offset);
    
    // Find high-quality sessions
    @Query("SELECT * FROM try_on_sessions WHERE quality_score >= :minScore AND is_public = true ORDER BY quality_score DESC, created_at DESC LIMIT :limit")
    Flux<TryOnSession> findHighQualitySessions(BigDecimal minScore, int limit);
    
    // Find sessions with results
    @Query("SELECT * FROM try_on_sessions WHERE result_image_url IS NOT NULL AND user_id = :userId ORDER BY created_at DESC")
    Flux<TryOnSession> findUserSessionsWithResults(Long userId);
    
    // Find recent sessions for avatar-garment combination
    @Query("SELECT * FROM try_on_sessions WHERE avatar_id = :avatarId AND garment_id = :garmentId ORDER BY created_at DESC LIMIT :limit")
    Flux<TryOnSession> findRecentSessionsForAvatarGarment(Long avatarId, Long garmentId, int limit);
    
    // Check if user has tried this combination before
    @Query("SELECT COUNT(*) > 0 FROM try_on_sessions WHERE user_id = :userId AND avatar_id = :avatarId AND garment_id = :garmentId")
    Mono<Boolean> hasUserTriedCombination(Long userId, Long avatarId, Long garmentId);
    
    // Find sessions with specific avatar and garment
    Flux<TryOnSession> findByAvatarIdAndGarmentIdOrderByCreatedAtDesc(Long avatarId, Long garmentId);
    
    // Count user's sessions
    Mono<Long> countByUserId(Long userId);
    
    // Count sessions by processing status
    Mono<Long> countByProcessingStatus(ProcessingStatus status);
    
    // Count completed sessions for user
    @Query("SELECT COUNT(*) FROM try_on_sessions WHERE user_id = :userId AND processing_status = 'COMPLETED'")
    Mono<Long> countCompletedSessionsByUserId(Long userId);
    
    // Get average processing time
    @Query("SELECT AVG(processing_time_ms) FROM try_on_sessions WHERE processing_status = 'COMPLETED' AND processing_time_ms IS NOT NULL")
    Mono<Double> getAverageProcessingTime();
    
    // Get average quality score
    @Query("SELECT AVG(quality_score) FROM try_on_sessions WHERE processing_status = 'COMPLETED' AND quality_score IS NOT NULL")
    Mono<BigDecimal> getAverageQualityScore();
    
    // Find sessions pending for too long (potential stuck processes)
    @Query("SELECT * FROM try_on_sessions WHERE processing_status IN ('PENDING', 'PROCESSING') AND created_at < NOW() - INTERVAL :minutes MINUTE")
    Flux<TryOnSession> findStuckSessions(int minutes);
    
    // Update processing status and result
    @Query("""
        UPDATE try_on_sessions 
        SET processing_status = :status, 
            result_image_url = :resultUrl, 
            processing_time_ms = :processingTime, 
            quality_score = :qualityScore, 
            updated_at = NOW() 
        WHERE id = :id
        """)
    Mono<Void> updateSessionResult(Long id, ProcessingStatus status, String resultUrl, Integer processingTime, BigDecimal qualityScore);
    
    // Mark session as saved
    @Query("UPDATE try_on_sessions SET is_saved = :isSaved, updated_at = NOW() WHERE id = :id")
    Mono<Void> updateSavedStatus(Long id, boolean isSaved);
    
    // Update public status
    @Query("UPDATE try_on_sessions SET is_public = :isPublic, updated_at = NOW() WHERE id = :id")
    Mono<Void> updatePublicStatus(Long id, boolean isPublic);
    
    // Delete old unsaved sessions
    @Query("DELETE FROM try_on_sessions WHERE is_saved = false AND created_at < NOW() - INTERVAL :days DAY")
    Mono<Void> deleteOldUnsavedSessions(int days);
    
    // Find sessions with avatar, garment, and user details
    @Query("""
        SELECT ts.*, a.name as avatar_name, g.name as garment_name, u.display_name as user_name
        FROM try_on_sessions ts
        LEFT JOIN avatars a ON ts.avatar_id = a.id
        LEFT JOIN garments g ON ts.garment_id = g.id  
        LEFT JOIN users u ON ts.user_id = u.id
        WHERE ts.user_id = :userId 
        ORDER BY ts.created_at DESC
        """)
    Flux<TryOnSession> findUserSessionsWithDetails(Long userId);
    
    // Find popular avatar-garment combinations
    @Query("""
        SELECT avatar_id, garment_id, COUNT(*) as session_count
        FROM try_on_sessions 
        WHERE processing_status = 'COMPLETED'
        GROUP BY avatar_id, garment_id
        HAVING COUNT(*) >= :minSessions
        ORDER BY session_count DESC
        LIMIT :limit
        """)
    Flux<TryOnSession> findPopularCombinations(int minSessions, int limit);
} 