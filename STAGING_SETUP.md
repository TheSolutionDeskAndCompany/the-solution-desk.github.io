# Staging Environment Setup Guide

This guide helps you configure and test the complete authentication flow between your deployed frontend (Netlify) and backend (Render).

## 1. Environment Configuration

### Frontend (Netlify) Environment Variables

In your Netlify dashboard → **Site settings → Build & deploy → Environment variables**, add:

```bash
# Required for API communication
REACT_APP_API_URL=https://ow-backend.onrender.com

# Optional auth-related configuration
REACT_APP_JWT_EXPIRES=3600
```

### Backend (Render) Environment Variables

In your Render dashboard → **Environment**, ensure you have:

```bash
# JWT Configuration (REQUIRED)
JWT_SECRET_KEY=your-secure-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration (REQUIRED for frontend communication)
CORS_ORIGINS=https://your-netlify-domain.netlify.app,https://your-custom-domain.com

# Database (if using external database)
DATABASE_URL=your-database-url-here

# Flask Environment
FLASK_ENV=production
```

## 2. Manual Smoke Test Checklist

### Step 1: User Registration
- [ ] Navigate to your staging frontend URL
- [ ] Click "Sign up" or navigate to `/register`
- [ ] Fill in email and password (meeting validation requirements)
- [ ] Submit form
- [ ] ✅ **Expected**: Success toast + redirect to `/dashboard`
- [ ] ✅ **Expected**: JWT token stored in localStorage (check DevTools → Application → Local Storage)

### Step 2: User Logout
- [ ] Click "Logout" button
- [ ] ✅ **Expected**: Logout toast message
- [ ] ✅ **Expected**: Token removed from localStorage
- [ ] ✅ **Expected**: Redirect to home/login page

### Step 3: User Login
- [ ] Navigate to `/login`
- [ ] Enter the credentials you just registered with
- [ ] Submit form
- [ ] ✅ **Expected**: Success toast + redirect to `/dashboard`
- [ ] ✅ **Expected**: New JWT token in localStorage

### Step 4: Protected API Access
- [ ] Open DevTools → Network tab
- [ ] Navigate to a protected route or trigger an API call
- [ ] ✅ **Expected**: `Authorization: Bearer <token>` header present
- [ ] ✅ **Expected**: 200 OK response (not 401 Unauthorized)
- [ ] ✅ **Expected**: No CORS errors in console

### Step 5: Token Expiry Handling
- [ ] In DevTools → Application → Local Storage, manually edit the token to an invalid value
- [ ] Refresh the page or make an API call
- [ ] ✅ **Expected**: Automatic redirect to login page
- [ ] ✅ **Expected**: "Session expired" toast message

## 3. Automated E2E Testing

### Run Tests Locally Against Staging

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies if not already done
npm install

# Run tests against staging (interactive mode)
STAGING_FRONTEND_URL=https://your-netlify-domain.netlify.app \
STAGING_BACKEND_URL=https://ow-backend.onrender.com \
node scripts/test-staging.js

# Run tests in headless mode (CI-style)
STAGING_FRONTEND_URL=https://your-netlify-domain.netlify.app \
STAGING_BACKEND_URL=https://ow-backend.onrender.com \
node scripts/test-staging.js --headless
```

### Available Test Scripts

```bash
# Local development testing
npm run cy:open

# Local headless testing
npm run cy:run

# Staging environment testing (interactive)
npm run test:staging

# Staging environment testing (headless)
npm run test:staging:ci
```

## 4. GitHub Secrets Configuration

In your GitHub repository → **Settings → Secrets and variables → Actions**, add:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secure-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Staging URLs for E2E testing
STAGING_FRONTEND_URL=https://your-netlify-domain.netlify.app
STAGING_BACKEND_URL=https://ow-backend.onrender.com

# Optional: Codecov token for coverage reporting
CODECOV_TOKEN=your-codecov-token-here

# Optional: Netlify tokens for deployment
NETLIFY_AUTH_TOKEN=your-netlify-auth-token
NETLIFY_SITE_ID=your-netlify-site-id
```

## 5. Troubleshooting Common Issues

### CORS Errors
- **Problem**: `Access to fetch at 'https://ow-backend.onrender.com' from origin 'https://your-netlify-domain.netlify.app' has been blocked by CORS policy`
- **Solution**: Add your Netlify domain to `CORS_ORIGINS` in Render environment variables

### 401 Unauthorized Errors
- **Problem**: API calls return 401 even with valid token
- **Solution**: Check that `JWT_SECRET_KEY` is the same in both CI and Render environments

### Token Not Persisting
- **Problem**: User gets logged out on page refresh
- **Solution**: Verify localStorage is working and AuthContext is properly initialized

### Environment Variables Not Loading
- **Problem**: `process.env.REACT_APP_API_URL` is undefined
- **Solution**: Ensure environment variables are prefixed with `REACT_APP_` and rebuild the frontend

## 6. Network Debugging

Use browser DevTools to verify:

1. **Request Headers**: `Authorization: Bearer <token>` is present
2. **Response Headers**: No CORS errors
3. **Status Codes**: 200/201 for success, appropriate error codes for failures
4. **Request/Response Bodies**: Proper JSON format

## 7. Success Criteria

Your staging environment is properly configured when:

- ✅ Users can register new accounts
- ✅ Users can log in with valid credentials
- ✅ Users get appropriate error messages for invalid credentials
- ✅ Protected routes require authentication
- ✅ API calls include proper Authorization headers
- ✅ No CORS errors in browser console
- ✅ Token expiry is handled gracefully
- ✅ Logout clears authentication state

## 8. Next Steps

Once staging is verified:
1. Set up production environment with same configuration
2. Configure custom domain DNS
3. Set up monitoring and error tracking
4. Configure backup and disaster recovery procedures
