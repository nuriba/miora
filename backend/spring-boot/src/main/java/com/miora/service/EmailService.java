package com.miora.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Service
public class EmailService {

    private final JavaMailSender mailSender;
    
    @Value("${spring.profiles.active:}")
    private String activeProfile;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public Mono<Void> sendVerificationEmail(String email, String token) {
        // Skip email sending in test profile
        if ("test".equals(activeProfile)) {
            System.out.println("TEST MODE: Would send verification email to " + email + " with token " + token);
            return Mono.empty();
        }
        
        return Mono.fromRunnable(() -> {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(email);
            message.setSubject("Miora - Verify Your Email");
            message.setText("Please click the following link to verify your email: " +
                    "http://localhost:8080/api/v1/auth/verify-email?token=" + token);
            
            mailSender.send(message);
        }).subscribeOn(Schedulers.boundedElastic()).then();
    }

    public Mono<Void> sendPasswordResetEmail(String email, String token) {
        // Skip email sending in test profile
        if ("test".equals(activeProfile)) {
            System.out.println("TEST MODE: Would send password reset email to " + email + " with token " + token);
            return Mono.empty();
        }
        
        return Mono.fromRunnable(() -> {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(email);
            message.setSubject("Miora - Password Reset");
            message.setText("Please click the following link to reset your password: " +
                    "http://localhost:3000/reset-password?token=" + token);
            
            mailSender.send(message);
        }).subscribeOn(Schedulers.boundedElastic()).then();
    }
} 