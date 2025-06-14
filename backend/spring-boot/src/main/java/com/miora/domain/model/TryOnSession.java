package com.miora.domain.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Represents a virtual try-on session in the Miora platform.
 * Stores the result of an avatar trying on a garment.
 */

@Table("try_on_sessions")
public class TryOnSession {

    @Id
    private Long id;

    @Column("user_id")
    private Long userId;

    @Column("avatar_id")
    private Long avatarId;

    @Column("garment_id")
    private Long garmentId;

    @Column("session_name")
    private String sessionName;

    @Column("result_image_url")
    private String resultImageUrl; // Final try-on result

    @Column("processing_status")
    private ProcessingStatus processingStatus;

    @Column("processing_time_ms")
    private Integer processingTimeMs;

    @Column("quality_score")
    private BigDecimal qualityScore; // AI confidence score 0-1

    @Column("is_saved")
    private Boolean isSaved = false;

    @Column("is_public")
    private Boolean isPublic = false;

    @Column("metadata")
    private String metadata; // Additional processing info as JSON

    @Column("created_at")
    private LocalDateTime createdAt;

    @Column("updated_at")
    private LocalDateTime updatedAt;

    // Constructors
    public TryOnSession() {}

    public TryOnSession(Long userId, Long avatarId, Long garmentId) {
        this.userId = userId;
        this.avatarId = avatarId;
        this.garmentId = garmentId;
        this.processingStatus = ProcessingStatus.PENDING;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public TryOnSession(Long userId, Long avatarId, Long garmentId, String sessionName) {
        this(userId, avatarId, garmentId);
        this.sessionName = sessionName;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
        this.updatedAt = LocalDateTime.now();
    }

    public Long getAvatarId() {
        return avatarId;
    }

    public void setAvatarId(Long avatarId) {
        this.avatarId = avatarId;
        this.updatedAt = LocalDateTime.now();
    }

    public Long getGarmentId() {
        return garmentId;
    }

    public void setGarmentId(Long garmentId) {
        this.garmentId = garmentId;
        this.updatedAt = LocalDateTime.now();
    }

    public String getSessionName() {
        return sessionName;
    }

    public void setSessionName(String sessionName) {
        this.sessionName = sessionName;
        this.updatedAt = LocalDateTime.now();
    }

    public String getResultImageUrl() {
        return resultImageUrl;
    }

    public void setResultImageUrl(String resultImageUrl) {
        this.resultImageUrl = resultImageUrl;
        this.updatedAt = LocalDateTime.now();
    }

    public ProcessingStatus getProcessingStatus() {
        return processingStatus;
    }

    public void setProcessingStatus(ProcessingStatus processingStatus) {
        this.processingStatus = processingStatus;
        this.updatedAt = LocalDateTime.now();
    }

    public Integer getProcessingTimeMs() {
        return processingTimeMs;
    }

    public void setProcessingTimeMs(Integer processingTimeMs) {
        this.processingTimeMs = processingTimeMs;
        this.updatedAt = LocalDateTime.now();
    }

    public BigDecimal getQualityScore() {
        return qualityScore;
    }

    public void setQualityScore(BigDecimal qualityScore) {
        this.qualityScore = qualityScore;
        this.updatedAt = LocalDateTime.now();
    }

    public Boolean getIsSaved() {
        return isSaved;
    }

    public void setIsSaved(Boolean isSaved) {
        this.isSaved = isSaved;
        this.updatedAt = LocalDateTime.now();
    }

    public Boolean getIsPublic() {
        return isPublic;
    }

    public void setIsPublic(Boolean isPublic) {
        this.isPublic = isPublic;
        this.updatedAt = LocalDateTime.now();
    }

    public String getMetadata() {
        return metadata;
    }

    public void setMetadata(String metadata) {
        this.metadata = metadata;
        this.updatedAt = LocalDateTime.now();
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    // Business Logic Methods
    public boolean isCompleted() {
        return processingStatus == ProcessingStatus.COMPLETED;
    }

    public boolean isProcessing() {
        return processingStatus == ProcessingStatus.PROCESSING;
    }

    public boolean hasFailed() {
        return processingStatus == ProcessingStatus.FAILED;
    }

    public boolean isPending() {
        return processingStatus == ProcessingStatus.PENDING;
    }

    public boolean hasResult() {
        return resultImageUrl != null && !resultImageUrl.trim().isEmpty();
    }

    public boolean isHighQuality() {
        return qualityScore != null && qualityScore.compareTo(new BigDecimal("0.8")) >= 0;
    }

    public boolean isLowQuality() {
        return qualityScore != null && qualityScore.compareTo(new BigDecimal("0.5")) < 0;
    }

    public void markAsCompleted(String resultImageUrl, Integer processingTimeMs, BigDecimal qualityScore) {
        this.processingStatus = ProcessingStatus.COMPLETED;
        this.resultImageUrl = resultImageUrl;
        this.processingTimeMs = processingTimeMs;
        this.qualityScore = qualityScore;
        this.updatedAt = LocalDateTime.now();
    }

    public void markAsFailed(String errorMessage) {
        this.processingStatus = ProcessingStatus.FAILED;
        this.metadata = errorMessage;
        this.updatedAt = LocalDateTime.now();
    }

    public void startProcessing() {
        this.processingStatus = ProcessingStatus.PROCESSING;
        this.updatedAt = LocalDateTime.now();
    }

    // Validation Methods
    public boolean isValid() {
        return userId != null &&
               avatarId != null &&
               garmentId != null &&
               processingStatus != null;
    }

    @Override
    public String toString() {
        return "TryOnSession{" +
                "id=" + id +
                ", userId=" + userId +
                ", avatarId=" + avatarId +
                ", garmentId=" + garmentId +
                ", sessionName='" + sessionName + '\'' +
                ", processingStatus=" + processingStatus +
                ", qualityScore=" + qualityScore +
                ", isSaved=" + isSaved +
                ", isPublic=" + isPublic +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TryOnSession that = (TryOnSession) o;
        return id != null && id.equals(that.id);
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
} 