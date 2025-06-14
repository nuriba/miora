package com.miora.controller;

import com.miora.service.AuthService;
import com.miora.service.AuthService.AuthResponse;
import com.miora.service.AuthService.LoginRequest;
import com.miora.service.AuthService.RegisterRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public Mono<ResponseEntity<AuthResponse>> register(@Valid @RequestBody RegisterRequest request) {
        return authService.register(request)
                .map(ResponseEntity::ok)
                .onErrorResume(ex -> {
                    System.err.println("Registration error: " + ex.getMessage());
                    ex.printStackTrace();
                    return Mono.just(ResponseEntity.badRequest()
                            .body(new AuthResponse("Registration failed: " + ex.getMessage(), null, null)));
                });
    }

    @PostMapping("/login")
    public Mono<ResponseEntity<AuthResponse>> login(@Valid @RequestBody LoginRequest request) {
        return authService.login(request)
                .map(ResponseEntity::ok)
                .onErrorReturn(ResponseEntity.badRequest().build());
    }

    @PostMapping("/refresh")
    public Mono<ResponseEntity<AuthResponse>> refreshToken(@RequestBody RefreshTokenRequest request) {
        return authService.refreshToken(request.getRefreshToken())
                .map(ResponseEntity::ok)
                .onErrorReturn(ResponseEntity.badRequest().build());
    }

    @GetMapping("/verify-email")
    public Mono<ResponseEntity<String>> verifyEmail(@RequestParam String token) {
        return authService.verifyEmail(token)
                .map(ResponseEntity::ok)
                .onErrorReturn(ResponseEntity.badRequest().body("Invalid verification token"));
    }

    @GetMapping("/health")
    public Mono<ResponseEntity<String>> health() {
        return Mono.just(ResponseEntity.ok("Auth service is healthy"));
    }

    // DTO for refresh token request
    public static class RefreshTokenRequest {
        private String refreshToken;

        public String getRefreshToken() {
            return refreshToken;
        }

        public void setRefreshToken(String refreshToken) {
            this.refreshToken = refreshToken;
        }
    }
} 