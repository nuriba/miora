# Miora Design System & Implementation Guide

## 🎨 Design Foundation

### Brand Colors
```css
Primary Gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Secondary Gradients:
  - Success: linear-gradient(135deg, #a8e6cf, #88d8a3)
  - Warning: linear-gradient(135deg, #ffd93d, #ff6b6b)
  - Error: linear-gradient(135deg, #ff6b6b, #ee5a24)
  - Neutral: linear-gradient(135deg, #f5f7fa, #c3cfe2)

Base Colors:
  - White: #ffffff
  - Light Gray: #f8f9fa
  - Medium Gray: #e9ecef
  - Dark Gray: #333333
  - Text Primary: #333333
  - Text Secondary: #666666
  - Text Muted: #999999
```

### Typography
```css
Font Family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif

Font Sizes:
  - Hero Title: clamp(3rem, 8vw, 6rem)
  - Section Title: 3rem
  - Subsection Title: 1.8rem
  - Card Title: 1.5rem
  - Body Large: 1.3rem
  - Body: 1rem
  - Body Small: 0.9rem

Font Weights:
  - Light: 300
  - Regular: 400
  - Medium: 500
  - Semibold: 600
  - Bold: 700
```

### Spacing System
```css
Spacing Scale (rem):
  - xs: 0.25rem (4px)
  - sm: 0.5rem (8px)
  - md: 1rem (16px)
  - lg: 1.5rem (24px)
  - xl: 2rem (32px)
  - 2xl: 3rem (48px)
  - 3xl: 4rem (64px)
  - 4xl: 6rem (96px)
  - 5xl: 8rem (128px)

Component Padding:
  - Buttons: 0.75rem 2rem
  - Cards: 2rem - 3rem
  - Sections: 4rem - 8rem vertical
  - Containers: 2rem horizontal
```

### Border Radius
```css
Border Radius Scale:
  - Small: 10px (form elements, small cards)
  - Medium: 15px (cards, panels)
  - Large: 20px (hero cards, major sections)
  - Pill: 50px (buttons, tags)
  - Circle: 50% (avatars, icon buttons)
```

---

## 📱 Landing Page Design Components

### 1. Navigation Bar
```
Layout: Fixed top navigation
Background: rgba(255, 255, 255, 0.95) with backdrop-filter: blur(10px)
Height: 80px
Content: Logo (left) + Navigation links (center) + Auth buttons (right)

Elements:
✓ Logo: Gradient text "Miora" (2rem, bold)
✓ Nav Links: Features, How It Works, Pricing, Demo
✓ Sign In Button: Outline style, white border
✓ Get Started Button: Primary gradient background
✓ Mobile: Hamburger menu for responsive
```

### 2. Hero Section
```
Layout: Full viewport height (100vh)
Background: Primary gradient with subtle pattern overlay
Text: Center-aligned, white text

Elements:
✓ Hero Title: "Try Before You Buy" (6rem max, responsive)
✓ Subtitle: Value proposition (1.8rem, 80% opacity)
✓ CTA Buttons: "Start Your Virtual Wardrobe" + "Watch Demo"
✓ Hero Image/Animation: 3D avatar preview or demo video
✓ Scroll indicator: Subtle down arrow
```

### 3. Features Section
```
Layout: 6-column grid (2 columns on mobile)
Background: Light gradient (#f8f9fa to #ffffff)
Padding: 8rem vertical

Card Design:
✓ White background with shadow
✓ 3rem padding
✓ Icon: 4rem emoji or SVG
✓ Title: 1.5rem, bold
✓ Description: Body text, line-height 1.6
✓ Hover effect: translateY(-10px)

Featured Benefits:
1. 🎯 Perfect Fit Guarantee
2. 🔒 Privacy First
3. ✨ Realistic Simulation
4. 👥 Social Shopping
5. 📱 Cross-Platform
6. 🌐 Universal Compatibility
```

### 4. How It Works Section
```
Layout: 4-step horizontal flow
Background: Light gray (#f8f9fa)
Padding: 8rem vertical

Step Design:
✓ Circular number badge: 80px diameter, gradient background
✓ Step title: 1.3rem, bold
✓ Description: Body text
✓ Progressive connector lines between steps (desktop)

Steps:
1. Create Your Avatar
2. Import Clothes
3. Virtual Try-On
4. Shop & Share
```

### 5. Demo Section
```
Layout: Centered content
Background: White
Video/Demo Area: 800px max width, 16:9 aspect ratio

Elements:
✓ Section title: "See Miora in Action"
✓ Demo placeholder: Gradient background with play icon
✓ CTA button: "Try It Yourself"
✓ Feature callouts around demo area
```

