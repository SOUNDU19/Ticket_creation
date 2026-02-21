# Quick Fix: Signup "Unexpected JSON" Error

## The Problem
You're getting "unexpected JSON" error during signup because the frontend can't reach the backend API.

## Quick Solution (3 Steps)

### Step 1: Find Your Backend URL

Where did you deploy? Check your deployment platform:

**If on Vercel:**
- Go to https://vercel.com/dashboard
- Click your project
- Copy the deployment URL (e.g., `https://ticket-creation.vercel.app`)

**If on Render:**
- Go to https://dashboard.render.com
- Find your backend service
- Copy the URL (e.g., `https://nexora-backend.onrender.com`)

### Step 2: Update Frontend Configuration

Open `frontend/js/config.js` and find this section (around line 3-20):

Replace the entire `API_BASE_URL` section with this simple version:

```javascript
// API Configuration - SIMPLE FIX
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000/api'
  : 'https://YOUR-BACKEND-URL-HERE/api';  // REPLACE THIS!

console.log('API Base URL:', API_BASE_URL);
```

**Important:** Replace `YOUR-BACKEND-URL-HERE` with your actual backend URL:

**Examples:**
- Vercel (same domain): Use `/api` instead
- Render: `https://nexora-backend.onrender.com/api`
- Railway: `https://nexora-backend.up.railway.app/api`

### Step 3: Push Changes

```bash
git add frontend/js/config.js
git commit -m "Fix API URL for deployment"
git push origin main
```

Your deployment will automatically update in 2-3 minutes.

---

## Test If Backend Is Working

Before fixing frontend, verify your backend is running:

1. Open browser
2. Go to: `https://YOUR-BACKEND-URL/api/health`
3. You should see:
```json
{"status": "healthy", "message": "NexoraAI API is running"}
```

**If you see an error or HTML page:**
- Your backend is not deployed correctly
- Check deployment logs
- Make sure you deployed the `backend` folder

---

## Platform-Specific Instructions

### Vercel (Single Deployment)

If you deployed everything to Vercel as one project:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000/api'
  : '/api';  // Use relative path
```

### Render (Separate Services)

If you have separate frontend and backend on Render:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000/api'
  : 'https://nexora-backend.onrender.com/api';  // Your backend URL
```

### Railway

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000/api'
  : 'https://your-backend.up.railway.app/api';  // Your backend URL
```

---

## Still Not Working?

### Check Browser Console

1. Open your deployed site
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Look for errors
5. Check what URL it's trying to call

### Common Issues:

**1. "Failed to fetch" or "NetworkError"**
- Backend is not running
- Wrong backend URL
- CORS not configured

**2. "404 Not Found"**
- API endpoint doesn't exist
- Wrong URL path
- Backend not deployed

**3. "500 Internal Server Error"**
- Backend is running but has errors
- Check backend logs
- Database might not be initialized

---

## Update CORS (If Needed)

If backend is running but you still get errors, update CORS:

Edit `backend/config.py`:

```python
CORS_ORIGINS = [
    'http://localhost:8000',
    'https://your-frontend-url.vercel.app',  # Add your frontend URL
    'https://*.vercel.app',  # Allow all Vercel deployments
    'https://*.onrender.com',  # Allow all Render deployments
]
```

Then commit and push:

```bash
git add backend/config.py
git commit -m "Update CORS configuration"
git push origin main
```

---

## Test Locally First

Make sure it works locally before deploying:

```bash
# Terminal 1: Backend
cd backend
py app.py

# Terminal 2: Frontend  
cd frontend
py -m http.server 8000
```

Open http://localhost:8000 and test signup. If it works locally, the issue is deployment configuration.

---

## What I Fixed

I've already updated your code with:

1. ✅ Better error handling in `frontend/js/api.js`
2. ✅ Improved API URL detection in `frontend/js/config.js`
3. ✅ Console logging to help debug
4. ✅ Better error messages

Now you just need to:
1. Find your backend URL
2. Update `frontend/js/config.js` with that URL
3. Push to GitHub
4. Wait for redeploy

---

## Example: Complete Fix

Here's a complete working example for Render deployment:

**frontend/js/config.js:**
```javascript
// API Configuration
let API_BASE_URL;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  API_BASE_URL = 'http://localhost:5000/api';
} else {
  // Production - use your actual backend URL
  API_BASE_URL = 'https://nexora-backend-abc123.onrender.com/api';
}

console.log('API Base URL:', API_BASE_URL);

// Rest of the file stays the same...
```

Replace `nexora-backend-abc123.onrender.com` with your actual backend URL!

---

## Need Help?

Tell me:
1. Where did you deploy? (Vercel/Render/Railway/Other)
2. What's your backend URL?
3. What's your frontend URL?
4. What error do you see in browser console (F12)?

I'll help you fix it!
