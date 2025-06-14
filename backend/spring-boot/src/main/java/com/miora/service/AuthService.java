package com.miora.service;

import com.miora.domain.model.User;
import com.miora.repository.UserRepository;
import com.miora.security.JwtUtil;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final EmailService emailService;
    
    @Value("${spring.profiles.active:}")
    private String activeProfile;

    public AuthService(UserRepository userRepository, 
                      PasswordEncoder passwordEncoder,
                      JwtUtil jwtUtil,
                      EmailService emailService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
        this.emailService = emailService;
    }

    public Mono<AuthResponse> register(RegisterRequest request) {
        return userRepository.existsByEmail(request.getEmail())
                .flatMap(exists -> {
                    if (exists) {
                        return Mono.error(new RuntimeException("Email already registered"));
                    }
                    
                    User user = new User();
                    user.setEmail(request.getEmail());
                    user.setDisplayName(request.getFirstName() + " " + request.getLastName());
                    user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
                    // Auto-verify emails in test profile
                    user.setIsEmailVerified(isTestProfile());
                    user.setEmailVerificationToken(isTestProfile() ? null : java.util.UUID.randomUUID().toString());
                    user.setCreatedAt(LocalDateTime.now());
                    user.setUpdatedAt(LocalDateTime.now());
                    
                    return userRepository.save(user)
                            .flatMap(savedUser -> {
                                // Send verification email
                                return emailService.sendVerificationEmail(savedUser.getEmail(), savedUser.getEmailVerificationToken())
                                        .then(Mono.just(new AuthResponse("Registration successful. Please verify your email.", null, null)));
                            });
                });
    }

    public Mono<AuthResponse> login(LoginRequest request) {
        return userRepository.findByEmail(request.getEmail())
                .switchIfEmpty(Mono.error(new RuntimeException("Invalid credentials")))
                .flatMap(user -> {
                    if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
                        return Mono.error(new RuntimeException("Invalid credentials"));
                    }
                    
                    if (!user.getIsEmailVerified()) {
                        return Mono.error(new RuntimeException("Please verify your email first"));
                    }
                    
                    if (user.getLockedUntil() != null && user.getLockedUntil().isAfter(LocalDateTime.now())) {
                        return Mono.error(new RuntimeException("Account is temporarily locked"));
                    }
                    
                    // Reset failed login attempts on successful login
                    return Mono.just(user)
                            .then(Mono.fromCallable(() -> {
                                String accessToken = jwtUtil.generateAccessToken(
                                    user.getId().toString(), 
                                    user.getEmail(), 
                                    "USER"
                                );
                                String refreshToken = jwtUtil.generateRefreshToken(user.getId().toString());
                                
                                return new AuthResponse("Login successful", accessToken, refreshToken);
                            }));
                });
    }

    public Mono<AuthResponse> refreshToken(String refreshToken) {
        return Mono.fromCallable(() -> {
            if (!jwtUtil.isRefreshToken(refreshToken) || jwtUtil.isTokenExpired(refreshToken)) {
                throw new RuntimeException("Invalid refresh token");
            }
            
            String userId = jwtUtil.getUserIdFromToken(refreshToken);
            return userId;
        })
        .flatMap(userId -> userRepository.findById(Long.parseLong(userId)))
        .switchIfEmpty(Mono.error(new RuntimeException("User not found")))
        .map(user -> {
            String newAccessToken = jwtUtil.generateAccessToken(
                user.getId().toString(), 
                user.getEmail(), 
                "USER"
            );
            String newRefreshToken = jwtUtil.generateRefreshToken(user.getId().toString());
            
            return new AuthResponse("Token refreshed", newAccessToken, newRefreshToken);
        });
    }

    public Mono<String> verifyEmail(String token) {
        return userRepository.findByEmailVerificationToken(token)
                .switchIfEmpty(Mono.error(new RuntimeException("Invalid verification token")))
                .flatMap(user -> {
                    user.setIsEmailVerified(true);
                    user.setEmailVerificationToken(null);
                    user.setUpdatedAt(LocalDateTime.now());
                    
                    return userRepository.save(user)
                            .then(Mono.just("Email verified successfully"));
                });
    }
    
    private boolean isTestProfile() {
        return "test".equals(activeProfile);
    }

    // DTOs
    public static class RegisterRequest {
        private String email;
        private String password;
        private String firstName;
        private String lastName;

        // Getters and setters
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
        public String getFirstName() { return firstName; }
        public void setFirstName(String firstName) { this.firstName = firstName; }
        public String getLastName() { return lastName; }
        public void setLastName(String lastName) { this.lastName = lastName; }
    }

    public static class LoginRequest {
        private String email;
        private String password;

        // Getters and setters
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    public static class AuthResponse {
        private String message;
        private String accessToken;
        private String refreshToken;

        public AuthResponse(String message, String accessToken, String refreshToken) {
            this.message = message;
            this.accessToken = accessToken;
            this.refreshToken = refreshToken;
        }

        // Getters and setters
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public String getAccessToken() { return accessToken; }
        public void setAccessToken(String accessToken) { this.accessToken = accessToken; }
        public String getRefreshToken() { return refreshToken; }
        public void setRefreshToken(String refreshToken) { this.refreshToken = refreshToken; }
    }
} 