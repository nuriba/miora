package com.miora.controller;

import com.miora.domain.model.TryOnSession;
import com.miora.service.TryOnService;
import com.miora.security.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import jakarta.validation.Valid;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * REST Controller for virtual try-on session APIs
 */
@RestController
@RequestMapping("/api/v1/try-on")
@CrossOrigin(origins = "*")
public class TryOnController {

    private final TryOnService tryOnService;
    private final JwtUtil jwtUtil;

    public TryOnController(TryOnService tryOnService, JwtUtil jwtUtil) {
        this.tryOnService = tryOnService;
        this.jwtUtil = jwtUtil;
    }

    // Create new try-on session
    @PostMapping
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<TryOnSessionResponse>> createTryOnSession(
            @RequestHeader("Authorization") String token,
            @RequestBody @Valid CreateTryOnSessionRequest request) {
        
        Long userId = extractUserIdFromToken(token);
        
        TryOnService.CreateTryOnRequest serviceRequest = new TryOnService.CreateTryOnRequest();
        serviceRequest.setAvatarId(request.getAvatarId());
        serviceRequest.setGarmentId(request.getGarmentId());
        serviceRequest.setSessionName(request.getSessionName());
        serviceRequest.setIsPublic(request.getIsPublic());
        
        return tryOnService.createTryOnSession(userId, serviceRequest)
                .map(session -> ResponseEntity.status(HttpStatus.CREATED)
                        .body(mapToResponse(session)))
                .onErrorResume(this::handleError);
    }

    // Get try-on session by ID
    @GetMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<TryOnSessionResponse>> getTryOnSession(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.getTryOnSession(userId, id)
                .map(session -> ResponseEntity.ok(mapToResponse(session)))
                .onErrorResume(this::handleError);
    }

    // Get user's try-on sessions
    @GetMapping("/my-sessions")
    @PreAuthorize("hasRole('USER')")
    public Flux<TryOnSessionResponse> getMyTryOnSessions(
            @RequestHeader("Authorization") String token) {
        
        Long userId = extractUserIdFromToken(token);
        return tryOnService.getUserTryOnSessions(userId)
                .map(this::mapToResponse);
    }

    // Get user's saved try-on sessions
    @GetMapping("/my-sessions/saved")
    @PreAuthorize("hasRole('USER')")
    public Flux<TryOnSessionResponse> getMySavedTryOnSessions(
            @RequestHeader("Authorization") String token) {
        
        Long userId = extractUserIdFromToken(token);
        return tryOnService.getUserSavedSessions(userId)
                .map(this::mapToResponse);
    }

    // Get public try-on sessions (discovery)
    @GetMapping("/public")
    public Flux<TryOnSessionResponse> getPublicTryOnSessions(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return tryOnService.getPublicSessions(page, size)
                .map(this::mapToResponse);
    }

    // Get try-on sessions for a specific avatar
    @GetMapping("/avatar/{avatarId}")
    @PreAuthorize("hasRole('USER')")
    public Flux<TryOnSessionResponse> getAvatarTryOnSessions(
            @RequestHeader("Authorization") String token,
            @PathVariable Long avatarId) {
        
        Long userId = extractUserIdFromToken(token);
        return tryOnService.getAvatarSessions(userId, avatarId)
                .map(this::mapToResponse);
    }

    // Get try-on sessions for a specific garment
    @GetMapping("/garment/{garmentId}")
    public Flux<TryOnSessionResponse> getGarmentTryOnSessions(
            @PathVariable Long garmentId) {
        return tryOnService.getGarmentSessions(garmentId)
                .map(this::mapToResponse);
    }

    // Save/unsave try-on session
    @PutMapping("/{id}/save")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<TryOnSessionResponse>> saveTryOnSession(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.saveTryOnSession(userId, id)
                .map(session -> ResponseEntity.ok(mapToResponse(session)))
                .onErrorResume(this::handleError);
    }

