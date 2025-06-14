package com.miora.security;

import org.springframework.security.authentication.ReactiveAuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

import java.util.List;

@Component
public class JwtAuthenticationManager implements ReactiveAuthenticationManager {

    private final JwtUtil jwtUtil;

    public JwtAuthenticationManager(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    public Mono<Authentication> authenticate(Authentication authentication) {
        String token = authentication.getCredentials().toString();
        
        return Mono.fromCallable(() -> {
            try {
                if (jwtUtil.isTokenExpired(token) || !jwtUtil.isAccessToken(token)) {
                    throw new RuntimeException("Token is expired or invalid");
                }
                
                String userId = jwtUtil.getUserIdFromToken(token);
                String role = jwtUtil.getRoleFromToken(token);
                
                List<SimpleGrantedAuthority> authorities = List.of(
                    new SimpleGrantedAuthority("ROLE_" + role.toUpperCase())
                );
                
                Authentication auth = new UsernamePasswordAuthenticationToken(userId, null, authorities);
                return auth;
            } catch (Exception e) {
                throw new RuntimeException("Authentication failed", e);
            }
        }).onErrorMap(throwable -> new RuntimeException("Authentication failed", throwable));
    }
} 