package com.miora.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

/**
 * Service class for handling file uploads and storage
 */
@Service
public class FileUploadService {

    @Value("${miora.upload.garment-storage-path:/tmp/miora/garments}")
    private String garmentStoragePath;
    
    @Value("${miora.upload.avatar-storage-path:/tmp/miora/avatars}")
    private String avatarStoragePath;
    
    @Value("${miora.upload.max-file-size:10485760}") // 10MB default
    private long maxFileSize;
    
    private static final String[] ALLOWED_IMAGE_TYPES = {
        "image/jpeg", "image/jpg", "image/png", "image/webp"
    };

    // Upload garment image
    public Mono<String> uploadGarmentImage(MultipartFile file) {
        return validateImageFile(file)
                .then(saveFile(file, garmentStoragePath, "garment"))
                .map(this::generatePublicUrl);
    }

    // Upload avatar image
    public Mono<String> uploadAvatarImage(MultipartFile file) {
        return validateImageFile(file)
                .then(saveFile(file, avatarStoragePath, "avatar"))
                .map(this::generatePublicUrl);
    }

    // Delete file
    public Mono<Void> deleteFile(String fileUrl) {
        return Mono.fromRunnable(() -> {
            try {
                String fileName = extractFileNameFromUrl(fileUrl);
                Path filePath = Paths.get(garmentStoragePath, fileName);
                Files.deleteIfExists(filePath);
                
                // Also try avatar path if not found in garment path
                filePath = Paths.get(avatarStoragePath, fileName);
                Files.deleteIfExists(filePath);
            } catch (IOException e) {
                // Log error but don't fail the operation
                System.err.println("Failed to delete file: " + fileUrl + ", error: " + e.getMessage());
            }
        });
    }

    // Validate image file
    private Mono<Void> validateImageFile(MultipartFile file) {
        return Mono.fromRunnable(() -> {
            if (file == null || file.isEmpty()) {
                throw new IllegalArgumentException("File is required");
            }
            
            if (file.getSize() > maxFileSize) {
                throw new IllegalArgumentException(
                    "File size exceeds maximum allowed size of " + (maxFileSize / 1024 / 1024) + "MB");
            }
            
            String contentType = file.getContentType();
            if (contentType == null || !isAllowedImageType(contentType)) {
                throw new IllegalArgumentException(
                    "Invalid file type. Allowed types: JPEG, PNG, WebP");
            }
        });
    }

    // Save file to storage
    private Mono<String> saveFile(MultipartFile file, String storagePath, String prefix) {
        return Mono.fromCallable(() -> {
            try {
                // Create directory if it doesn't exist
                Path storageDir = Paths.get(storagePath);
                Files.createDirectories(storageDir);
                
                // Generate unique filename
                String originalFilename = file.getOriginalFilename();
                String extension = getFileExtension(originalFilename);
                String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
                String uniqueId = UUID.randomUUID().toString().substring(0, 8);
                String fileName = prefix + "_" + timestamp + "_" + uniqueId + extension;
                
                // Save file
                Path targetPath = storageDir.resolve(fileName);
                Files.copy(file.getInputStream(), targetPath, StandardCopyOption.REPLACE_EXISTING);
                
                return fileName;
            } catch (IOException e) {
                throw new RuntimeException("Failed to save file: " + e.getMessage(), e);
            }
        });
    }

    // Generate public URL for file
    private String generatePublicUrl(String fileName) {
        // In a real implementation, this would return the full URL
        // For now, return relative path
        return "/uploads/" + fileName;
    }

    // Extract filename from URL
    private String extractFileNameFromUrl(String url) {
        if (url == null) return "";
        return url.substring(url.lastIndexOf('/') + 1);
    }

    // Check if content type is allowed
    private boolean isAllowedImageType(String contentType) {
        for (String allowedType : ALLOWED_IMAGE_TYPES) {
            if (allowedType.equals(contentType)) {
                return true;
            }
        }
        return false;
    }

    // Get file extension
    private String getFileExtension(String filename) {
        if (filename == null || !filename.contains(".")) {
            return ".jpg"; // Default extension
        }
        return filename.substring(filename.lastIndexOf('.'));
    }

    // Get file info
    public static class FileInfo {
        private String fileName;
        private String contentType;
        private long size;
        private String url;

        public FileInfo(String fileName, String contentType, long size, String url) {
            this.fileName = fileName;
            this.contentType = contentType;
            this.size = size;
            this.url = url;
        }

        // Getters
        public String getFileName() { return fileName; }
        public String getContentType() { return contentType; }
        public long getSize() { return size; }
        public String getUrl() { return url; }
    }
} 