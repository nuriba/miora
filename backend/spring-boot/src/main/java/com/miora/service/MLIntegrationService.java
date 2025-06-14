package com.miora.service;

import com.miora.domain.model.TryOnSession;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.time.Duration;

/**
 * Service class for integrating with the ML service
 */
@Service
public class MLIntegrationService {

    private final WebClient webClient;
    private final TryOnService tryOnService;
    
    @Value("${miora.ml-service.base-url:http://localhost:8000}")
    private String mlServiceBaseUrl;
    
    @Value("${miora.ml-service.timeout:30s}")
    private Duration timeout;

    public MLIntegrationService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .codecs(clientCodecConfigurer -> 
                    clientCodecConfigurer.defaultCodecs().maxInMemorySize(10 * 1024 * 1024)) // 10MB
                .build();
        this.tryOnService = null; // Avoid circular dependency for now
    }

    // Process try-on session asynchronously
    public Mono<Void> processTryOnAsync(TryOnSession session) {
        return Mono.fromRunnable(() -> {
            // Start async processing in background
            processTryOnWithML(session)
                .subscribe(
                    result -> {
                        // Success - this would normally call back to TryOnService
                        System.out.println("Try-on completed for session " + session.getId() + 
                                         " with quality score: " + result.getQualityScore());
                    },
                    error -> {
                        // Error - this would normally call back to TryOnService
                        System.err.println("Try-on failed for session " + session.getId() + 
                                         ": " + error.getMessage());
                    }
                );
        });
    }

    // Process try-on with ML service
    private Mono<TryOnService.TryOnResult> processTryOnWithML(TryOnSession session) {
        TryOnRequest request = new TryOnRequest();
        request.setSessionId(session.getId());
        request.setAvatarImageUrl(getAvatarImageUrl(session.getAvatarId()));
        request.setGarmentImageUrl(getGarmentImageUrl(session.getGarmentId()));
        
        return webClient.post()
                .uri(mlServiceBaseUrl + "/try-on")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(TryOnResponse.class)
                .timeout(timeout)
                .map(response -> new TryOnService.TryOnResult(
                    response.getResultImageUrl(),
                    response.getProcessingTimeMs(),
                    response.getQualityScore()
                ))
                .doOnError(error -> 
                    System.err.println("ML service error: " + error.getMessage())
                );
    }

    // Get avatar image URL (placeholder - would integrate with avatar service)
    private String getAvatarImageUrl(Long avatarId) {
        // This would normally fetch the avatar image URL from the database
        return "avatar_" + avatarId + ".jpg";
    }

    // Get garment image URL (placeholder - would integrate with garment service)
    private String getGarmentImageUrl(Long garmentId) {
        // This would normally fetch the garment image URL from the database
        return "garment_" + garmentId + ".jpg";
    }

    // Process avatar for ML readiness
    public Mono<ProcessingResult> processAvatar(String avatarImageUrl) {
        ProcessAvatarRequest request = new ProcessAvatarRequest();
        request.setImageUrl(avatarImageUrl);
        
        return webClient.post()
                .uri(mlServiceBaseUrl + "/process-avatar")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ProcessingResult.class)
                .timeout(timeout);
    }

    // Process garment for ML readiness
    public Mono<ProcessingResult> processGarment(String garmentImageUrl) {
        ProcessGarmentRequest request = new ProcessGarmentRequest();
        request.setImageUrl(garmentImageUrl);
        
        return webClient.post()
                .uri(mlServiceBaseUrl + "/process-garment")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ProcessingResult.class)
                .timeout(timeout);
    }

    // Check ML service health
    public Mono<Boolean> isMLServiceHealthy() {
        return webClient.get()
                .uri(mlServiceBaseUrl + "/health")
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(5))
                .map(response -> true)
                .onErrorReturn(false);
    }

    // DTOs for ML service communication
    public static class TryOnRequest {
        private Long sessionId;
        private String avatarImageUrl;
        private String garmentImageUrl;

        // Getters and setters
        public Long getSessionId() { return sessionId; }
        public void setSessionId(Long sessionId) { this.sessionId = sessionId; }
        public String getAvatarImageUrl() { return avatarImageUrl; }
        public void setAvatarImageUrl(String avatarImageUrl) { this.avatarImageUrl = avatarImageUrl; }
        public String getGarmentImageUrl() { return garmentImageUrl; }
        public void setGarmentImageUrl(String garmentImageUrl) { this.garmentImageUrl = garmentImageUrl; }
    }

    public static class TryOnResponse {
        private String resultImageUrl;
        private Integer processingTimeMs;
        private BigDecimal qualityScore;
        private String status;
        private String errorMessage;

        // Getters and setters
        public String getResultImageUrl() { return resultImageUrl; }
        public void setResultImageUrl(String resultImageUrl) { this.resultImageUrl = resultImageUrl; }
        public Integer getProcessingTimeMs() { return processingTimeMs; }
        public void setProcessingTimeMs(Integer processingTimeMs) { this.processingTimeMs = processingTimeMs; }
        public BigDecimal getQualityScore() { return qualityScore; }
        public void setQualityScore(BigDecimal qualityScore) { this.qualityScore = qualityScore; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public String getErrorMessage() { return errorMessage; }
        public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
    }

    public static class ProcessAvatarRequest {
        private String imageUrl;

        public String getImageUrl() { return imageUrl; }
        public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    }

    public static class ProcessGarmentRequest {
        private String imageUrl;

        public String getImageUrl() { return imageUrl; }
        public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    }

    public static class ProcessingResult {
        private String processedDataUrl;
        private String status;
        private String errorMessage;
        private BigDecimal qualityScore;

        // Getters and setters
        public String getProcessedDataUrl() { return processedDataUrl; }
        public void setProcessedDataUrl(String processedDataUrl) { this.processedDataUrl = processedDataUrl; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public String getErrorMessage() { return errorMessage; }
        public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
        public BigDecimal getQualityScore() { return qualityScore; }
        public void setQualityScore(BigDecimal qualityScore) { this.qualityScore = qualityScore; }
    }
} 