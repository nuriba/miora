package com.miora.repository;

import com.miora.domain.model.Garment;
import com.miora.domain.model.ProcessingStatus;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;

/**
 * Repository interface for Garment entity operations
 */
@Repository
public interface GarmentRepository extends R2dbcRepository<Garment, Long> {

    // Find garments by user
    Flux<Garment> findByUserIdOrderByCreatedAtDesc(Long userId);
    
    // Find user's public garments
    Flux<Garment> findByUserIdAndIsPublicTrueOrderByCreatedAtDesc(Long userId);
    
    // Find garments by category
    Flux<Garment> findByCategoryIdAndIsPublicTrueOrderByCreatedAtDesc(Long categoryId);
    
    // Find garments by processing status
    Flux<Garment> findByProcessingStatusOrderByCreatedAtAsc(ProcessingStatus status);
    
    // Find user's garments by processing status
    Flux<Garment> findByUserIdAndProcessingStatusOrderByCreatedAtAsc(Long userId, ProcessingStatus status);
    
    // Find public garments (for discovery)
    @Query("SELECT * FROM garments WHERE is_public = true ORDER BY created_at DESC LIMIT :limit OFFSET :offset")
    Flux<Garment> findPublicGarments(int limit, int offset);
    
    // Find featured garments
    @Query("SELECT * FROM garments WHERE is_featured = true AND is_public = true ORDER BY created_at DESC LIMIT :limit")
    Flux<Garment> findFeaturedGarments(int limit);
    
    // Find popular garments (by try-on count)
    @Query("SELECT * FROM garments WHERE is_public = true ORDER BY try_on_count DESC, created_at DESC LIMIT :limit OFFSET :offset")
    Flux<Garment> findPopularGarments(int limit, int offset);
    
    // Find trending garments (high engagement recently)
    @Query("""
        SELECT * FROM garments 
        WHERE is_public = true 
        AND created_at >= DATEADD('DAY', -7, CURRENT_TIMESTAMP)
        ORDER BY (like_count + try_on_count + view_count) DESC, created_at DESC 
        LIMIT :limit OFFSET :offset
        """)
    Flux<Garment> findTrendingGarments(int limit, int offset);
    
    // Search garments by name or description
    @Query("""
        SELECT * FROM garments 
        WHERE is_public = true 
        AND (LOWER(name) LIKE LOWER(CONCAT('%', :query, '%')) 
             OR LOWER(description) LIKE LOWER(CONCAT('%', :query, '%'))
             OR LOWER(brand) LIKE LOWER(CONCAT('%', :query, '%')))
        ORDER BY created_at DESC 
        LIMIT :limit OFFSET :offset
        """)
    Flux<Garment> searchGarments(String query, int limit, int offset);
    
    // Find garments by brand
    @Query("SELECT * FROM garments WHERE LOWER(brand) = LOWER(:brand) AND is_public = true ORDER BY created_at DESC")
    Flux<Garment> findByBrandIgnoreCase(String brand);
    
    // Find garments by color
    @Query("SELECT * FROM garments WHERE LOWER(color) LIKE LOWER(CONCAT('%', :color, '%')) AND is_public = true ORDER BY created_at DESC")
    Flux<Garment> findByColorContainingIgnoreCase(String color);
    
    // Find garments in price range
    @Query("SELECT * FROM garments WHERE price BETWEEN :minPrice AND :maxPrice AND is_public = true ORDER BY price ASC")
    Flux<Garment> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
    
    // Count user's garments
    Mono<Long> countByUserId(Long userId);
    
    // Count garments by category
    Mono<Long> countByCategoryId(Long categoryId);
    
    // Count public garments
    @Query("SELECT COUNT(*) FROM garments WHERE is_public = true")
    Mono<Long> countPublicGarments();
    
    // Update view count
    @Query("UPDATE garments SET view_count = view_count + 1, updated_at = NOW() WHERE id = :id")
    Mono<Void> incrementViewCount(Long id);
    
    // Update like count
    @Query("UPDATE garments SET like_count = like_count + :increment, updated_at = NOW() WHERE id = :id")
    Mono<Void> updateLikeCount(Long id, int increment);
    
    // Update try-on count
    @Query("UPDATE garments SET try_on_count = try_on_count + 1, updated_at = NOW() WHERE id = :id")
    Mono<Void> incrementTryOnCount(Long id);
    
    // Update processing status
    @Query("UPDATE garments SET processing_status = :status, updated_at = NOW() WHERE id = :id")
    Mono<Void> updateProcessingStatus(Long id, ProcessingStatus status);
    
    // Update garment data URL after processing
    @Query("UPDATE garments SET garment_data_url = :dataUrl, processing_status = :status, updated_at = NOW() WHERE id = :id")
    Mono<Void> updateGarmentData(Long id, String dataUrl, ProcessingStatus status);
    
    // Find user's garments with category info
    @Query("""
        SELECT g.*, gc.name as category_name, gc.slug as category_slug 
        FROM garments g 
        LEFT JOIN garment_categories gc ON g.category_id = gc.id 
        WHERE g.user_id = :userId 
        ORDER BY g.created_at DESC
        """)
    Flux<Garment> findUserGarmentsWithCategory(Long userId);
    
    // Find similar garments (by category and color)
    @Query("""
        SELECT * FROM garments 
        WHERE id != :garmentId 
        AND category_id = :categoryId 
        AND is_public = true 
        AND (color = :color OR color IS NULL OR :color IS NULL)
        ORDER BY created_at DESC 
        LIMIT :limit
        """)
    Flux<Garment> findSimilarGarments(Long garmentId, Long categoryId, String color, int limit);
} 