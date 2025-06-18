# Miora Frontend Deployment Guide

## Production Deployment Checklist

### Frontend
- [ ] Update environment variables for production
- [ ] Build optimized production bundle
- [ ] Configure CDN for static assets
- [ ] Set up SSL certificates
- [ ] Configure CORS for production domain
- [ ] Enable service worker for PWA
- [ ] Set up error tracking (Sentry)
- [ ] Configure analytics (Google Analytics/Mixpanel)

### Backend Integration
- [ ] Verify API endpoints work
- [ ] Test WebSocket connections
- [ ] Validate file uploads
- [ ] Check CORS settings
- [ ] Test authentication flow

## Deployment Options

### 1. Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### 2. Netlify
```bash
# Build and deploy
npm run build
# Upload dist/ folder to Netlify
```

### 3. AWS S3 + CloudFront
```bash
# Build application
npm run build

# Sync to S3
aws s3 sync dist/ s3://miora-frontend --delete

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### 4. Docker Deployment
```bash
# Build Docker image
docker build -t miora-frontend .

# Run container
docker run -p 80:80 miora-frontend
```

## Environment Configuration

### Production (.env.production)
```env
VITE_API_URL=https://api.miora.com/api/v1
VITE_MEDIA_URL=https://cdn.miora.com
VITE_WEBSOCKET_URL=wss://api.miora.com/ws
VITE_SENTRY_DSN=your-sentry-dsn
VITE_GA_TRACKING_ID=your-ga-id
```

### Staging (.env.staging)
```env
VITE_API_URL=https://staging-api.miora.com/api/v1
VITE_MEDIA_URL=https://staging-cdn.miora.com
VITE_WEBSOCKET_URL=wss://staging-api.miora.com/ws
```

## Performance Optimization

- Enable gzip/brotli compression
- Configure CDN for static assets
- Optimize images with WebP
- Implement service worker
- Enable HTTP/2
- Use preload directives

## Security Configuration

- Configure Content Security Policy
- Enable HTTPS only
- Set security headers
- Validate all inputs
- Implement rate limiting

## Monitoring Setup

- Application performance monitoring
- Error tracking with Sentry
- Analytics with Google Analytics
- Uptime monitoring
- User session recording

## Post-Deployment Testing

- [ ] All pages load correctly
- [ ] Authentication flow works
- [ ] 3D features function properly
- [ ] Mobile responsiveness
- [ ] Performance benchmarks
- [ ] Security scan results 