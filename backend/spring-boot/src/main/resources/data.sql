-- Initial Garment Categories Data
-- Clear any existing data first
DELETE FROM garment_categories;

-- Top Level Categories
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(1, 'Clothing', 'clothing', NULL, 'All types of clothing and apparel', 1, true, NOW(), NOW()),
(2, 'Accessories', 'accessories', NULL, 'Fashion accessories and add-ons', 2, true, NOW(), NOW()),
(3, 'Footwear', 'footwear', NULL, 'Shoes, boots, sneakers and all footwear', 3, true, NOW(), NOW()),
(4, 'Swimwear', 'swimwear', NULL, 'Swimsuits, bikinis, and beach wear', 4, true, NOW(), NOW()),
(5, 'Underwear', 'underwear', NULL, 'Undergarments and intimate wear', 5, true, NOW(), NOW());

-- Clothing Subcategories - Tops
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(10, 'Tops', 'tops', 1, 'All types of tops and upper body wear', 1, true, NOW(), NOW()),
(11, 'T-Shirts', 't-shirts', 10, 'Casual t-shirts and tees', 1, true, NOW(), NOW()),
(12, 'Shirts', 'shirts', 10, 'Formal and casual shirts', 2, true, NOW(), NOW()),
(13, 'Blouses', 'blouses', 10, 'Women blouses and feminine tops', 3, true, NOW(), NOW()),
(14, 'Tank Tops', 'tank-tops', 10, 'Sleeveless tops and tank tops', 4, true, NOW(), NOW()),
(15, 'Hoodies', 'hoodies', 10, 'Hooded sweatshirts and hoodies', 5, true, NOW(), NOW()),
(16, 'Sweaters', 'sweaters', 10, 'Knit sweaters and pullovers', 6, true, NOW(), NOW());

-- Clothing Subcategories - Bottoms
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(20, 'Bottoms', 'bottoms', 1, 'All types of bottoms and lower body wear', 2, true, NOW(), NOW()),
(21, 'Jeans', 'jeans', 20, 'Denim jeans and jean wear', 1, true, NOW(), NOW()),
(22, 'Pants', 'pants', 20, 'Trousers, chinos, and formal pants', 2, true, NOW(), NOW()),
(23, 'Shorts', 'shorts', 20, 'Short pants and casual shorts', 3, true, NOW(), NOW()),
(24, 'Skirts', 'skirts', 20, 'All types of skirts', 4, true, NOW(), NOW()),
(25, 'Leggings', 'leggings', 20, 'Leggings and yoga pants', 5, true, NOW(), NOW());

-- Clothing Subcategories - Dresses
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(30, 'Dresses', 'dresses', 1, 'All types of dresses', 3, true, NOW(), NOW()),
(31, 'Casual Dresses', 'casual-dresses', 30, 'Everyday and casual dresses', 1, true, NOW(), NOW()),
(32, 'Formal Dresses', 'formal-dresses', 30, 'Evening and formal dresses', 2, true, NOW(), NOW()),
(33, 'Summer Dresses', 'summer-dresses', 30, 'Light summer and sundresses', 3, true, NOW(), NOW());

-- Clothing Subcategories - Outerwear
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(40, 'Outerwear', 'outerwear', 1, 'Jackets, coats, and outer layers', 4, true, NOW(), NOW()),
(41, 'Jackets', 'jackets', 40, 'All types of jackets', 1, true, NOW(), NOW()),
(42, 'Coats', 'coats', 40, 'Winter coats and long outerwear', 2, true, NOW(), NOW()),
(43, 'Blazers', 'blazers', 40, 'Formal blazers and suit jackets', 3, true, NOW(), NOW());

-- Accessories Subcategories
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(50, 'Bags', 'bags', 2, 'Handbags, backpacks, and purses', 1, true, NOW(), NOW()),
(51, 'Jewelry', 'jewelry', 2, 'Necklaces, earrings, and accessories', 2, true, NOW(), NOW()),
(52, 'Hats', 'hats', 2, 'Caps, beanies, and headwear', 3, true, NOW(), NOW()),
(53, 'Belts', 'belts', 2, 'Leather and fabric belts', 4, true, NOW(), NOW()),
(54, 'Scarves', 'scarves', 2, 'Scarves and neck accessories', 5, true, NOW(), NOW()),
(55, 'Watches', 'watches', 2, 'Wrist watches and timepieces', 6, true, NOW(), NOW());

-- Footwear Subcategories
INSERT INTO garment_categories (id, name, slug, parent_id, description, sort_order, is_active, created_at, updated_at) VALUES
(60, 'Sneakers', 'sneakers', 3, 'Athletic and casual sneakers', 1, true, NOW(), NOW()),
(61, 'Boots', 'boots', 3, 'All types of boots', 2, true, NOW(), NOW()),
(62, 'Heels', 'heels', 3, 'High heels and dress shoes', 3, true, NOW(), NOW()),
(63, 'Flats', 'flats', 3, 'Flat shoes and ballet flats', 4, true, NOW(), NOW()),
(64, 'Sandals', 'sandals', 3, 'Open-toe sandals and summer shoes', 5, true, NOW(), NOW()); 