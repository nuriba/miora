package com.miora.repository;

import com.miora.domain.model.GarmentCategory;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface GarmentCategoryRepository extends ReactiveCrudRepository<GarmentCategory, Long> {
    
    // Find by slug
    Mono<GarmentCategory> findBySlug(String slug);
    
    // Find all active categories
    Flux<GarmentCategory> findByIsActiveTrueOrderBySortOrderAsc();
    
    // Find all root categories (no parent)
    Flux<GarmentCategory> findByParentIdIsNullAndIsActiveTrueOrderBySortOrderAsc();
    
    // Find child categories by parent ID
    Flux<GarmentCategory> findByParentIdAndIsActiveTrueOrderBySortOrderAsc(Long parentId);
    
    // Find all subcategories of a category (including nested)
    @Query("SELECT * FROM garment_categories WHERE parent_id = :categoryId AND is_active = true ORDER BY sort_order ASC")
    Flux<GarmentCategory> findSubcategories(Long categoryId);
    
    // Search categories by name
    @Query("SELECT * FROM garment_categories WHERE LOWER(name) LIKE LOWER(CONCAT('%', :query, '%')) AND is_active = true ORDER BY sort_order ASC")
    Flux<GarmentCategory> searchByName(String query);
    
    // Find category hierarchy (simplified for H2 compatibility)
    @Query("SELECT * FROM garment_categories WHERE id = :categoryId OR parent_id = :categoryId ORDER BY parent_id NULLS FIRST, sort_order ASC")
    Flux<GarmentCategory> findCategoryHierarchy(Long categoryId);
    
    // Count categories by parent
    Mono<Long> countByParentIdAndIsActiveTrue(Long parentId);
    
    // Find categories by IDs
    @Query("SELECT * FROM garment_categories WHERE id IN (:ids) AND is_active = true ORDER BY sort_order ASC")
    Flux<GarmentCategory> findByIdInAndIsActiveTrue(Iterable<Long> ids);
    
    // Check if category exists by slug
    Mono<Boolean> existsBySlug(String slug);
    
    // Find popular categories (based on garment count)
    @Query("""
        SELECT gc.* FROM garment_categories gc 
        LEFT JOIN garments g ON gc.id = g.category_id 
        WHERE gc.is_active = true 
        GROUP BY gc.id, gc.name, gc.slug, gc.parent_id, gc.description, gc.sort_order, gc.is_active, gc.created_at, gc.updated_at 
        ORDER BY COUNT(g.id) DESC, gc.sort_order ASC 
        LIMIT :limit
        """)
    Flux<GarmentCategory> findPopularCategories(int limit);
    
    // Find top level categories (alias for root categories)
    default Flux<GarmentCategory> findTopLevelCategories() {
        return findByParentIdIsNullAndIsActiveTrueOrderBySortOrderAsc();
    }
    
    // Find categories with garment count
    @Query("""
        SELECT gc.*, COUNT(g.id) as garment_count 
        FROM garment_categories gc 
        LEFT JOIN garments g ON gc.id = g.category_id 
        WHERE gc.is_active = true 
        GROUP BY gc.id, gc.name, gc.slug, gc.parent_id, gc.description, gc.sort_order, gc.is_active, gc.created_at, gc.updated_at 
        ORDER BY gc.sort_order ASC
        """)
    Flux<GarmentCategory> findCategoriesWithGarmentCount();
    
    // Find by name containing (case insensitive)
    @Query("SELECT * FROM garment_categories WHERE LOWER(name) LIKE LOWER(CONCAT('%', :name, '%')) AND is_active = true ORDER BY sort_order ASC")
    Flux<GarmentCategory> findByNameContainingIgnoreCase(String name);
    
    // Count by parent ID
    Mono<Long> countByParentId(Long parentId);
} 