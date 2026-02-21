# Render.com Deployment Guide (Recommended)

## Why Render Instead of Vercel?

Render.com is perfect for your Flask + SQLite application:
- ✅ **Persistent SQLite database** (data doesn't reset)
- ✅ **File uploads work** (avatars persist)
- ✅ **No cold starts** (always running)
- ✅ **ML models supported** (no size limits)
- ✅ **Free tier available** (750 hours/month)
- ✅ **Easy deployment** (from GitHub)

## Quick Deployment Steps

### 1. Create Render Account
- Go to https://render.com
- Sign up with your GitHub account

### 2. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `SOUNDU19/Ticket_creation`
3. Configure the service:

**Basic Settings:**
- Name: `nexora-ticket-system`
- Region: Choose closest to you
- Branch: `main`
- Root Directory: `backend`
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

**Instance Type:**
- Free (or paid for better performance)

### 3. Add Environment Variables
Click "Environment" and add:
```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-random-jwt-secret-here
PYTHON_VERSION=3.11.3
```

### 4. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- You'll get a URL like: `https://nexora-ticket-system.onrender.com`

### 5. Deploy Frontend (Static Site)
1. Click "New +" → "Static Site"
2. Connect same repository
3. Configure:
   - Name: `nexora-frontend`
   - Root Directory: `frontend`
   - Build Command: (leave empty)
   - Publish Directory: `.`

### 6. Update Frontend Configuration
Update your frontend to use the Render backend URL:

In `frontend/js/config.js`, change:
```javascript
const API_BASE_URL = 'https://nexora-ticket-system.onrender.com/api';
```

Then push to GitHub:
```bash
git add frontend/js/config.js
git commit -m "Update API URL for Render deployment"
git push origin main
```

Both sites will auto-redeploy!

---

## Alternative: Single Service Deployment

Deploy both frontend and backend as one service:

### Step 1: Create Build Script
Create `build.sh` in root:
```bash
#!/bin/bash
cd backend
pip install -r requirements.txt
```

### Step 2: Create Start Script
Create `start.sh` in root:
```bash
#!/bin/bash
cd backend
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Step 3: Configure Render
- Root Directory: `.`
- Build Command: `bash build.sh`
- Start Command: `bash start.sh`

### Step 4: Serve Frontend from Flask
The Flask app already serves static files, so frontend will be accessible!

---

## Required Files for Render

### 1. Add Gunicorn to Requirements
Update `backend/requirements.txt`:
```
Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.5.2
Werkzeug==2.3.7
python-dotenv==1.0.0
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
joblib==1.3.2
gunicorn==21.2.0
```

### 2. Update CORS Configuration
In `backend/config.py`, add your Render URL:
```python
CORS_ORIGINS = [
    'http://localhost:8000',
    'https://nexora-ticket-system.onrender.com',
    'https://nexora-frontend.onrender.com'
]
```

### 3. Update Flask App for Production
In `backend/app.py`, ensure it works with Gunicorn:
```python
if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## Post-Deployment

### Access Your Application
- Backend API: `https://nexora-ticket-system.onrender.com/api`
- Frontend: `https://nexora-frontend.onrender.com`
- Health Check: `https://nexora-ticket-system.onrender.com/api/health`

### Default Admin Login
- Email: `admin@nexora.ai`
- Password: `admin123`

### Database Persistence
Your SQLite database will persist! Data won't be lost between deployments.

### File Uploads
Avatar uploads will work and persist in the `uploads/` directory.

---

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version matches (3.11.3)

### App Crashes
- Check logs in Render dashboard
- Verify environment variables are set
- Check database initialization

### CORS Errors
- Add your Render URLs to `CORS_ORIGINS` in `backend/config.py`
- Commit and push to trigger redeploy

### Database Not Initializing
- Check logs for database creation errors
- Verify `instance/` directory is created
- Database auto-creates on first run

---

## Free Tier Limitations

Render Free Tier:
- ⏰ 750 hours/month (enough for one service)
- 💤 Spins down after 15 minutes of inactivity
- 🐌 Cold start takes 30-60 seconds
- 💾 Limited disk space (512 MB)

**Upgrade to Paid ($7/month) for:**
- ✅ Always running (no cold starts)
- ✅ More disk space
- ✅ Better performance
- ✅ Custom domains

---

## Automatic Deployments

Render automatically redeploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Wait 2-3 minutes and your changes are live!

---

## Custom Domain (Optional)

1. Go to your Render service settings
2. Click "Custom Domain"
3. Add your domain (e.g., `nexora.yourdomain.com`)
4. Update DNS records as instructed
5. SSL certificate auto-generated!

---

## Monitoring

Render provides:
- 📊 Real-time logs
- 📈 Metrics (CPU, memory, requests)
- 🔔 Email alerts for crashes
- 📉 Performance graphs

Access from your service dashboard.

---

## Summary

**Render is the best choice for NexoraAI because:**
1. Full Flask support with persistent database
2. File uploads work out of the box
3. ML models load without issues
4. Free tier is generous
5. Auto-deploys from GitHub
6. No code changes needed

**Next Steps:**
1. Add `gunicorn` to `backend/requirements.txt`
2. Update CORS in `backend/config.py`
3. Push to GitHub
4. Deploy on Render
5. Update frontend API URL
6. Test and enjoy!

Need help with deployment? Let me know!
