# Miora Database Design

## Overview
Database design for Miora - AI-powered virtual avatar and garment try-on platform.

## Core Entities

### 1. Users
- **Purpose**: Store user account information
- **Key Features**: Authentication, profiles, preferences
```sql
users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(255) NOT NULL,
    profile_image_url VARCHAR(500),
    bio TEXT,
    is_email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    email_verification_expires_at TIMESTAMP,
    password_reset_token VARCHAR(255),
    password_reset_expires_at TIMESTAMP,
    is_two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    default_privacy_level VARCHAR(50) DEFAULT 'FRIENDS',
    preferred_language VARCHAR(10) DEFAULT 'en',
    active_avatar_id BIGINT,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    google_id VARCHAR(255),
    apple_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)
```

### 2. Avatars
- **Purpose**: Store user's AI-generated avatars
- **Key Features**: Multiple avatars per user, privacy settings
```sql
avatars (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    avatar_data_url TEXT NOT NULL,
    generation_method VARCHAR(50) NOT NULL, -- AI_GENERATED, PHOTO_UPLOAD, MANUAL
    processing_status VARCHAR(50) NOT NULL, -- PENDING, PROCESSING, COMPLETED, FAILED
    is_public BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    body_type VARCHAR(50), -- SLIM, ATHLETIC, CURVY, PLUS_SIZE
    height_cm INTEGER,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

### 3. Garment Categories
- **Purpose**: Hierarchical categorization of clothing items
```sql
garment_categories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    parent_id BIGINT, -- For subcategories
    description TEXT,
    icon_url VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES garment_categories(id)
)
```

### 4. Garments
- **Purpose**: Store clothing items for virtual try-on
```sql
garments (
    id BIGINT PRIMARY KEY,
    user_id BIGINT, -- NULL for system/brand garments
    category_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    price DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    garment_image_url VARCHAR(500) NOT NULL,
    garment_data_url TEXT, -- 3D model or processed image data
    color VARCHAR(100),
    size_info JSON, -- {"sizes": ["S", "M", "L"], "measurements": {...}}
    material VARCHAR(255),
    care_instructions TEXT,
    processing_status VARCHAR(50) NOT NULL, -- PENDING, PROCESSING, COMPLETED, FAILED
    is_public BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    try_on_count INTEGER DEFAULT 0,
    external_url VARCHAR(500), -- Link to purchase
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES garment_categories(id)
)
```

### 5. Try-On Sessions
- **Purpose**: Store virtual try-on results and history
```sql
try_on_sessions (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    avatar_id BIGINT NOT NULL,
    garment_id BIGINT NOT NULL,
    session_name VARCHAR(255),
    result_image_url VARCHAR(500), -- Final try-on result
    processing_status VARCHAR(50) NOT NULL, -- PENDING, PROCESSING, COMPLETED, FAILED
    processing_time_ms INTEGER,
    quality_score DECIMAL(3,2), -- AI confidence score 0-1
    is_saved BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    metadata JSON, -- Additional processing info
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (avatar_id) REFERENCES avatars(id) ON DELETE CASCADE,
    FOREIGN KEY (garment_id) REFERENCES garments(id) ON DELETE CASCADE
)
```

### 6. Collections
- **Purpose**: User-created collections of garments
```sql
collections (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cover_image_url VARCHAR(500),
    is_public BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

### 7. Collection Items
- **Purpose**: Many-to-many relationship between collections and garments
```sql
collection_items (
    id BIGINT PRIMARY KEY,
    collection_id BIGINT NOT NULL,
    garment_id BIGINT NOT NULL,
    added_at TIMESTAMP NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE,
    FOREIGN KEY (garment_id) REFERENCES garments(id) ON DELETE CASCADE,
    UNIQUE(collection_id, garment_id)
)
```

### 8. User Follows
- **Purpose**: Social following relationships
```sql
user_follows (
    id BIGINT PRIMARY KEY,
    follower_id BIGINT NOT NULL,
    followed_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(follower_id, followed_id)
)
```

### 9. Likes
- **Purpose**: User likes on garments, avatars, or try-on sessions
```sql
likes (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    target_type VARCHAR(50) NOT NULL, -- GARMENT, AVATAR, TRY_ON_SESSION
    target_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, target_type, target_id)
)
```

### 10. Comments
- **Purpose**: Comments on garments, avatars, or try-on sessions
```sql
comments (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    target_type VARCHAR(50) NOT NULL, -- GARMENT, AVATAR, TRY_ON_SESSION
    target_id BIGINT NOT NULL,
    parent_id BIGINT, -- For reply comments
    content TEXT NOT NULL,
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
)
```

## Indexes for Performance

```sql
-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_email_verification_token ON users(email_verification_token);
CREATE INDEX idx_users_password_reset_token ON users(password_reset_token);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Avatars
CREATE INDEX idx_avatars_user_id ON avatars(user_id);
CREATE INDEX idx_avatars_is_public ON avatars(is_public);
CREATE INDEX idx_avatars_processing_status ON avatars(processing_status);

-- Garments
CREATE INDEX idx_garments_user_id ON garments(user_id);
CREATE INDEX idx_garments_category_id ON garments(category_id);
CREATE INDEX idx_garments_is_public ON garments(is_public);
CREATE INDEX idx_garments_is_featured ON garments(is_featured);
CREATE INDEX idx_garments_created_at ON garments(created_at);
CREATE INDEX idx_garments_brand ON garments(brand);

-- Try-On Sessions
CREATE INDEX idx_try_on_sessions_user_id ON try_on_sessions(user_id);
CREATE INDEX idx_try_on_sessions_avatar_id ON try_on_sessions(avatar_id);
CREATE INDEX idx_try_on_sessions_garment_id ON try_on_sessions(garment_id);
CREATE INDEX idx_try_on_sessions_created_at ON try_on_sessions(created_at);
CREATE INDEX idx_try_on_sessions_is_public ON try_on_sessions(is_public);

-- Collections
CREATE INDEX idx_collections_user_id ON collections(user_id);
CREATE INDEX idx_collections_is_public ON collections(is_public);

-- Social features
CREATE INDEX idx_user_follows_follower_id ON user_follows(follower_id);
CREATE INDEX idx_user_follows_followed_id ON user_follows(followed_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);
CREATE INDEX idx_likes_target ON likes(target_type, target_id);
CREATE INDEX idx_comments_target ON comments(target_type, target_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
```

## Data Relationships

1. **User → Avatars**: One-to-Many (user can have multiple avatars)
2. **User → Garments**: One-to-Many (user can upload multiple garments)
3. **Avatar + Garment → Try-On Session**: Many-to-Many through try_on_sessions
4. **User → Collections**: One-to-Many 
5. **Collection → Garments**: Many-to-Many through collection_items
6. **User → User**: Many-to-Many through user_follows (social graph)
7. **User → Content**: Many-to-Many through likes and comments

## Business Logic Constraints

1. **Avatar Limits**: Max 5 avatars per user (configurable)
2. **Garment Limits**: Max 100 user-uploaded garments (configurable)
3. **Try-On History**: Keep 30 days for free users, unlimited for premium
4. **Privacy**: Public content discoverable, private content only visible to user/friends
5. **Content Moderation**: All public content subject to review 