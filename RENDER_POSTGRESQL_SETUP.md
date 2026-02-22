# Fix: Data Loss Issue on Render

## Problem
Your users and tickets disappear because Render's free tier uses ephemeral storage. When the service spins down and restarts, the SQLite database is lost.

## Solution
Use Render's free PostgreSQL database for persistent storage.

---

## Step-by-Step Setup

### 1. Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `nexora-db` (or any name you prefer)
   - **Database**: `nexora` (default is fine)
   - **User**: `nexora` (default is fine)
   - **Region**: Same as your web service (e.g., Oregon)
   - **Plan**: **Free** (0 GB storage, expires after 90 days but can be recreated)
4. Click **"Create Database"**
5. Wait 2-3 minutes for database creation

### 2. Get Database Connection String

1. Once created, click on your database
2. Scroll down to **"Connections"** section
3. Copy the **"Internal Database URL"** (starts with `postgres://`)
   - Example: `postgres://nexora:xxxxx@dpg-xxxxx-a/nexora`
4. Keep this URL handy

### 3. Connect Web Service to Database

1. Go to your web service: https://dashboard.render.com
2. Click on your service (ticket-creation-6 or similar)
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
6. Click **"Save Changes"**

### 4. Redeploy

1. The service will automatically redeploy
2. Watch the logs - you should see:
   ```
   ✓ Database tables created
   ✓ Admin user created: admin@nexora.ai / admin123
   ✅ Database initialized - Ready for real users!
   ```

### 5. Verify

1. Visit your app: https://ticket-creation-rho.vercel.app/landing.html
2. Sign up with a test account
3. Create some tickets
4. **Wait 20 minutes** (let Render spin down)
5. Visit the app again (it will spin up)
6. Login - **Your data should still be there!** ✅

---

## Alternative: Use Render Disk (Not Recommended for Free Tier)

If you don't want PostgreSQL, you can add a persistent disk:

1. Go to your web service settings
2. Scroll to **"Disks"**
3. Click **"Add Disk"**
4. Configure:
   - **Name**: `data`
   - **Mount Path**: `/data`
   - **Size**: 1 GB (minimum)
5. Update `backend/config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'sqlite:////data/nexora.db'
   ```

**Note**: Disks are NOT available on free tier. You need a paid plan ($7/month).

---

## Why PostgreSQL is Better

✅ **Persistent**: Data survives service restarts
✅ **Free**: Render provides free PostgreSQL (90 days, renewable)
✅ **Scalable**: Better performance for multiple users
✅ **Production-ready**: Industry standard database
✅ **Backups**: Render provides automatic backups (paid plans)

---

## Current Status

Your code is now ready for PostgreSQL. Just follow the steps above to:
1. Create PostgreSQL database
2. Add DATABASE_URL environment variable
3. Redeploy

Your data will persist forever! 🎉

---

## Troubleshooting

**Q: Database creation failed**
A: Try a different region or wait a few minutes and try again

**Q: Connection error after setup**
A: Make sure you copied the "Internal Database URL" not "External"

**Q: Old data is gone**
A: Unfortunately, data in SQLite is lost. Start fresh with PostgreSQL

**Q: Free PostgreSQL expires after 90 days**
A: You can create a new free database and migrate, or upgrade to paid plan ($7/month)

---

## Migration Script (If Needed)

If you want to migrate existing local data to PostgreSQL:

```bash
# Export from SQLite
sqlite3 backend/instance/nexora.db .dump > backup.sql

# Import to PostgreSQL (after setting up)
psql $DATABASE_URL < backup.sql
```

---

## Summary

**Before**: SQLite → Data lost on restart ❌
**After**: PostgreSQL → Data persists forever ✅

Follow the steps above to fix the data loss issue permanently!
