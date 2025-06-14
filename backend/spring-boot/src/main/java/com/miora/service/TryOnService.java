package com.miora.service;

import com.miora.domain.model.TryOnSession;
import com.miora.domain.model.ProcessingStatus;
import com.miora.repository.TryOnSessionRepository;
import com.miora.repository.AvatarRepository;
import com.miora.repository.GarmentRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Service class for virtual try-on business logic
 */
@Service
public class TryOnService {

    private final TryOnSessionRepository tryOnSessionRepository;
    private final AvatarRepository avatarRepository;
    private final GarmentRepository garmentRepository;
    private final MLIntegrationService mlIntegrationService;

    public TryOnService(TryOnSessionRepository tryOnSessionRepository,
                       AvatarRepository avatarRepository,
                       GarmentRepository garmentRepository,
                       MLIntegrationService mlIntegrationService) {
        this.tryOnSessionRepository = tryOnSessionRepository;
        this.avatarRepository = avatarRepository;
        this.garmentRepository = garmentRepository;
        this.mlIntegrationService = mlIntegrationService;
    }

    // Create new try-on session
    public Mono<TryOnSession> createTryOnSession(Long userId, CreateTryOnRequest request) {
        return validateTryOnRequest(userId, request.getAvatarId(), request.getGarmentId())
                .then(Mono.fromCallable(() -> {
                    TryOnSession session = new TryOnSession();
                    session.setUserId(userId);
                    session.setAvatarId(request.getAvatarId());
                    session.setGarmentId(request.getGarmentId());
                    session.setSessionName(request.getSessionName());
                    session.setProcessingStatus(ProcessingStatus.PENDING);
                    session.setIsPublic(request.getIsPublic() != null ? request.getIsPublic() : false);
                    session.setCreatedAt(LocalDateTime.now());
                    session.setUpdatedAt(LocalDateTime.now());
                    return session;
                }))
                .flatMap(tryOnSessionRepository::save)
                .flatMap(this::startTryOnProcessing);
    }

    // Start try-on processing
    public Mono<TryOnSession> startTryOnProcessing(TryOnSession session) {
        return Mono.fromCallable(() -> {
            session.setProcessingStatus(ProcessingStatus.PROCESSING);
            session.setUpdatedAt(LocalDateTime.now());
            return session;
        })
        .flatMap(tryOnSessionRepository::save)
        .flatMap(savedSession -> 
            mlIntegrationService.processTryOnAsync(savedSession)
                .thenReturn(savedSession)
        );
    }

    // Get try-on session by ID
    public Mono<TryOnSession> getTryOnSession(Long userId, Long sessionId) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .filter(session -> session.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to access this session")));
    }

    // Get user's try-on sessions
    public Flux<TryOnSession> getUserTryOnSessions(Long userId) {
        return tryOnSessionRepository.findByUserIdOrderByCreatedAtDesc(userId);
    }

    // Get user's saved sessions
    public Flux<TryOnSession> getUserSavedSessions(Long userId) {
        return tryOnSessionRepository.findByUserIdAndIsSavedTrueOrderByCreatedAtDesc(userId);
    }

    // Get sessions for avatar
    public Flux<TryOnSession> getAvatarSessions(Long userId, Long avatarId) {
        return avatarRepository.findById(avatarId)
                .filter(avatar -> avatar.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to access this avatar")))
                .flatMapMany(avatar -> tryOnSessionRepository.findByAvatarIdOrderByCreatedAtDesc(avatarId));
    }

    // Get sessions for garment
    public Flux<TryOnSession> getGarmentSessions(Long garmentId) {
        return tryOnSessionRepository.findByGarmentIdOrderByCreatedAtDesc(garmentId);
    }

    // Get public try-on sessions (for discovery)
    public Flux<TryOnSession> getPublicSessions(int page, int size) {
        return tryOnSessionRepository.findPublicSessions(size, page * size);
    }

    // Get high-quality sessions
    public Flux<TryOnSession> getHighQualitySessions(int limit) {
        return tryOnSessionRepository.findHighQualitySessions(new BigDecimal("0.8"), limit);
    }

    // Save try-on session
    public Mono<TryOnSession> saveTryOnSession(Long userId, Long sessionId) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .filter(session -> session.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to save this session")))
                .flatMap(session -> {
                    session.setIsSaved(true);
                    session.setUpdatedAt(LocalDateTime.now());
                    return tryOnSessionRepository.save(session);
                });
    }

    // Update session visibility
    public Mono<TryOnSession> updateSessionVisibility(Long userId, Long sessionId, boolean isPublic) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .filter(session -> session.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to update this session")))
                .flatMap(session -> {
                    session.setIsPublic(isPublic);
                    session.setUpdatedAt(LocalDateTime.now());
                    return tryOnSessionRepository.save(session);
                });
    }

    // Delete try-on session
    public Mono<Void> deleteTryOnSession(Long userId, Long sessionId) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .filter(session -> session.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to delete this session")))
                .flatMap(tryOnSessionRepository::delete);
    }

    // Complete try-on processing (called by ML service)
    public Mono<TryOnSession> completeTryOnProcessing(Long sessionId, TryOnResult result) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .flatMap(session -> {
                    session.markAsCompleted(
                        result.getResultImageUrl(),
                        result.getProcessingTimeMs(),
                        result.getQualityScore()
                    );
                    
                    // Update garment try-on count
                    garmentRepository.incrementTryOnCount(session.getGarmentId()).subscribe();
                    
                    return tryOnSessionRepository.save(session);
                });
    }

