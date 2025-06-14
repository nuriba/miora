package com.miora.domain.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Represents a garment (clothing item) in the Miora platform.
 * Can be user-uploaded or system/brand garments.
 */
@Table("garments")
public class Garment {

    @Id
    private Long id;

    @Column("user_id")
    private Long userId; // NULL for system/brand garments

    @Column("category_id")
    private Long categoryId;

    @Column("name")
    private String name;

    @Column("description")
    private String description;

    @Column("brand")
    private String brand;

    @Column("price")
    private BigDecimal price;

    @Column("currency")
    private String currency = "USD";

    @Column("garment_image_url")
    private String garmentImageUrl;

    @Column("garment_data_url")
    private String garmentDataUrl; // 3D model or processed image data

    @Column("color")
    private String color;

    @Column("size_info")
    private String sizeInfo; // JSON stored as string

    @Column("material")
    private String material;

    @Column("care_instructions")
    private String careInstructions;

    @Column("processing_status")
    private ProcessingStatus processingStatus;

    @Column("is_public")
    private Boolean isPublic = false;

    @Column("is_featured")
    private Boolean isFeatured = false;

    @Column("view_count")
    private Integer viewCount = 0;

    @Column("like_count")
    private Integer likeCount = 0;

    @Column("try_on_count")
    private Integer tryOnCount = 0;

    @Column("external_url")
    private String externalUrl; // Link to purchase

    @Column("created_at")
    private LocalDateTime createdAt;

    @Column("updated_at")
    private LocalDateTime updatedAt;

    // Constructors
    public Garment() {}

    public Garment(String name, Long categoryId, String garmentImageUrl) {
        this.name = name;
        this.categoryId = categoryId;
        this.garmentImageUrl = garmentImageUrl;
        this.processingStatus = ProcessingStatus.PENDING;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
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

    public Long getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Long categoryId) {
        this.categoryId = categoryId;
        this.updatedAt = LocalDateTime.now();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
        this.updatedAt = LocalDateTime.now();
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
        this.updatedAt = LocalDateTime.now();
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
        this.updatedAt = LocalDateTime.now();
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
        this.updatedAt = LocalDateTime.now();
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
        this.updatedAt = LocalDateTime.now();
    }

    public String getGarmentImageUrl() {
        return garmentImageUrl;
    }

    public void setGarmentImageUrl(String garmentImageUrl) {
        this.garmentImageUrl = garmentImageUrl;
        this.updatedAt = LocalDateTime.now();
    }

    public String getGarmentDataUrl() {
        return garmentDataUrl;
    }

    public void setGarmentDataUrl(String garmentDataUrl) {
        this.garmentDataUrl = garmentDataUrl;
        this.updatedAt = LocalDateTime.now();
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
        this.updatedAt = LocalDateTime.now();
    }

    public String getSizeInfo() {
        return sizeInfo;
    }

    public void setSizeInfo(String sizeInfo) {
        this.sizeInfo = sizeInfo;
        this.updatedAt = LocalDateTime.now();
    }

    public String getMaterial() {
        return material;
    }

    public void setMaterial(String material) {
        this.material = material;
        this.updatedAt = LocalDateTime.now();
    }

    public String getCareInstructions() {
        return careInstructions;
    }

    public void setCareInstructions(String careInstructions) {
        this.careInstructions = careInstructions;
        this.updatedAt = LocalDateTime.now();
    }

    public ProcessingStatus getProcessingStatus() {
        return processingStatus;
    }

    public void setProcessingStatus(ProcessingStatus processingStatus) {
        this.processingStatus = processingStatus;
        this.updatedAt = LocalDateTime.now();
    }

    public Boolean getIsPublic() {
        return isPublic;
    }

    public void setIsPublic(Boolean isPublic) {
        this.isPublic = isPublic;
        this.updatedAt = LocalDateTime.now();
    }

    public Boolean getIsFeatured() {
        return isFeatured;
    }

    public void setIsFeatured(Boolean isFeatured) {
        this.isFeatured = isFeatured;
        this.updatedAt = LocalDateTime.now();
    }

    public Integer getViewCount() {
        return viewCount;
    }

    public void setViewCount(Integer viewCount) {
        this.viewCount = viewCount;
    }

    public Integer getLikeCount() {
        return likeCount;
    }

    public void setLikeCount(Integer likeCount) {
        this.likeCount = likeCount;
    }

    public Integer getTryOnCount() {
        return tryOnCount;
    }

    public void setTryOnCount(Integer tryOnCount) {
        this.tryOnCount = tryOnCount;
    }

    public String getExternalUrl() {
        return externalUrl;
    }

    public void setExternalUrl(String externalUrl) {
        this.externalUrl = externalUrl;
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
    public boolean isUserUploaded() {
        return userId != null;
    }

    public boolean isSystemGarment() {
        return userId == null;
    }

    public boolean isProcessed() {
        return processingStatus == ProcessingStatus.COMPLETED;
    }

    public boolean isProcessing() {
        return processingStatus == ProcessingStatus.PROCESSING;
    }

    public boolean hasFailed() {
        return processingStatus == ProcessingStatus.FAILED;
    }

    public void incrementViewCount() {
        this.viewCount = (this.viewCount == null ? 0 : this.viewCount) + 1;
    }

    public void incrementLikeCount() {
        this.likeCount = (this.likeCount == null ? 0 : this.likeCount) + 1;
    }

    public void decrementLikeCount() {
        this.likeCount = Math.max(0, (this.likeCount == null ? 0 : this.likeCount) - 1);
    }

    public void incrementTryOnCount() {
        this.tryOnCount = (this.tryOnCount == null ? 0 : this.tryOnCount) + 1;
    }

    // Validation Methods
    public boolean isValid() {
        return name != null && !name.trim().isEmpty() &&
               categoryId != null &&
               garmentImageUrl != null && !garmentImageUrl.trim().isEmpty() &&
               processingStatus != null;
    }

    @Override
    public String toString() {
        return "Garment{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", brand='" + brand + '\'' +
                ", userId=" + userId +
                ", categoryId=" + categoryId +
                ", processingStatus=" + processingStatus +
                ", isPublic=" + isPublic +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Garment garment = (Garment) o;
        return id != null && id.equals(garment.id);
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
} 