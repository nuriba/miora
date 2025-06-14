package com.miora.controller;

import com.miora.domain.model.Avatar;
import com.miora.service.AvatarService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/v1/avatars")
public class AvatarController {

    private final AvatarService avatarService;

    public AvatarController(AvatarService avatarService) {
        this.avatarService = avatarService;
    }

    @GetMapping
    public Flux<Avatar> getUserAvatars(Authentication authentication) {
        Long userId = Long.parseLong(authentication.getName());
        return avatarService.getUserAvatars(userId);
    }

    @PostMapping("/generate")
    public Mono<ResponseEntity<String>> generateAvatar(@RequestBody AvatarGenerationRequest request, 
                                                      Authentication authentication) {
        Long userId = Long.parseLong(authentication.getName());
        return avatarService.generateAvatar(userId, request.getImageUrls(), request.getPrivacyLevel())
                .map(taskId -> ResponseEntity.ok("Avatar generation started. Task ID: " + taskId))
                .onErrorReturn(ResponseEntity.badRequest().body("Failed to start avatar generation"));
    }

    @GetMapping("/{avatarId}")
    public Mono<ResponseEntity<Avatar>> getAvatar(@PathVariable Long avatarId, Authentication authentication) {
        Long userId = Long.parseLong(authentication.getName());
        return avatarService.getAvatar(avatarId, userId)
                .map(ResponseEntity::ok)
                .switchIfEmpty(Mono.just(ResponseEntity.notFound().build()));
    }

    @DeleteMapping("/{avatarId}")
    public Mono<ResponseEntity<String>> deleteAvatar(@PathVariable Long avatarId, Authentication authentication) {
        Long userId = Long.parseLong(authentication.getName());
        return avatarService.deleteAvatar(avatarId, userId)
                .then(Mono.just(ResponseEntity.ok("Avatar deleted successfully")))
                .onErrorReturn(ResponseEntity.badRequest().body("Failed to delete avatar"));
    }

    // DTO for avatar generation request
    public static class AvatarGenerationRequest {
        private java.util.List<String> imageUrls;
        private String privacyLevel;

        public java.util.List<String> getImageUrls() {
            return imageUrls;
        }

        public void setImageUrls(java.util.List<String> imageUrls) {
            this.imageUrls = imageUrls;
        }

        public String getPrivacyLevel() {
            return privacyLevel;
        }

        public void setPrivacyLevel(String privacyLevel) {
            this.privacyLevel = privacyLevel;
        }
    }
} 