    // Mark try-on processing as failed
    public Mono<TryOnSession> failTryOnProcessing(Long sessionId, String errorMessage) {
        return tryOnSessionRepository.findById(sessionId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Try-on session not found")))
                .flatMap(session -> {
                    session.markAsFailed(errorMessage);
                    return tryOnSessionRepository.save(session);
                });
    }

    // Get processing statistics
    public Mono<TryOnStatistics> getTryOnStatistics(Long userId) {
        return Mono.zip(
            tryOnSessionRepository.countByUserId(userId),
            tryOnSessionRepository.countCompletedSessionsByUserId(userId),
            tryOnSessionRepository.getAverageProcessingTime(),
            tryOnSessionRepository.getAverageQualityScore()
        ).map(tuple -> new TryOnStatistics(
            tuple.getT1(), // total sessions
            tuple.getT2(), // completed sessions
            tuple.getT3() != null ? tuple.getT3().intValue() : 0, // avg processing time
            tuple.getT4() != null ? tuple.getT4() : BigDecimal.ZERO // avg quality score
        ));
    }

    // Check if user has tried this combination before
    public Mono<Boolean> hasUserTriedCombination(Long userId, Long avatarId, Long garmentId) {
        return tryOnSessionRepository.hasUserTriedCombination(userId, avatarId, garmentId);
    }

    // Get recent sessions for specific avatar-garment combination
    public Flux<TryOnSession> getRecentSessionsForCombination(Long avatarId, Long garmentId, int limit) {
        return tryOnSessionRepository.findRecentSessionsForAvatarGarment(avatarId, garmentId, limit);
    }

    // Validate try-on request
    private Mono<Void> validateTryOnRequest(Long userId, Long avatarId, Long garmentId) {
        return Mono.zip(
            avatarRepository.findById(avatarId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Avatar not found")))
                .filter(avatar -> avatar.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to use this avatar"))),
            garmentRepository.findById(garmentId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Garment not found")))
                .filter(garment -> garment.isProcessed())
                .switchIfEmpty(Mono.error(new IllegalStateException("Garment is not ready for try-on")))
        ).then();
    }

    // DTOs
    public static class CreateTryOnRequest {
        private Long avatarId;
        private Long garmentId;
        private String sessionName;
        private Boolean isPublic;

        // Getters and setters
        public Long getAvatarId() { return avatarId; }
        public void setAvatarId(Long avatarId) { this.avatarId = avatarId; }
        public Long getGarmentId() { return garmentId; }
        public void setGarmentId(Long garmentId) { this.garmentId = garmentId; }
        public String getSessionName() { return sessionName; }
        public void setSessionName(String sessionName) { this.sessionName = sessionName; }
        public Boolean getIsPublic() { return isPublic; }
        public void setIsPublic(Boolean isPublic) { this.isPublic = isPublic; }
    }

    public static class TryOnResult {
        private String resultImageUrl;
        private Integer processingTimeMs;
        private BigDecimal qualityScore;

        public TryOnResult(String resultImageUrl, Integer processingTimeMs, BigDecimal qualityScore) {
            this.resultImageUrl = resultImageUrl;
            this.processingTimeMs = processingTimeMs;
            this.qualityScore = qualityScore;
        }

        // Getters
        public String getResultImageUrl() { return resultImageUrl; }
        public Integer getProcessingTimeMs() { return processingTimeMs; }
        public BigDecimal getQualityScore() { return qualityScore; }
    }

    public static class TryOnStatistics {
        private Long totalSessions;
        private Long completedSessions;
        private Integer averageProcessingTimeMs;
        private BigDecimal averageQualityScore;

        public TryOnStatistics(Long totalSessions, Long completedSessions, 
                              Integer averageProcessingTimeMs, BigDecimal averageQualityScore) {
            this.totalSessions = totalSessions;
            this.completedSessions = completedSessions;
            this.averageProcessingTimeMs = averageProcessingTimeMs;
            this.averageQualityScore = averageQualityScore;
        }

        // Getters
        public Long getTotalSessions() { return totalSessions; }
        public Long getCompletedSessions() { return completedSessions; }
        public Integer getAverageProcessingTimeMs() { return averageProcessingTimeMs; }
        public BigDecimal getAverageQualityScore() { return averageQualityScore; }
    }
} 