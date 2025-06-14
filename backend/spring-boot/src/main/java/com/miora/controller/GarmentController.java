package com.miora.controller;

import com.miora.domain.model.Garment;
import com.miora.service.GarmentService;
import com.miora.security.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.multipart.FilePart;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import jakarta.validation.Valid;
import java.math.BigDecimal;

/**
 * REST Controller for garment management APIs
 */
@RestController
@RequestMapping("/api/v1/garments")
@CrossOrigin(origins = "*")
public class GarmentController {

    private final GarmentService garmentService;
    private final JwtUtil jwtUtil;

    public GarmentController(GarmentService garmentService, JwtUtil jwtUtil) {
        this.garmentService = garmentService;
        this.jwtUtil = jwtUtil;
    }

    // Create new garment
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<GarmentResponse>> createGarment(
            @RequestHeader("Authorization") String token,
            @RequestPart("garment") @Valid CreateGarmentRequest request,
            @RequestPart("image") MultipartFile imageFile) {
        
        Long userId = extractUserIdFromToken(token);
        
        // Set the image file in the request
        GarmentService.CreateGarmentRequest serviceRequest = mapToServiceRequest(request);
        serviceRequest.setImageFile(imageFile);
        
        return garmentService.createGarment(userId, serviceRequest)
                .map(garment -> ResponseEntity.status(HttpStatus.CREATED)
                        .body(mapToResponse(garment)))
                .onErrorResume(this::handleError);
    }

    // Get garment by ID
    @GetMapping("/{id}")
    public Mono<ResponseEntity<GarmentResponse>> getGarment(@PathVariable Long id) {
        return garmentService.getGarment(id)
                .map(garment -> ResponseEntity.ok(mapToResponse(garment)))
                .onErrorResume(this::handleError);
    }

    // Get user's garments
    @GetMapping("/my-garments")
    @PreAuthorize("hasRole('USER')")
    public Flux<GarmentResponse> getMyGarments(@RequestHeader("Authorization") String token) {
        Long userId = extractUserIdFromToken(token);
        return garmentService.getUserGarments(userId)
                .map(this::mapToResponse);
    }

    // Get user's public garments
    @GetMapping("/users/{userId}/public")
    public Flux<GarmentResponse> getUserPublicGarments(@PathVariable Long userId) {
        return garmentService.getUserPublicGarments(userId)
                .map(this::mapToResponse);
    }

    // Get garments by category
    @GetMapping("/category/{categoryId}")
    public Flux<GarmentResponse> getGarmentsByCategory(
            @PathVariable Long categoryId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return garmentService.getGarmentsByCategory(categoryId, page, size)
                .map(this::mapToResponse);
    }

    // Get public garments (discovery)
    @GetMapping("/public")
    public Flux<GarmentResponse> getPublicGarments(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return garmentService.getPublicGarments(page, size)
                .map(this::mapToResponse);
    }

    // Get featured garments
    @GetMapping("/featured")
    public Flux<GarmentResponse> getFeaturedGarments(
            @RequestParam(defaultValue = "10") int limit) {
        return garmentService.getFeaturedGarments(limit)
                .map(this::mapToResponse);
    }

    // Get popular garments
    @GetMapping("/popular")
    public Flux<GarmentResponse> getPopularGarments(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return garmentService.getPopularGarments(page, size)
                .map(this::mapToResponse);
    }

    // Get trending garments
    @GetMapping("/trending")
    public Flux<GarmentResponse> getTrendingGarments(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return garmentService.getTrendingGarments(page, size)
                .map(this::mapToResponse);
    }

    // Search garments
    @GetMapping("/search")
    public Flux<GarmentResponse> searchGarments(
            @RequestParam String q,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return garmentService.searchGarments(q, page, size)
                .map(this::mapToResponse);
    }

    // Get similar garments
    @GetMapping("/{id}/similar")
    public Flux<GarmentResponse> getSimilarGarments(
            @PathVariable Long id,
            @RequestParam(defaultValue = "10") int limit) {
        return garmentService.getSimilarGarments(id, limit)
                .map(this::mapToResponse);
    }

    // Update garment
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<GarmentResponse>> updateGarment(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id,
            @RequestBody @Valid UpdateGarmentRequest request) {
        
        Long userId = extractUserIdFromToken(token);
        GarmentService.UpdateGarmentRequest serviceRequest = mapToUpdateServiceRequest(request);
        
        return garmentService.updateGarment(userId, id, serviceRequest)
                .map(garment -> ResponseEntity.ok(mapToResponse(garment)))
                .onErrorResume(this::handleError);
    }

    // Delete garment
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<Void>> deleteGarment(
            @RequestHeader("Authorization") String token,
            @PathVariable Long id) {
        
        Long userId = extractUserIdFromToken(token);
        
        return garmentService.deleteGarment(userId, id)
                .then(Mono.just(ResponseEntity.noContent().<Void>build()))
                .onErrorResume(this::handleError);
    }

    // Process garment for ML
    @PostMapping("/{id}/process")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<Void>> processGarment(@PathVariable Long id) {
        return garmentService.processGarment(id)
                .then(Mono.just(ResponseEntity.accepted().<Void>build()))
                .onErrorResume(this::handleError);
    }

    // Helper methods
    private Long extractUserIdFromToken(String token) {
        String jwt = token.replace("Bearer ", "");
        return Long.valueOf(jwtUtil.getUserIdFromToken(jwt));
    }

