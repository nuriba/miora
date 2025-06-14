package com.miora.service;

import com.miora.domain.model.Garment;
import com.miora.domain.model.ProcessingStatus;
import com.miora.repository.GarmentRepository;
import com.miora.repository.GarmentCategoryRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Service class for garment-related business logic
 */
@Service
public class GarmentService {

    private final GarmentRepository garmentRepository;
    private final GarmentCategoryRepository categoryRepository;
    private final FileUploadService fileUploadService;
    
    @Value("${miora.business.max-garments-per-user:100}")
    private int maxGarmentsPerUser;

    public GarmentService(GarmentRepository garmentRepository, 
                         GarmentCategoryRepository categoryRepository,
                         FileUploadService fileUploadService) {
        this.garmentRepository = garmentRepository;
        this.categoryRepository = categoryRepository;
        this.fileUploadService = fileUploadService;
    }

    // Create new garment
    public Mono<Garment> createGarment(Long userId, CreateGarmentRequest request) {
        return validateUserCanCreateGarment(userId)
                .then(categoryRepository.findById(request.getCategoryId()))
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Category not found")))
                .then(fileUploadService.uploadGarmentImage(request.getImageFile()))
                .flatMap(imageUrl -> {
                    Garment garment = new Garment();
                    garment.setUserId(userId);
                    garment.setCategoryId(request.getCategoryId());
                    garment.setName(request.getName());
                    garment.setDescription(request.getDescription());
                    garment.setBrand(request.getBrand());
                    garment.setPrice(request.getPrice());
                    garment.setCurrency(request.getCurrency());
                    garment.setColor(request.getColor());
                    garment.setMaterial(request.getMaterial());
                    garment.setCareInstructions(request.getCareInstructions());
                    garment.setSizeInfo(request.getSizeInfo());
                    garment.setGarmentImageUrl(imageUrl);
                    garment.setProcessingStatus(ProcessingStatus.PENDING);
                    garment.setIsPublic(request.getIsPublic());
                    garment.setExternalUrl(request.getExternalUrl());
                    garment.setCreatedAt(LocalDateTime.now());
                    garment.setUpdatedAt(LocalDateTime.now());
                    
                    return garmentRepository.save(garment);
                });
    }

