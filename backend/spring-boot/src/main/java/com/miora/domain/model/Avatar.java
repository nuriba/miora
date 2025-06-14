package com.miora.domain.model;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Avatar entity representing 3D digital twins of users
 * 
 * Covers requirements:
 * - AVR-01: Auto-generate avatar from selfie/scan
 * - AVR-03: Manual entry of measurements
 * - AVR-10: Manage multiple avatars
 * - UPR-04: Import measurements from avatar builder
 */
@Table("avatars")
public class Avatar {
    
    @Id
    private Long id;
    
    @NotNull(message = "User ID is required")
    @Column("user_id")
    private Long userId;
    
    @NotBlank(message = "Avatar name is required")
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    // Physical measurements (in centimeters)
    @Positive(message = "Height must be positive")
    @Column("height_cm")
    private Double heightCm;
    
    @Positive(message = "Weight must be positive")
    @Column("weight_kg")
    private Double weightKg;
    
    @Column("chest_cm")
    private Double chestCm;
    
    @Column("waist_cm")
    private Double waistCm;
    
    @Column("hip_cm")
    private Double hipCm;
    
    // Limb measurements
    @Column("shoulder_width_cm")
    private Double shoulderWidthCm;
    
    @Column("arm_length_cm")
    private Double armLengthCm;
    
    @Column("leg_length_cm")
    private Double legLengthCm;
    
    @Column("neck_cm")
    private Double neckCm;
    
    // Avatar generation metadata
    @Column("generation_method")
    private AvatarGenerationMethod generationMethod;
    
    @Column("source_image_url")
    private String sourceImageUrl; // URL to original source image/scan
    
    @Column("mesh_file_url")
    private String meshFileUrl; // URL to 3D mesh file
    
    @Column("texture_file_url")
    private String textureFileUrl; // URL to texture/material file
    
    @Column("is_active")
    private Boolean isActive = true;
    
    @Column("processing_status")
    private ProcessingStatus processingStatus = ProcessingStatus.PENDING;
    
    @Column("processing_error_message")
    private String processingErrorMessage;
    
    // Pose and appearance settings
    @Column("default_pose")
    private String defaultPose = "standing";
    
    @Column("skin_tone")
    private String skinTone;
    
    @Column("hair_color")
    private String hairColor;
    
    @Column("eye_color")
    private String eyeColor;
    
    // Privacy and sharing
    @Column("is_public")
    private Boolean isPublic = false;
    
    @CreatedDate
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors
    public Avatar() {}
    
    public Avatar(Long userId, String name, AvatarGenerationMethod generationMethod) {
        this.userId = userId;
        this.name = name;
        this.generationMethod = generationMethod;
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
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public Double getHeightCm() {
        return heightCm;
    }
    
    public void setHeightCm(Double heightCm) {
        this.heightCm = heightCm;
    }
    
    public Double getWeightKg() {
        return weightKg;
    }
    
    public void setWeightKg(Double weightKg) {
        this.weightKg = weightKg;
    }
    
    public Double getChestCm() {
        return chestCm;
    }
    
    public void setChestCm(Double chestCm) {
        this.chestCm = chestCm;
    }
    
    public Double getWaistCm() {
        return waistCm;
    }
    
    public void setWaistCm(Double waistCm) {
        this.waistCm = waistCm;
    }
    
    public Double getHipCm() {
        return hipCm;
    }
    
    public void setHipCm(Double hipCm) {
        this.hipCm = hipCm;
    }
    
    public Double getShoulderWidthCm() {
        return shoulderWidthCm;
    }
    
    public void setShoulderWidthCm(Double shoulderWidthCm) {
        this.shoulderWidthCm = shoulderWidthCm;
    }
    
    public Double getArmLengthCm() {
        return armLengthCm;
    }
    
    public void setArmLengthCm(Double armLengthCm) {
        this.armLengthCm = armLengthCm;
    }
    
    public Double getLegLengthCm() {
        return legLengthCm;
    }
    
    public void setLegLengthCm(Double legLengthCm) {
        this.legLengthCm = legLengthCm;
    }
    
    public Double getNeckCm() {
        return neckCm;
    }
    
    public void setNeckCm(Double neckCm) {
        this.neckCm = neckCm;
    }
    
    public AvatarGenerationMethod getGenerationMethod() {
        return generationMethod;
    }
    
    public void setGenerationMethod(AvatarGenerationMethod generationMethod) {
        this.generationMethod = generationMethod;
    }
    
    public String getSourceImageUrl() {
        return sourceImageUrl;
    }
    
    public void setSourceImageUrl(String sourceImageUrl) {
        this.sourceImageUrl = sourceImageUrl;
    }
    
    public String getMeshFileUrl() {
        return meshFileUrl;
    }
    
    public void setMeshFileUrl(String meshFileUrl) {
        this.meshFileUrl = meshFileUrl;
    }
    
    public String getTextureFileUrl() {
        return textureFileUrl;
    }
    
    public void setTextureFileUrl(String textureFileUrl) {
        this.textureFileUrl = textureFileUrl;
    }
    
    public Boolean getIsActive() {
        return isActive;
    }
    
    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }
    
    public ProcessingStatus getProcessingStatus() {
        return processingStatus;
    }
    
    public void setProcessingStatus(ProcessingStatus processingStatus) {
        this.processingStatus = processingStatus;
    }
    
    public String getProcessingErrorMessage() {
        return processingErrorMessage;
    }
    
    public void setProcessingErrorMessage(String processingErrorMessage) {
        this.processingErrorMessage = processingErrorMessage;
    }
    
    public String getDefaultPose() {
        return defaultPose;
    }
    
    public void setDefaultPose(String defaultPose) {
        this.defaultPose = defaultPose;
    }
    
    public String getSkinTone() {
        return skinTone;
    }
    
    public void setSkinTone(String skinTone) {
        this.skinTone = skinTone;
    }
    
    public String getHairColor() {
        return hairColor;
    }
    
    public void setHairColor(String hairColor) {
        this.hairColor = hairColor;
    }
    
    public String getEyeColor() {
        return eyeColor;
    }
    
    public void setEyeColor(String eyeColor) {
        this.eyeColor = eyeColor;
    }
    
    public Boolean getIsPublic() {
        return isPublic;
    }
    
    public void setIsPublic(Boolean isPublic) {
        this.isPublic = isPublic;
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
    
    // Business logic methods
    public boolean isProcessingComplete() {
        return processingStatus == ProcessingStatus.COMPLETED;
    }
    
    public boolean hasFailedProcessing() {
        return processingStatus == ProcessingStatus.FAILED;
    }
    
    public boolean isReadyForTryOn() {
        return isProcessingComplete() && meshFileUrl != null;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Avatar avatar = (Avatar) o;
        return Objects.equals(id, avatar.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
    
    @Override
    public String toString() {
        return "Avatar{" +
                "id=" + id +
                ", userId=" + userId +
                ", name='" + name + '\'' +
                ", processingStatus=" + processingStatus +
                ", isActive=" + isActive +
                '}';
    }
} 