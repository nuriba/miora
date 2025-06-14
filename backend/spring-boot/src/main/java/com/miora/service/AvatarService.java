package com.miora.service;

import com.miora.domain.model.Avatar;
import com.miora.repository.AvatarRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
public class AvatarService {

    private final AvatarRepository avatarRepository;
    private final WebClient mlServiceClient;

    public AvatarService(AvatarRepository avatarRepository, WebClient.Builder webClientBuilder) {
        this.avatarRepository = avatarRepository;
        this.mlServiceClient = webClientBuilder
                .baseUrl("http://localhost:8000")
                .build();
    }

    public Flux<Avatar> getUserAvatars(Long userId) {
        return avatarRepository.findByUserId(userId);
    }

    public Mono<String> generateAvatar(Long userId, List<String> imageUrls, String privacyLevel) {
        // Call ML service to generate avatar
        return mlServiceClient.post()
                .uri("/api/v1/avatar/generate")
                .bodyValue(new AvatarGenerationRequest(userId.toString(), imageUrls, privacyLevel))
                .retrieve()
                .bodyToMono(AvatarGenerationResponse.class)
                .map(response -> response.getTaskId())
                .onErrorReturn("failed");
    }

    public Mono<Avatar> getAvatar(Long avatarId, Long userId) {
        return avatarRepository.findById(avatarId)
                .filter(avatar -> avatar.getUserId().equals(userId));
    }

    public Mono<Void> deleteAvatar(Long avatarId, Long userId) {
        return avatarRepository.findById(avatarId)
                .filter(avatar -> avatar.getUserId().equals(userId))
                .flatMap(avatar -> avatarRepository.delete(avatar));
    }

    // DTOs for ML service communication
    public static class AvatarGenerationRequest {
        private String userId;
        private List<String> imageUrls;
        private String privacyLevel;

        public AvatarGenerationRequest(String userId, List<String> imageUrls, String privacyLevel) {
            this.userId = userId;
            this.imageUrls = imageUrls;
            this.privacyLevel = privacyLevel;
        }

        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
        public List<String> getImageUrls() { return imageUrls; }
        public void setImageUrls(List<String> imageUrls) { this.imageUrls = imageUrls; }
        public String getPrivacyLevel() { return privacyLevel; }
        public void setPrivacyLevel(String privacyLevel) { this.privacyLevel = privacyLevel; }
    }

    public static class AvatarGenerationResponse {
        private String taskId;
        private String status;

        public String getTaskId() { return taskId; }
        public void setTaskId(String taskId) { this.taskId = taskId; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
    }
} 