    // Get garment by ID
    public Mono<Garment> getGarment(Long garmentId) {
        return garmentRepository.findById(garmentId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Garment not found")))
                .doOnNext(garment -> garmentRepository.incrementViewCount(garmentId).subscribe());
    }

    // Get user's garments
    public Flux<Garment> getUserGarments(Long userId) {
        return garmentRepository.findByUserIdOrderByCreatedAtDesc(userId);
    }

    // Get user's public garments
    public Flux<Garment> getUserPublicGarments(Long userId) {
        return garmentRepository.findByUserIdAndIsPublicTrueOrderByCreatedAtDesc(userId);
    }

    // Get garments by category
    public Flux<Garment> getGarmentsByCategory(Long categoryId, int page, int size) {
        return garmentRepository.findByCategoryIdAndIsPublicTrueOrderByCreatedAtDesc(categoryId)
                .skip((long) page * size)
                .take(size);
    }

    // Get public garments for discovery
    public Flux<Garment> getPublicGarments(int page, int size) {
        return garmentRepository.findPublicGarments(size, page * size);
    }

    // Get featured garments
    public Flux<Garment> getFeaturedGarments(int limit) {
        return garmentRepository.findFeaturedGarments(limit);
    }

    // Get popular garments
    public Flux<Garment> getPopularGarments(int page, int size) {
        return garmentRepository.findPopularGarments(size, page * size);
    }

    // Get trending garments
    public Flux<Garment> getTrendingGarments(int page, int size) {
        return garmentRepository.findTrendingGarments(size, page * size);
    }

    // Search garments
    public Flux<Garment> searchGarments(String query, int page, int size) {
        return garmentRepository.searchGarments(query, size, page * size);
    }

    // Get similar garments
    public Flux<Garment> getSimilarGarments(Long garmentId, int limit) {
        return garmentRepository.findById(garmentId)
                .flatMapMany(garment -> 
                    garmentRepository.findSimilarGarments(
                        garmentId, 
                        garment.getCategoryId(), 
                        garment.getColor(), 
                        limit
                    )
                );
    }

    // Update garment
    public Mono<Garment> updateGarment(Long userId, Long garmentId, UpdateGarmentRequest request) {
        return garmentRepository.findById(garmentId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Garment not found")))
                .filter(garment -> garment.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to update this garment")))
                .flatMap(garment -> {
                    // Update fields
                    if (request.getName() != null) garment.setName(request.getName());
                    if (request.getDescription() != null) garment.setDescription(request.getDescription());
                    if (request.getBrand() != null) garment.setBrand(request.getBrand());
                    if (request.getPrice() != null) garment.setPrice(request.getPrice());
                    if (request.getColor() != null) garment.setColor(request.getColor());
                    if (request.getMaterial() != null) garment.setMaterial(request.getMaterial());
                    if (request.getCareInstructions() != null) garment.setCareInstructions(request.getCareInstructions());
                    if (request.getIsPublic() != null) garment.setIsPublic(request.getIsPublic());
                    if (request.getExternalUrl() != null) garment.setExternalUrl(request.getExternalUrl());
                    
                    garment.setUpdatedAt(LocalDateTime.now());
                    return garmentRepository.save(garment);
                });
    }

    // Delete garment
    public Mono<Void> deleteGarment(Long userId, Long garmentId) {
        return garmentRepository.findById(garmentId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Garment not found")))
                .filter(garment -> garment.getUserId().equals(userId))
                .switchIfEmpty(Mono.error(new SecurityException("Not authorized to delete this garment")))
                .flatMap(garment -> 
                    fileUploadService.deleteFile(garment.getGarmentImageUrl())
                        .then(garmentRepository.delete(garment))
                );
    }

    // Process garment for ML readiness
    public Mono<Void> processGarment(Long garmentId) {
        return garmentRepository.findById(garmentId)
                .switchIfEmpty(Mono.error(new IllegalArgumentException("Garment not found")))
                .filter(garment -> garment.getProcessingStatus() == ProcessingStatus.PENDING)
                .switchIfEmpty(Mono.error(new IllegalStateException("Garment is not in pending status")))
                .flatMap(garment -> {
                    // Update status to processing
                    garment.setProcessingStatus(ProcessingStatus.PROCESSING);
                    return garmentRepository.save(garment);
                })
                .flatMap(garment -> 
                    // Call ML service to process garment
                    processGarmentWithML(garment)
                )
                .then();
    }

    // Validate user can create more garments
    private Mono<Void> validateUserCanCreateGarment(Long userId) {
        return garmentRepository.countByUserId(userId)
                .flatMap(count -> {
                    if (count >= maxGarmentsPerUser) {
                        return Mono.error(new IllegalStateException(
                            "Maximum number of garments reached (" + maxGarmentsPerUser + ")"));
                    }
                    return Mono.empty();
                });
    }

    // Process garment with ML service
    private Mono<Garment> processGarmentWithML(Garment garment) {
        // This would integrate with the ML service
        // For now, simulate processing
        return Mono.fromCallable(() -> {
            // Simulate processing time
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            // Generate mock processed data URL
            String processedDataUrl = "processed/" + UUID.randomUUID().toString() + ".json";
            
            garment.setGarmentDataUrl(processedDataUrl);
            garment.setProcessingStatus(ProcessingStatus.COMPLETED);
            garment.setUpdatedAt(LocalDateTime.now());
            
            return garment;
        })
        .flatMap(garmentRepository::save);
    }

    // DTOs
    public static class CreateGarmentRequest {
        private String name;
        private String description;
        private String brand;
        private java.math.BigDecimal price;
        private String currency = "USD";
        private String color;
        private String material;
        private String careInstructions;
        private String sizeInfo;
        private Long categoryId;
        private Boolean isPublic = false;
        private String externalUrl;
        private MultipartFile imageFile;

        // Getters and setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public String getBrand() { return brand; }
        public void setBrand(String brand) { this.brand = brand; }
        public java.math.BigDecimal getPrice() { return price; }
        public void setPrice(java.math.BigDecimal price) { this.price = price; }
        public String getCurrency() { return currency; }
        public void setCurrency(String currency) { this.currency = currency; }
        public String getColor() { return color; }
        public void setColor(String color) { this.color = color; }
        public String getMaterial() { return material; }
        public void setMaterial(String material) { this.material = material; }
        public String getCareInstructions() { return careInstructions; }
        public void setCareInstructions(String careInstructions) { this.careInstructions = careInstructions; }
        public String getSizeInfo() { return sizeInfo; }
        public void setSizeInfo(String sizeInfo) { this.sizeInfo = sizeInfo; }
        public Long getCategoryId() { return categoryId; }
        public void setCategoryId(Long categoryId) { this.categoryId = categoryId; }
        public Boolean getIsPublic() { return isPublic; }
        public void setIsPublic(Boolean isPublic) { this.isPublic = isPublic; }
        public String getExternalUrl() { return externalUrl; }
        public void setExternalUrl(String externalUrl) { this.externalUrl = externalUrl; }
        public MultipartFile getImageFile() { return imageFile; }
        public void setImageFile(MultipartFile imageFile) { this.imageFile = imageFile; }
    }

    public static class UpdateGarmentRequest {
        private String name;
        private String description;
        private String brand;
        private java.math.BigDecimal price;
        private String color;
        private String material;
        private String careInstructions;
        private Boolean isPublic;
        private String externalUrl;

        // Getters and setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public String getBrand() { return brand; }
        public void setBrand(String brand) { this.brand = brand; }
        public java.math.BigDecimal getPrice() { return price; }
        public void setPrice(java.math.BigDecimal price) { this.price = price; }
        public String getColor() { return color; }
        public void setColor(String color) { this.color = color; }
        public String getMaterial() { return material; }
        public void setMaterial(String material) { this.material = material; }
        public String getCareInstructions() { return careInstructions; }
        public void setCareInstructions(String careInstructions) { this.careInstructions = careInstructions; }
        public Boolean getIsPublic() { return isPublic; }
        public void setIsPublic(Boolean isPublic) { this.isPublic = isPublic; }
        public String getExternalUrl() { return externalUrl; }
        public void setExternalUrl(String externalUrl) { this.externalUrl = externalUrl; }
    }
} 