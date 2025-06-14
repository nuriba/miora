package com.miora.repository;

import com.miora.domain.model.User;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface UserRepository extends R2dbcRepository<User, Long> {
    
    Mono<User> findByEmail(String email);
    
    Mono<User> findByDisplayName(String displayName);
    
    Mono<Boolean> existsByEmail(String email);
    
    Mono<Boolean> existsByDisplayName(String displayName);
    
    @Query("SELECT * FROM users WHERE email_verification_token = :token")
    Mono<User> findByEmailVerificationToken(String token);
    
    @Query("SELECT * FROM users WHERE password_reset_token = :token")
    Mono<User> findByPasswordResetToken(String token);
    
    @Query("UPDATE users SET failed_login_attempts = failed_login_attempts + 1, last_login_at = NOW() WHERE id = :userId")
    Mono<Void> incrementFailedLoginAttempts(Long userId);
    
    @Query("UPDATE users SET failed_login_attempts = 0, locked_until = NULL WHERE id = :userId")
    Mono<Void> resetFailedLoginAttempts(Long userId);
} 