    // Update session visibility
    @PutMapping("/{id}/visibility")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<TryOnSessionResponse>> updateSessionVisibility(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id,
            @RequestBody VisibilityUpdateRequest request) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.updateSessionVisibility(userId, id, request.getIsPublic())
                .map(session -> ResponseEntity.ok(mapToResponse(session)))
                .onErrorResume(this::handleError);
    }

    // Delete try-on session
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<Void>> deleteTryOnSession(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.deleteTryOnSession(userId, id)
                .then(Mono.just(ResponseEntity.noContent().<Void>build()))
                .onErrorResume(this::handleError);
    }

    // Get try-on statistics
    @GetMapping("/statistics")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<TryOnStatisticsResponse>> getTryOnStatistics(
            @RequestHeader("Authorization") String token) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.getTryOnStatistics(userId)
                .map(stats -> ResponseEntity.ok(mapToStatisticsResponse(stats)))
                .onErrorResume(this::handleError);
    }

    // Get high quality sessions
    @GetMapping("/high-quality")
    public Flux<TryOnSessionResponse> getHighQualitySessions(
            @RequestParam(defaultValue = "10") int limit) {
        return tryOnService.getHighQualitySessions(limit)
                .map(this::mapToResponse);
    }

    // Check if user has tried combination
    @GetMapping("/check-combination")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<CombinationCheckResponse>> checkCombination(
            @RequestHeader("Authorization") String token,
            @RequestParam Long avatarId,
            @RequestParam Long garmentId) {
        
        Long userId = extractUserIdFromToken(token);
        
        return tryOnService.hasUserTriedCombination(userId, avatarId, garmentId)
                .map(hasTried -> ResponseEntity.ok(new CombinationCheckResponse(hasTried)))
                .onErrorResume(this::handleError);
    }

    // Helper methods
    private Long extractUserIdFromToken(String token) {
        String jwt = token.replace("Bearer ", "");
        return Long.valueOf(jwtUtil.getUserIdFromToken(jwt));
    }

    private TryOnSessionResponse mapToResponse(TryOnSession session) {
        return new TryOnSessionResponse(
            session.getId(),
            session.getUserId(),
            session.getAvatarId(),
            session.getGarmentId(),
            session.getResultImageUrl(),
            session.getProcessingStatus().name(),
            session.getQualityScore(),
            session.getProcessingTimeMs(),
            session.getIsPublic(),
            session.getIsSaved(),
            session.getSessionName(),
            session.getCreatedAt(),
            session.getUpdatedAt()
        );
    }

    private TryOnStatisticsResponse mapToStatisticsResponse(TryOnService.TryOnStatistics statistics) {
        return new TryOnStatisticsResponse(
            statistics.getTotalSessions(),
            statistics.getCompletedSessions(),
            statistics.getAverageProcessingTimeMs(),
            statistics.getAverageQualityScore()
        );
    }

    private <T> Mono<ResponseEntity<T>> handleError(Throwable error) {
        if (error instanceof IllegalArgumentException) {
            return Mono.just(ResponseEntity.badRequest().build());
        } else if (error instanceof SecurityException) {
            return Mono.just(ResponseEntity.status(HttpStatus.FORBIDDEN).build());
        } else if (error instanceof IllegalStateException) {
            return Mono.just(ResponseEntity.status(HttpStatus.CONFLICT).build());
        } else {
            return Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build());
        }
    }

    // DTOs
    public static class CreateTryOnSessionRequest {
        private Long avatarId;
        private Long garmentId;
        private String sessionName;
        private Boolean isPublic = false;

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

    public static class VisibilityUpdateRequest {
        private Boolean isPublic;

        public Boolean getIsPublic() { return isPublic; }
        public void setIsPublic(Boolean isPublic) { this.isPublic = isPublic; }
    }

    public static class TryOnSessionResponse {
        private Long id;
        private Long userId;
        private Long avatarId;
        private Long garmentId;
        private String resultImageUrl;
        private String processingStatus;
        private BigDecimal qualityScore;
        private Integer processingTimeMs;
        private Boolean isPublic;
        private Boolean isSaved;
        private String sessionName;
        private LocalDateTime createdAt;
        private LocalDateTime updatedAt;

        public TryOnSessionResponse(Long id, Long userId, Long avatarId, Long garmentId,
                                  String resultImageUrl, String processingStatus,
                                  BigDecimal qualityScore, Integer processingTimeMs,
                                  Boolean isPublic, Boolean isSaved, String sessionName,
                                  LocalDateTime createdAt, LocalDateTime updatedAt) {
            this.id = id;
            this.userId = userId;
            this.avatarId = avatarId;
            this.garmentId = garmentId;
            this.resultImageUrl = resultImageUrl;
            this.processingStatus = processingStatus;
            this.qualityScore = qualityScore;
            this.processingTimeMs = processingTimeMs;
            this.isPublic = isPublic;
            this.isSaved = isSaved;
            this.sessionName = sessionName;
            this.createdAt = createdAt;
            this.updatedAt = updatedAt;
        }

        // Getters
        public Long getId() { return id; }
        public Long getUserId() { return userId; }
        public Long getAvatarId() { return avatarId; }
        public Long getGarmentId() { return garmentId; }
        public String getResultImageUrl() { return resultImageUrl; }
        public String getProcessingStatus() { return processingStatus; }
        public BigDecimal getQualityScore() { return qualityScore; }
        public Integer getProcessingTimeMs() { return processingTimeMs; }
        public Boolean getIsPublic() { return isPublic; }
        public Boolean getIsSaved() { return isSaved; }
        public String getSessionName() { return sessionName; }
        public LocalDateTime getCreatedAt() { return createdAt; }
        public LocalDateTime getUpdatedAt() { return updatedAt; }
    }

    public static class TryOnStatisticsResponse {
        private Long totalSessions;
        private Long completedSessions;
        private Integer averageProcessingTimeMs;
        private BigDecimal averageQualityScore;

        public TryOnStatisticsResponse(Long totalSessions, Long completedSessions,
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

    public static class CombinationCheckResponse {
        private Boolean hasTried;

        public CombinationCheckResponse(Boolean hasTried) {
            this.hasTried = hasTried;
        }

        public Boolean getHasTried() { return hasTried; }
    }
} 