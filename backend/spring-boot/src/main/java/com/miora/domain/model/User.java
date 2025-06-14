package com.miora.domain.model;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * User entity representing registered users of the Miora platform
 * 
 * Covers requirements:
 * - ACC-01: Sign-up via email/password or OAuth
 * - ACC-02: Email verification status
 * - UPR-01: User profile management
 * - UPR-05: Privacy settings
 */
@Table("users")
public class User {
    
    @Id
    private Long id;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Column("email")
    private String email;
    
    @Column("password_hash")
    private String passwordHash; // Nullable for OAuth-only users
    
    @NotBlank(message = "Display name is required")
    @Size(min = 2, max = 50, message = "Display name must be between 2 and 50 characters")
    @Column("display_name")
    private String displayName;
    
    @Column("profile_image_url")
    private String profileImageUrl;
    
    @Column("is_email_verified")
    private Boolean isEmailVerified = false;
    
    @Column("email_verification_token")
    private String emailVerificationToken;
    
    @Column("email_verification_expires_at")
    private LocalDateTime emailVerificationExpiresAt;
    
    @Column("password_reset_token")
    private String passwordResetToken;
    
    @Column("password_reset_expires_at")
    private LocalDateTime passwordResetExpiresAt;
    
    @Column("is_two_factor_enabled")
    private Boolean isTwoFactorEnabled = false;
    
    @Column("two_factor_secret")
    private String twoFactorSecret;
    
    @Column("default_privacy_level")
    private PrivacyLevel defaultPrivacyLevel = PrivacyLevel.FRIENDS;
    
    @Column("preferred_language")
    private String preferredLanguage = "en";
    
    @Column("active_avatar_id")
    private Long activeAvatarId;
    
    @Column("failed_login_attempts")
    private Integer failedLoginAttempts = 0;
    
    @Column("locked_until")
    private LocalDateTime lockedUntil;
    
    @Column("last_login_at")
    private LocalDateTime lastLoginAt;
    
    @Column("is_active")
    private Boolean isActive = true;
    
    // OAuth provider information
    @Column("google_id")
    private String googleId;
    
    @Column("apple_id")
    private String appleId;
    
    @CreatedDate
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors
    public User() {}
    
    public User(String email, String displayName) {
        this.email = email;
        this.displayName = displayName;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getPasswordHash() {
        return passwordHash;
    }
    
    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }
    
    public String getDisplayName() {
        return displayName;
    }
    
    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }
    
    public String getProfileImageUrl() {
        return profileImageUrl;
    }
    
    public void setProfileImageUrl(String profileImageUrl) {
        this.profileImageUrl = profileImageUrl;
    }
    
    public Boolean getIsEmailVerified() {
        return isEmailVerified;
    }
    
    public void setIsEmailVerified(Boolean isEmailVerified) {
        this.isEmailVerified = isEmailVerified;
    }
    
    public String getEmailVerificationToken() {
        return emailVerificationToken;
    }
    
    public void setEmailVerificationToken(String emailVerificationToken) {
        this.emailVerificationToken = emailVerificationToken;
    }
    
    public LocalDateTime getEmailVerificationExpiresAt() {
        return emailVerificationExpiresAt;
    }
    
    public void setEmailVerificationExpiresAt(LocalDateTime emailVerificationExpiresAt) {
        this.emailVerificationExpiresAt = emailVerificationExpiresAt;
    }
    
    public String getPasswordResetToken() {
        return passwordResetToken;
    }
    
    public void setPasswordResetToken(String passwordResetToken) {
        this.passwordResetToken = passwordResetToken;
    }
    
    public LocalDateTime getPasswordResetExpiresAt() {
        return passwordResetExpiresAt;
    }
    
    public void setPasswordResetExpiresAt(LocalDateTime passwordResetExpiresAt) {
        this.passwordResetExpiresAt = passwordResetExpiresAt;
    }
    
    public Boolean getIsTwoFactorEnabled() {
        return isTwoFactorEnabled;
    }
    
    public void setIsTwoFactorEnabled(Boolean isTwoFactorEnabled) {
        this.isTwoFactorEnabled = isTwoFactorEnabled;
    }
    
    public String getTwoFactorSecret() {
        return twoFactorSecret;
    }
    
    public void setTwoFactorSecret(String twoFactorSecret) {
        this.twoFactorSecret = twoFactorSecret;
    }
    
    public PrivacyLevel getDefaultPrivacyLevel() {
        return defaultPrivacyLevel;
    }
    
    public void setDefaultPrivacyLevel(PrivacyLevel defaultPrivacyLevel) {
        this.defaultPrivacyLevel = defaultPrivacyLevel;
    }
    
    public String getPreferredLanguage() {
        return preferredLanguage;
    }
    
    public void setPreferredLanguage(String preferredLanguage) {
        this.preferredLanguage = preferredLanguage;
    }
    
    public Long getActiveAvatarId() {
        return activeAvatarId;
    }
    
    public void setActiveAvatarId(Long activeAvatarId) {
        this.activeAvatarId = activeAvatarId;
    }
    
    public Integer getFailedLoginAttempts() {
        return failedLoginAttempts;
    }
    
    public void setFailedLoginAttempts(Integer failedLoginAttempts) {
        this.failedLoginAttempts = failedLoginAttempts;
    }
    
    public LocalDateTime getLockedUntil() {
        return lockedUntil;
    }
    
    public void setLockedUntil(LocalDateTime lockedUntil) {
        this.lockedUntil = lockedUntil;
    }
    
    public LocalDateTime getLastLoginAt() {
        return lastLoginAt;
    }
    
    public void setLastLoginAt(LocalDateTime lastLoginAt) {
        this.lastLoginAt = lastLoginAt;
    }
    
    public Boolean getIsActive() {
        return isActive;
    }
    
    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }
    
    public String getGoogleId() {
        return googleId;
    }
    
    public void setGoogleId(String googleId) {
        this.googleId = googleId;
    }
    
    public String getAppleId() {
        return appleId;
    }
    
    public void setAppleId(String appleId) {
        this.appleId = appleId;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
    
    // Business logic methods
    public boolean isAccountLocked() {
        return lockedUntil != null && lockedUntil.isAfter(LocalDateTime.now());
    }
    
    public boolean isOAuthUser() {
        return passwordHash == null && (googleId != null || appleId != null);
    }
    
    public void incrementFailedLoginAttempts() {
        this.failedLoginAttempts = (this.failedLoginAttempts == null) ? 1 : this.failedLoginAttempts + 1;
    }
    
    public void resetFailedLoginAttempts() {
        this.failedLoginAttempts = 0;
        this.lockedUntil = null;
    }
    
    public void lockAccount(int lockoutMinutes) {
        this.lockedUntil = LocalDateTime.now().plusMinutes(lockoutMinutes);
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return Objects.equals(id, user.id) && Objects.equals(email, user.email);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id, email);
    }
    
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", email='" + email + '\'' +
                ", displayName='" + displayName + '\'' +
                ", isEmailVerified=" + isEmailVerified +
                ", isActive=" + isActive +
                '}';
    }
} 