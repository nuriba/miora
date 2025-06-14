package com.miora.domain.model;

/**
 * Privacy levels for user content and profile visibility
 * 
 * Supports requirement UPR-05: Global privacy toggle
 */
public enum PrivacyLevel {
    /**
     * Content visible to everyone
     */
    PUBLIC,
    
    /**
     * Content visible only to friends/followers
     */
    FRIENDS,
    
    /**
     * Content visible only to the user
     */
    PRIVATE
} 