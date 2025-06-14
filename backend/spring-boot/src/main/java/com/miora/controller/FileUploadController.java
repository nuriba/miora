package com.miora.controller;

import com.miora.service.FileUploadService;
import com.miora.security.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

/**
 * REST Controller for file upload APIs
 */
@RestController
@RequestMapping("/api/v1/upload")
@CrossOrigin(origins = "*")
public class FileUploadController {

    private final FileUploadService fileUploadService;
    private final JwtUtil jwtUtil;

    public FileUploadController(FileUploadService fileUploadService, JwtUtil jwtUtil) {
        this.fileUploadService = fileUploadService;
        this.jwtUtil = jwtUtil;
    }

    // Upload garment image
    @PostMapping(value = "/garment", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<FileUploadResponse>> uploadGarmentImage(
            @RequestHeader("Authorization") String token,
            @RequestPart("file") MultipartFile file) {
        
        Long userId = extractUserIdFromToken(token);
        
        return fileUploadService.uploadGarmentImage(file)
                .map(fileUrl -> ResponseEntity.ok(new FileUploadResponse(
                    file.getOriginalFilename(),
                    fileUrl,
                    file.getSize(),
                    file.getContentType(),
                    "Garment image uploaded successfully",
                    LocalDateTime.now()
                )))
                .onErrorResume(this::handleError);
    }

    // Upload avatar image
    @PostMapping(value = "/avatar", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<FileUploadResponse>> uploadAvatarImage(
            @RequestHeader("Authorization") String token,
            @RequestPart("file") MultipartFile file) {
        
        Long userId = extractUserIdFromToken(token);
        
        return fileUploadService.uploadAvatarImage(file)
                .map(fileUrl -> ResponseEntity.ok(new FileUploadResponse(
                    file.getOriginalFilename(),
                    fileUrl,
                    file.getSize(),
                    file.getContentType(),
                    "Avatar image uploaded successfully",
                    LocalDateTime.now()
                )))
                .onErrorResume(this::handleError);
    }

    // Validate file before upload
    @PostMapping(value = "/validate", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<FileValidationResponse>> validateFile(
            @RequestPart("file") MultipartFile file) {
        
        return Mono.fromCallable(() -> {
            boolean isValid = true;
            String message = "File is valid";
            
            try {
                if (file == null || file.isEmpty()) {
                    isValid = false;
                    message = "File is required";
                } else if (file.getSize() > 10485760) { // 10MB
                    isValid = false;
                    message = "File size exceeds maximum allowed size of 10MB";
                } else {
                    String contentType = file.getContentType();
                    if (contentType == null || !isAllowedImageType(contentType)) {
                        isValid = false;
                        message = "Invalid file type. Allowed types: JPEG, PNG, WebP";
                    }
                }
            } catch (Exception e) {
                isValid = false;
                message = "File validation failed: " + e.getMessage();
            }
            
            FileValidationResponse response = new FileValidationResponse(
                isValid,
                message,
                file.getOriginalFilename(),
                file.getSize(),
                file.getContentType()
            );
            
            return isValid ? ResponseEntity.ok(response) : ResponseEntity.badRequest().body(response);
        });
    }

    // Get upload limits
    @GetMapping("/limits")
    public ResponseEntity<UploadLimitsResponse> getUploadLimits() {
        UploadLimitsResponse limits = new UploadLimitsResponse(
            10485760L, // 10MB
            Arrays.asList("image/jpeg", "image/jpg", "image/png", "image/webp"),
            100 // max files per user
        );
        return ResponseEntity.ok(limits);
    }

    // Delete uploaded file
    @DeleteMapping("/{fileName}")
    @PreAuthorize("hasRole('USER')")
    public Mono<ResponseEntity<Void>> deleteFile(
            @RequestHeader("Authorization") String token,
            @PathVariable String fileName) {
        
        Long userId = extractUserIdFromToken(token);
        String fileUrl = "/uploads/" + fileName;
        
        return fileUploadService.deleteFile(fileUrl)
                .then(Mono.just(ResponseEntity.noContent().<Void>build()))
                .onErrorResume(this::handleError);
    }

    // Helper methods
    private Long extractUserIdFromToken(String token) {
        String jwt = token.replace("Bearer ", "");
        return Long.valueOf(jwtUtil.getUserIdFromToken(jwt));
    }

    private boolean isAllowedImageType(String contentType) {
        String[] allowedTypes = {"image/jpeg", "image/jpg", "image/png", "image/webp"};
        for (String allowedType : allowedTypes) {
            if (allowedType.equals(contentType)) {
                return true;
            }
        }
        return false;
    }


    private <T> Mono<ResponseEntity<T>> handleError(Throwable error) {
        if (error instanceof IllegalArgumentException) {
            return Mono.just(ResponseEntity.badRequest().build());
        } else if (error instanceof SecurityException) {
            return Mono.just(ResponseEntity.status(HttpStatus.FORBIDDEN).build());
        } else if (error instanceof IllegalStateException) {
            return Mono.just(ResponseEntity.status(HttpStatus.PAYLOAD_TOO_LARGE).build());
        } else {
            return Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build());
        }
    }

    // DTOs
    public static class FileUploadResponse {
        private String fileName;
        private String fileUrl;
        private Long fileSize;
        private String contentType;
        private String message;
        private LocalDateTime uploadedAt;

        public FileUploadResponse(String fileName, String fileUrl, Long fileSize,
                                String contentType, String message, LocalDateTime uploadedAt) {
            this.fileName = fileName;
            this.fileUrl = fileUrl;
            this.fileSize = fileSize;
            this.contentType = contentType;
            this.message = message;
            this.uploadedAt = uploadedAt;
        }

        // Getters
        public String getFileName() { return fileName; }
        public String getFileUrl() { return fileUrl; }
        public Long getFileSize() { return fileSize; }
        public String getContentType() { return contentType; }
        public String getMessage() { return message; }
        public LocalDateTime getUploadedAt() { return uploadedAt; }
    }

    public static class FileValidationResponse {
        private Boolean isValid;
        private String message;
        private String fileName;
        private Long fileSize;
        private String contentType;

        public FileValidationResponse(Boolean isValid, String message, String fileName,
                                    Long fileSize, String contentType) {
            this.isValid = isValid;
            this.message = message;
            this.fileName = fileName;
            this.fileSize = fileSize;
            this.contentType = contentType;
        }

        // Getters
        public Boolean getIsValid() { return isValid; }
        public String getMessage() { return message; }
        public String getFileName() { return fileName; }
        public Long getFileSize() { return fileSize; }
        public String getContentType() { return contentType; }
    }

    public static class UploadLimitsResponse {
        private Long maxFileSize;
        private List<String> allowedTypes;
        private Integer maxFilesPerUser;

        public UploadLimitsResponse(Long maxFileSize, List<String> allowedTypes,
                                  Integer maxFilesPerUser) {
            this.maxFileSize = maxFileSize;
            this.allowedTypes = allowedTypes;
            this.maxFilesPerUser = maxFilesPerUser;
        }

        // Getters
        public Long getMaxFileSize() { return maxFileSize; }
        public List<String> getAllowedTypes() { return allowedTypes; }
        public Integer getMaxFilesPerUser() { return maxFilesPerUser; }
    }
} 