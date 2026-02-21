# Deployment Troubleshooting Guide

## "Unexpected JSON" Error During Signup

This error means the frontend is receiving HTML instead of JSON from the backend. Here's how to fix it:

### Step 1: Identify Your Deployment Platform

Where did you deploy your project?
- Vercel
- Render
- Railway
- Other

### Step 2: Check Backend URL

Open your deployed frontend in browser and press F12 (Developer Tools), then:

1. Go to Console tab
2. Look for the line: `API Base URL: ...`
3. Note the URL shown

### Step 3: Fix Based on Platform

#### If Deployed on Vercel:

**Problem**: Vercel needs both frontend and backend deployed together, or you need separate deployments.

**Solution A: Single Deployment (Recommended)**
Your `vercel.json` is already configured. Just make sure:
1. Both frontend and backend are in the same repo ✅
2. Vercel is building from the root directory
3. Check Vercel logs for build errors

**Solution B: Separate Deployments**
1. Deploy backend separately on Render/Railway
2. Get backend URL (e.g., `https://nexora-backend.onrender.com`)
3. Update `frontend/js/config.js`:

```javascript
} else if (window.location.hostname.includes('vercel.app')) {
  // Vercel deployment - use your backend URL
  API_BASE_URL = 'https://YOUR-BACKEND-URL.onrender.com/api';
}
```

#### If Deployed on Render:

**Problem**: Frontend and backend are separate services.

**Solution**: Update frontend config with backend URL

1. Find your backend URL from Render dashboard (e.g., `https://nexora-backend.onrender.com`)
2. Update `frontend/js/config.js`:

```javascript
} else if (window.location.hostname.includes('onrender.com')) {
  // Render deployment
  if (window.location.hostname.includes('backend')) {
    API_BASE_URL = '/api';
  } else {
    // Frontend is separate - UPDATE THIS WITH YOUR BACKEND URL
    API_BASE_URL = 'https://nexora-backend.onrender.com/api';
  }
}
```

3. Replace `nexora-backend.onrender.com` with your actual backend URL
4. Commit and push to GitHub
5. Render will auto-redeploy

### Step 4: Verify Backend is Running

Test your backend directly:

1. Open browser
2. Go to: `https://YOUR-BACKEND-URL/api/health`
3. You should see: `{"status": "healthy", "message": "NexoraAI API is running"}`

If you see an error or HTML page:
- Backend is not running correctly
- Check deployment logs
- Verify environment variables are set

### Step 5: Check CORS Configuration

If backend is running but signup still fails:

1. Open `backend/config.py`
2. Add your frontend URL to CORS_ORIGINS:

```python
CORS_ORIGINS = [
    'http://localhost:8000',
    'https://your-frontend.vercel.app',  # Add your frontend URL
    'https://your-frontend.onrender.com',  # Or Render URL
    'https://*.vercel.app',  # Allow all Vercel preview deployments
    'https://*.onrender.com'  # Allow all Render deployments
]
```

3. Commit and push
4. Wait for redeploy

---

## Quick Fix: Update API URL Manually

If you need a quick fix, update the API URL directly:

### Option 1: Edit config.js

In `frontend/js/config.js`, replace the entire API_BASE_URL section with:

```javascript
// API Configuration - MANUAL OVERRIDE
const API_BASE_URL = 'https://YOUR-ACTUAL-BACKEND-URL.com/api';
console.log('API Base URL:', API_BASE_URL);
```

Replace `YOUR-ACTUAL-BACKEND-URL.com` with your real backend URL.

### Option 2: Use Environment Variable (Vercel/Render)

**For Vercel:**
1. Go to Project Settings → Environment Variables
2. Add: `VITE_API_URL` = `https://your-backend-url.com/api`
3. Update `config.js` to use it:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
```

**For Render:**
1. Go to Environment tab
2. Add: `API_URL` = `https://your-backend-url.com/api`
3. Render will inject it automatically

---

## Testing Locally First

Before deploying, test locally to ensure everything works:

```bash
# Terminal 1: Start backend
cd backend
py app.py

# Terminal 2: Start frontend
cd frontend
py -m http.server 8000
```

Open http://localhost:8000 and test signup. If it works locally but not on deployment, it's a configuration issue.

---

## Common Deployment Issues

### 1. Backend Not Starting

**Symptoms:**
- 502 Bad Gateway
- Service Unavailable
- HTML error pages

**Solutions:**
- Check deployment logs
- Verify `requirements.txt` has all dependencies
- Ensure `gunicorn` is installed
- Check start command is correct: `gunicorn app:app`

### 2. Database Not Initializing

**Symptoms:**
- "Table doesn't exist" errors
- "No such column" errors

**Solutions:**
- Backend creates database automatically on first run
- Check logs for database creation messages
- Verify `instance/` directory is writable
- On Render, database persists; on Vercel, it doesn't

### 3. CORS Errors

**Symptoms:**
- "CORS policy" errors in browser console
- "Access-Control-Allow-Origin" errors

**Solutions:**
- Add frontend URL to `CORS_ORIGINS` in `backend/config.py`
- Redeploy backend
- Clear browser cache

### 4. ML Models Not Loading

**Symptoms:**
- "model.pkl not found" errors
- Prediction endpoint fails

**Solutions:**
- Ensure `backend/ml/model.pkl` and `vectorizer.pkl` are in repo
- Check file size limits (Vercel: 50MB, Render: no limit)
- Verify files are not in `.gitignore`

---

## Step-by-Step: Fix Your Deployment Now

### 1. Find Your Backend URL

Go to your deployment platform dashboard and find the backend URL.

### 2. Test Backend Health

Open: `https://YOUR-BACKEND-URL/api/health`

Expected response:
```json
{"status": "healthy", "message": "NexoraAI API is running"}
```

### 3. Update Frontend Config

Edit `frontend/js/config.js` and set your backend URL:

```javascript
// For Render deployment
} else if (window.location.hostname.includes('onrender.com')) {
  API_BASE_URL = 'https://YOUR-BACKEND-URL.onrender.com/api';
}
```

### 4. Commit and Push

```bash
git add frontend/js/config.js
git commit -m "Fix API URL for deployment"
git push origin main
```

### 5. Wait for Redeploy

Most platforms auto-redeploy on git push. Wait 2-3 minutes.

### 6. Test Signup Again

Open your deployed frontend and try signing up. Check browser console (F12) for any errors.

---

## Still Having Issues?

### Check These:

1. ✅ Backend is deployed and running
2. ✅ Backend health endpoint returns JSON
3. ✅ Frontend config has correct backend URL
4. ✅ CORS is configured with frontend URL
5. ✅ Environment variables are set
6. ✅ Database is initialized

### Get Help:

1. Check deployment logs for errors
2. Test API endpoints directly with Postman/curl
3. Check browser console for detailed error messages
4. Verify network tab shows correct API URLs

---

## Quick Reference: Deployment URLs

### Local Development:
- Frontend: http://localhost:8000
- Backend: http://localhost:5000/api

### Vercel:
- Frontend: https://your-project.vercel.app
- Backend: https://your-project.vercel.app/api (same domain)

### Render:
- Frontend: https://your-frontend.onrender.com
- Backend: https://your-backend.onrender.com/api (different domain)

### Railway:
- Frontend: https://your-frontend.up.railway.app
- Backend: https://your-backend.up.railway.app/api (different domain)

---

## Need More Help?

Share these details:
1. Which platform you deployed to
2. Your backend URL
3. Your frontend URL
4. Error message from browser console
5. Backend deployment logs

This will help diagnose the exact issue!