### 6. Social Proof Section
```
Layout: Testimonial carousel or grid
Background: Subtle gradient

Elements:
✓ User testimonials with avatars
✓ Usage statistics: "10,000+ users", "90% accuracy"
✓ Brand logos of partners
✓ Star ratings and review snippets
```

### 7. Final CTA Section
```
Layout: Full-width banner
Background: Primary gradient
Text: White, center-aligned

Elements:
✓ Compelling headline: "Ready to Transform Your Shopping?"
✓ Subtitle: Social proof or urgency
✓ Primary CTA button: "Start Free Today"
✓ Secondary info: "No credit card required"
```

### 8. Footer
```
Layout: 4-column grid with bottom bar
Background: Dark (#333333)
Text: White/gray

Columns:
✓ Product: Features, How It Works, Pricing, API
✓ Company: About, Careers, Press, Contact
✓ Support: Help Center, Privacy, Terms, Security
✓ Connect: Social media links

Bottom Bar:
✓ Copyright notice
✓ Additional legal links
```

---

## 🏠 User Dashboard Design Components

### 1. Authenticated Navigation
```
Layout: Fixed top bar, 80px height
Background: White with subtle blur effect
Content: Logo + Navigation + User menu

Elements:
✓ Logo: Gradient text, same as landing
✓ Navigation: Try-On Studio, My Wardrobe, Community, Trending
✓ User Avatar: 40px circle with initials
✓ User Menu: Dropdown with profile, settings, sign out
✓ Notifications: Bell icon with badge
```

### 2. Three-Panel Layout
```
Main Container: Fixed height (calc(100vh - 80px))
Background: Primary gradient

Left Sidebar (280px):
✓ Avatar preview and edit button
✓ Quick wardrobe grid (2x2)
✓ Recent outfits list
✓ Scroll: Auto when content overflows

Center Viewport (Flex 1):
✓ 3D rendering area
✓ Gradient background for depth
✓ Floating controls at bottom

Right Panel (320px):
✓ Fit analysis
✓ Size recommendations
✓ Product information
✓ Action buttons
✓ Social sharing
```

### 3. Avatar Sidebar Components
```
Avatar Preview:
✓ Size: 200px height, full width
✓ Background: Subtle gradient
✓ 3D avatar placeholder or actual model
✓ Edit button: Full width, primary style

Quick Wardrobe:
✓ Grid: 2x2 layout
✓ Item cards: Square aspect ratio
✓ Background: Warm gradients
✓ Hover: Scale(1.05) effect
✓ Content: Emoji or thumbnail

Recent Outfits:
✓ List layout with thumbnails
✓ Item height: 48px
✓ Background: Light gray
✓ Hover: Darker background
✓ Text: Outfit name with emoji
```

### 4. 3D Viewport Design
```
Container: Full height, flex center
Background: Dynamic gradient based on lighting
3D Scene: WebGL canvas, full size

Avatar Display:
✓ Size: 300px width x 500px height
✓ Style: Outlined figure with subtle glow
✓ Poses: Standing, walking, casual positions
✓ Clothing: Realistic physics simulation

Controls Bar:
✓ Position: Bottom center, floating
✓ Background: White with blur effect
✓ Buttons: 50px circles, gradient background
✓ Icons: Rotate left/right, reset, pose, camera
✓ Spacing: 1rem between buttons
```

### 5. Fit Analysis Panel
```
Fit Score Card:
✓ Background: Dynamic based on score (green/yellow/red)
✓ Score: 2.5rem font size, bold
✓ Label: Descriptive text (Perfect Fit, Good Fit, etc.)
✓ Border radius: 15px
✓ Padding: 1.5rem

Size Recommendations:
✓ Layout: Horizontal flex
✓ Options: S, M, L buttons
✓ Recommended: Highlighted with primary gradient
✓ Others: Light border, white background
✓ Hover: Border color change

Product Information:
✓ Background: Light gray card
✓ Content: Image, title, description, price
✓ Price: Large, red accent color
✓ Discount: Green badge
✓ Layout: Stacked content
```

### 6. Action Buttons
```
Button Stack:
✓ Layout: Vertical flex, 1rem gap
✓ Full width buttons
✓ Height: 3rem minimum

Primary Actions:
✓ Add to Cart: Primary gradient
✓ Save Outfit: Secondary outline
✓ Find Similar: Secondary outline

Social Sharing:
✓ Layout: Horizontal flex, centered
✓ Buttons: 40px circles
✓ Platforms: Instagram, TikTok, Twitter, WhatsApp
✓ Colors: Platform-specific gradients
✓ Hover: Scale(1.1) effect
```

