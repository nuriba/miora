package com.miora.domain.model;

/**
 * Methods for generating avatars
 * 
 * Supports requirement AVR-01: Auto-generate avatar from selfie or scan
 */
public enum AvatarGenerationMethod {
    /**
     * Generated from a single selfie image
     */
    SELFIE,
    
    /**
     * Generated from multiple angle photos
     */
    MULTI_ANGLE,
    
    /**
     * Generated from LiDAR scan
     */
    LIDAR_SCAN,
    
    /**
     * Manually created with measurements
     */
    MANUAL_ENTRY,
    
    /**
     * Generated from 3D scanning device
     */
    DEPTH_CAMERA
} 