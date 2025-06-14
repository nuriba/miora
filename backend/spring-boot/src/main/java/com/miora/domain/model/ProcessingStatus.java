package com.miora.domain.model;

/**
 * Processing status for avatars and garments
 * 
 * Tracks the lifecycle of ML/CV processing operations
 */
public enum ProcessingStatus {
    /**
     * Processing has been queued but not started
     */
    PENDING,
    
    /**
     * Currently being processed by ML service
     */
    PROCESSING,
    
    /**
     * Processing completed successfully
     */
    COMPLETED,
    
    /**
     * Processing failed with errors
     */
    FAILED,
    
    /**
     * Processing was cancelled by user or system
     */
    CANCELLED
} 