### 7. Floating Action Button
```
Position: Fixed bottom-right (2rem from edges)
Size: 60px diameter
Background: Primary gradient
Icon: Plus symbol, 1.5rem
Shadow: Large, colored shadow
Hover: Scale(1.1) effect
Purpose: Add new garment
```

---

## 🎭 Interactive States & Animations

### Button States
```css
Default: Base styling
Hover: translateY(-2px) + enhanced shadow
Active: translateY(0) + reduced shadow
Disabled: 50% opacity + no hover effects
Loading: Spinner animation inside button
```

### Card Interactions
```css
Default: Subtle shadow
Hover: translateY(-10px) + larger shadow
Selected: Border or background highlight
Loading: Skeleton animation or spinner overlay
```

### Page Transitions
```css
Landing to Dashboard: Fade transition (0.5s)
Section Changes: Slide animations (0.3s)
Modal Overlays: Scale up from center (0.2s)
Navigation: Smooth scroll behavior
```

### Loading States
```css
Avatar Generation: Progress bar + text updates
Garment Processing: Spinner in viewport
API Calls: Button loading states
Image Loading: Progressive blur effect
```

---

## 📱 Responsive Design Breakpoints

### Breakpoint Strategy
```css
Mobile: 320px - 767px
Tablet: 768px - 1023px
Desktop: 1024px - 1439px
Large Desktop: 1440px+

Grid Adjustments:
Mobile: Single column layouts
Tablet: Simplified 2-column grids
Desktop: Full 3-panel layout
Large: Enhanced spacing and sizing
```

### Mobile Adaptations
```
Landing Page:
✓ Hero: Reduced text size, stacked CTAs
✓ Features: Single column grid
✓ Navigation: Hamburger menu
✓ Footer: Stacked columns

Dashboard:
✓ Layout: Vertical stack (sidebar > viewport > panel)
✓ Sidebar: Collapsed by default, slide-out menu
✓ Viewport: Reduced height (60vh)
✓ Controls: Larger touch targets
✓ Panel: Bottom sheet or accordion
```

---

## 🔧 Technical Implementation Notes

### CSS Framework Recommendations
```
Base: Tailwind CSS or Styled Components
3D: Three.js + React Three Fiber
Animations: Framer Motion or React Spring
Icons: Lucide React or Heroicons
```

### Component Architecture
```jsx
// Landing Page Structure
<LandingPage>
  <Navigation />
  <HeroSection />
  <FeaturesSection />
  <HowItWorksSection />
  <DemoSection />
  <CTASection />
  <Footer />
</LandingPage>

// Dashboard Structure
<Dashboard>
  <AuthenticatedNav />
  <MainLayout>
    <AvatarSidebar />
    <ViewportContainer>
      <ThreeJSCanvas />
      <ViewportControls />
    </ViewportContainer>
    <AnalysisPanel />
  </MainLayout>
  <FloatingActionButton />
</Dashboard>
```

### State Management
```javascript
// Authentication State
isAuthenticated: boolean
currentUser: User | null
authLoading: boolean

// Avatar State
avatars: Avatar[]
activeAvatar: Avatar | null
avatarLoading: boolean

// Try-On State
currentGarments: Garment[]
fitScore: number
sizeRecommendation: string
simulationLoading: boolean

// UI State
sidebarOpen: boolean
currentSection: string
notifications: Notification[]
```

### Performance Considerations
```
Loading Strategy:
✓ Critical CSS inline
✓ Progressive image loading
✓ 3D model streaming
✓ Component code splitting

Optimization:
✓ Image compression (WebP/AVIF)
✓ Font subsetting
✓ GPU acceleration for 3D
✓ Service worker caching
```

---

## 🎯 Key Success Metrics to Design For

### Conversion Funnel
```
Landing Page → Sign Up: 15%+ conversion rate
Sign Up → Avatar Creation: 80%+ completion
Avatar → First Try-On: 90%+ engagement
Try-On → Save/Share: 60%+ action rate
Save → Purchase: 25%+ conversion
```

### User Experience Goals
```
Time to First Value: < 3 minutes
Avatar Creation: < 5 minutes
Garment Try-On: < 15 seconds
Page Load Speed: < 2 seconds
Mobile Usability: 95%+ task completion
```

### Accessibility Requirements
```
WCAG 2.1 AA Compliance:
✓ Color contrast ratios
✓ Keyboard navigation
✓ Screen reader support
✓ Focus indicators
✓ Alt text for images
✓ Semantic HTML structure
```

This design guide provides a comprehensive foundation for implementing Miora's interface while maintaining consistency, usability, and brand alignment throughout the entire user journey.