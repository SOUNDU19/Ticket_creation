# Vercel Deployment Guide for NexoraAI

## Important Note About Vercel Limitations

⚠️ **Vercel has significant limitations for this project:**

1. **SQLite Database**: Vercel's serverless functions are stateless, so SQLite won't persist data between requests
2. **File Uploads**: User avatars and file uploads won't work on Vercel's free tier
3. **ML Models**: Large pickle files may exceed Vercel's size limits
4. **Cold Starts**: First request may be slow due to serverless function initialization

## Recommended Alternative: Render.com

For a full-stack Flask + SQLite application like NexoraAI, **Render.com** is a better choice:
- ✅ Persistent SQLite database
- ✅ File storage support
- ✅ No cold starts
- ✅ Free tier available
- ✅ Easy deployment from GitHub

See `RENDER_DEPLOYMENT_GUIDE.md` for Render deployment instructions.

---

## If You Still Want to Deploy on Vercel

### Prerequisites
1. GitHub account with your code pushed
2. Vercel account (sign up at https://vercel.com)
3. Understanding that database and uploads won't persist

### Files Created for Vercel
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `requirements.txt` - Python dependencies (root level)
- ✅ Updated `frontend/js/config.js` - Auto-detect environment

### Deployment Steps

#### 1. Push Changes to GitHub
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

#### 2. Deploy on Vercel

**Option A: Using Vercel Dashboard (Recommended)**
1. Go to https://vercel.com/new
2. Import your GitHub repository: `SOUNDU19/Ticket_creation`
3. Configure project:
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: `frontend`
4. Add Environment Variables:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = `your-secret-key-here` (generate a random string)
   - `JWT_SECRET_KEY` = `your-jwt-secret-here` (generate a random string)
5. Click "Deploy"

**Option B: Using Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

#### 3. Post-Deployment Configuration

After deployment, you'll get a URL like: `https://ticket-creation.vercel.app`

**Update CORS Settings:**
You'll need to update `backend/config.py` to allow your Vercel domain:
```python
CORS_ORIGINS = [
    'http://localhost:8000',
    'https://ticket-creation.vercel.app',  # Add your Vercel URL
    'https://*.vercel.app'  # Allow all Vercel preview deployments
]
```

Then commit and push:
```bash
git add backend/config.py
git commit -m "Update CORS for Vercel deployment"
git push origin main
```

Vercel will automatically redeploy.

### Known Issues on Vercel

1. **Database Resets**: SQLite database resets on every deployment
   - Solution: Use PostgreSQL with Vercel Postgres or external database

2. **File Uploads Don't Work**: Avatar uploads won't persist
   - Solution: Use Vercel Blob Storage or external storage (AWS S3, Cloudinary)

3. **ML Model Size**: model.pkl and vectorizer.pkl may be too large
   - Solution: Use external model hosting or reduce model size

4. **Cold Starts**: First request takes 5-10 seconds
   - Solution: Use Vercel Pro plan or switch to Render

### Troubleshooting

**Build Fails:**
- Check Vercel build logs
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

**API Returns 404:**
- Check `vercel.json` routes configuration
- Verify API paths start with `/api/`

**CORS Errors:**
- Add your Vercel domain to CORS_ORIGINS in `backend/config.py`
- Redeploy after updating

**Database Empty:**
- This is expected on Vercel - database resets on each deployment
- Consider using PostgreSQL instead

### Upgrading to PostgreSQL (Recommended for Production)

To make Vercel deployment viable, switch from SQLite to PostgreSQL:

1. Create Vercel Postgres database
2. Update `backend/config.py`:
```python
SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
```
3. Add environment variable in Vercel dashboard
4. Redeploy

### Alternative: Deploy Frontend Only on Vercel

Deploy only the frontend on Vercel and host the backend elsewhere:

1. Update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ]
}
```

2. Deploy backend on Render/Railway/Heroku
3. Update `frontend/js/config.js` with backend URL

---

## Summary

**For Development/Testing:**
- ✅ Use local setup (current setup works great)

**For Production Deployment:**
- ⭐ **Recommended**: Use Render.com (see RENDER_DEPLOYMENT_GUIDE.md)
- ⚠️ **Not Recommended**: Vercel (too many limitations for this stack)

**If You Must Use Vercel:**
- Switch to PostgreSQL database
- Use external file storage
- Accept cold start delays
- Consider frontend-only deployment

Need help with Render deployment instead? Let me know!