    private GarmentService.CreateGarmentRequest mapToServiceRequest(CreateGarmentRequest request) {
        GarmentService.CreateGarmentRequest serviceRequest = new GarmentService.CreateGarmentRequest();
        serviceRequest.setName(request.getName());
        serviceRequest.setDescription(request.getDescription());
        serviceRequest.setBrand(request.getBrand());
        serviceRequest.setPrice(request.getPrice());
        serviceRequest.setCurrency(request.getCurrency());
        serviceRequest.setColor(request.getColor());
        serviceRequest.setMaterial(request.getMaterial());
        serviceRequest.setCareInstructions(request.getCareInstructions());
        serviceRequest.setSizeInfo(request.getSizeInfo());
        serviceRequest.setCategoryId(request.getCategoryId());
        serviceRequest.setIsPublic(request.getIsPublic());
        serviceRequest.setExternalUrl(request.getExternalUrl());
        return serviceRequest;
    }

    private GarmentService.UpdateGarmentRequest mapToUpdateServiceRequest(UpdateGarmentRequest request) {
        GarmentService.UpdateGarmentRequest serviceRequest = new GarmentService.UpdateGarmentRequest();
        serviceRequest.setName(request.getName());
        serviceRequest.setDescription(request.getDescription());
        serviceRequest.setBrand(request.getBrand());
        serviceRequest.setPrice(request.getPrice());
        serviceRequest.setColor(request.getColor());
        serviceRequest.setMaterial(request.getMaterial());
        serviceRequest.setCareInstructions(request.getCareInstructions());
        serviceRequest.setIsPublic(request.getIsPublic());
        serviceRequest.setExternalUrl(request.getExternalUrl());
        return serviceRequest;
    }

    private GarmentResponse mapToResponse(Garment garment) {
        return new GarmentResponse(
            garment.getId(),
            garment.getName(),
            garment.getDescription(),
            garment.getBrand(),
            garment.getPrice(),
            garment.getCurrency(),
            garment.getColor(),
            garment.getMaterial(),
            garment.getGarmentImageUrl(),
            garment.getCategoryId(),
            garment.getProcessingStatus().name(),
            garment.getIsPublic(),
            garment.getIsFeatured(),
            garment.getViewCount(),
            garment.getLikeCount(),
            garment.getTryOnCount(),
            garment.getExternalUrl(),
            garment.getCreatedAt(),
            garment.getUpdatedAt()
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
    public static class CreateGarmentRequest {
        private String name;
        private String description;
        private String brand;
        private BigDecimal price;
        private String currency = "USD";
        private String color;
        private String material;
        private String careInstructions;
        private String sizeInfo;
        private Long categoryId;
        private Boolean isPublic = false;
        private String externalUrl;

        // Getters and setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public String getBrand() { return brand; }
        public void setBrand(String brand) { this.brand = brand; }
        public BigDecimal getPrice() { return price; }
        public void setPrice(BigDecimal price) { this.price = price; }
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
    }

    public static class UpdateGarmentRequest {
        private String name;
        private String description;
        private String brand;
        private BigDecimal price;
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
        public BigDecimal getPrice() { return price; }
        public void setPrice(BigDecimal price) { this.price = price; }
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

    public static class GarmentResponse {
        private Long id;
        private String name;
        private String description;
        private String brand;
        private BigDecimal price;
        private String currency;
        private String color;
        private String material;
        private String imageUrl;
        private Long categoryId;
        private String processingStatus;
        private Boolean isPublic;
        private Boolean isFeatured;
        private Integer viewCount;
        private Integer likeCount;
        private Integer tryOnCount;
        private String externalUrl;
        private java.time.LocalDateTime createdAt;
        private java.time.LocalDateTime updatedAt;

        public GarmentResponse(Long id, String name, String description, String brand, 
                             BigDecimal price, String currency, String color, String material,
                             String imageUrl, Long categoryId, String processingStatus,
                             Boolean isPublic, Boolean isFeatured, Integer viewCount,
                             Integer likeCount, Integer tryOnCount, String externalUrl,
                             java.time.LocalDateTime createdAt, java.time.LocalDateTime updatedAt) {
            this.id = id;
            this.name = name;
            this.description = description;
            this.brand = brand;
            this.price = price;
            this.currency = currency;
            this.color = color;
            this.material = material;
            this.imageUrl = imageUrl;
            this.categoryId = categoryId;
            this.processingStatus = processingStatus;
            this.isPublic = isPublic;
            this.isFeatured = isFeatured;
            this.viewCount = viewCount;
            this.likeCount = likeCount;
            this.tryOnCount = tryOnCount;
            this.externalUrl = externalUrl;
            this.createdAt = createdAt;
            this.updatedAt = updatedAt;
        }

        // Getters
        public Long getId() { return id; }
        public String getName() { return name; }
        public String getDescription() { return description; }
        public String getBrand() { return brand; }
        public BigDecimal getPrice() { return price; }
        public String getCurrency() { return currency; }
        public String getColor() { return color; }
        public String getMaterial() { return material; }
        public String getImageUrl() { return imageUrl; }
        public Long getCategoryId() { return categoryId; }
        public String getProcessingStatus() { return processingStatus; }
        public Boolean getIsPublic() { return isPublic; }
        public Boolean getIsFeatured() { return isFeatured; }
        public Integer getViewCount() { return viewCount; }
        public Integer getLikeCount() { return likeCount; }
        public Integer getTryOnCount() { return tryOnCount; }
        public String getExternalUrl() { return externalUrl; }
        public java.time.LocalDateTime getCreatedAt() { return createdAt; }
        public java.time.LocalDateTime getUpdatedAt() { return updatedAt; }
    }
} 