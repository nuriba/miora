package com.miora;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.r2dbc.config.EnableR2dbcAuditing;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;

/**
 * Miora - Virtual Fashion Try-On Platform
 * Main Spring Boot Application Entry Point
 * 
 * This application handles:
 * - User authentication and authorization
 * - User profile management
 * - Social features (sharing, following, etc.)
 * - Business logic coordination
 * - Communication with ML/CV service
 */
@SpringBootApplication
@EnableR2dbcAuditing
@EnableAsync
@EnableWebFluxSecurity
public class MioraBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(MioraBackendApplication.class, args);
    }
} 