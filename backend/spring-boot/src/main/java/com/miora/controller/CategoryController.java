package com.miora.controller;

import com.miora.domain.model.GarmentCategory;
import com.miora.repository.GarmentCategoryRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

/**
 * REST Controller for garment category browsing APIs
 */
@RestController
@RequestMapping("/api/v1/categories")
@CrossOrigin(origins = "*")
public class CategoryController {

    private final GarmentCategoryRepository categoryRepository;

    public CategoryController(GarmentCategoryRepository categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    // Get all active categories
    @GetMapping
    public Flux<CategoryResponse> getAllCategories() {
        return categoryRepository.findByIsActiveTrueOrderBySortOrderAsc()
                .map(this::mapToResponse);
    }

    // Get top-level categories
    @GetMapping("/top-level")
    public Flux<CategoryResponse> getTopLevelCategories() {
        return categoryRepository.findTopLevelCategories()
                .map(this::mapToResponse);
    }

    // Get category by ID
    @GetMapping("/{id}")
    public Mono<ResponseEntity<CategoryResponse>> getCategoryById(@PathVariable Long id) {
        return categoryRepository.findById(id)
                .map(category -> ResponseEntity.ok(mapToResponse(category)))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    // Get category by slug
    @GetMapping("/slug/{slug}")
    public Mono<ResponseEntity<CategoryResponse>> getCategoryBySlug(@PathVariable String slug) {
        return categoryRepository.findBySlug(slug)
                .map(category -> ResponseEntity.ok(mapToResponse(category)))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    // Get subcategories
    @GetMapping("/{id}/subcategories")
    public Flux<CategoryResponse> getSubcategories(@PathVariable Long id) {
        return categoryRepository.findByParentIdAndIsActiveTrueOrderBySortOrderAsc(id)
                .map(this::mapToResponse);
    }

    // Get category hierarchy
    @GetMapping("/{id}/hierarchy")
    public Flux<CategoryResponse> getCategoryHierarchy(@PathVariable Long id) {
        return categoryRepository.findCategoryHierarchy(id)
                .map(this::mapToResponse);
    }

    // Get categories with garment count
    @GetMapping("/with-counts")
    public Flux<CategoryResponse> getCategoriesWithCounts() {
        return categoryRepository.findCategoriesWithGarmentCount()
                .map(this::mapToResponse);
    }

    // Search categories by name
    @GetMapping("/search")
    public Flux<CategoryResponse> searchCategories(@RequestParam String q) {
        return categoryRepository.findByNameContainingIgnoreCase(q)
                .map(this::mapToResponse);
    }

    // Count subcategories
    @GetMapping("/{id}/subcategories/count")
    public Mono<ResponseEntity<SubcategoryCountResponse>> countSubcategories(@PathVariable Long id) {
        return categoryRepository.countByParentId(id)
                .map(count -> ResponseEntity.ok(new SubcategoryCountResponse(id, count)))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    // Helper methods
    private CategoryResponse mapToResponse(GarmentCategory category) {
        return new CategoryResponse(
            category.getId(),
            category.getName(),
            category.getSlug(),
            category.getDescription(),
            category.getParentId(),
            category.getIconUrl(),
            category.getSortOrder(),
            category.getIsActive(),
            category.isTopLevel(),
            category.isSubCategory(),
            category.getCreatedAt(),
            category.getUpdatedAt()
        );
    }

    // DTOs
    public static class CategoryResponse {
        private Long id;
        private String name;
        private String slug;
        private String description;
        private Long parentId;
        private String iconUrl;
        private Integer sortOrder;
        private Boolean isActive;
        private Boolean isTopLevel;
        private Boolean isSubCategory;
        private LocalDateTime createdAt;
        private LocalDateTime updatedAt;

        public CategoryResponse(Long id, String name, String slug, String description,
                              Long parentId, String iconUrl, Integer sortOrder, Boolean isActive,
                              Boolean isTopLevel, Boolean isSubCategory,
                              LocalDateTime createdAt, LocalDateTime updatedAt) {
            this.id = id;
            this.name = name;
            this.slug = slug;
            this.description = description;
            this.parentId = parentId;
            this.iconUrl = iconUrl;
            this.sortOrder = sortOrder;
            this.isActive = isActive;
            this.isTopLevel = isTopLevel;
            this.isSubCategory = isSubCategory;
            this.createdAt = createdAt;
            this.updatedAt = updatedAt;
        }

        // Getters
        public Long getId() { return id; }
        public String getName() { return name; }
        public String getSlug() { return slug; }
        public String getDescription() { return description; }
        public Long getParentId() { return parentId; }
        public String getIconUrl() { return iconUrl; }
        public Integer getSortOrder() { return sortOrder; }
        public Boolean getIsActive() { return isActive; }
        public Boolean getIsTopLevel() { return isTopLevel; }
        public Boolean getIsSubCategory() { return isSubCategory; }
        public LocalDateTime getCreatedAt() { return createdAt; }
        public LocalDateTime getUpdatedAt() { return updatedAt; }
    }

    public static class SubcategoryCountResponse {
        private Long categoryId;
        private Long subcategoryCount;

        public SubcategoryCountResponse(Long categoryId, Long subcategoryCount) {
            this.categoryId = categoryId;
            this.subcategoryCount = subcategoryCount;
        }

        // Getters
        public Long getCategoryId() { return categoryId; }
        public Long getSubcategoryCount() { return subcategoryCount; }
    }
} 