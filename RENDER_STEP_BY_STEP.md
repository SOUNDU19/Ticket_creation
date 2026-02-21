# Render Deployment - Complete Step-by-Step Guide

## Step 1: Go to Render Website

1. Open your browser
2. Go to: **https://render.com**
3. Click **"Get Started"** or **"Sign Up"**

---

## Step 2: Sign Up / Sign In

1. Click **"Sign in with GitHub"** (easiest option)
2. Authorize Render to access your GitHub account
3. You'll be redirected to Render dashboard

---

## Step 3: Create New Web Service

1. On the Render dashboard, click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

---

## Step 4: Connect Your Repository

1. You'll see a list of your GitHub repositories
2. Find **"Ticket_creation"** in the list
3. Click **"Connect"** button next to it

**If you don't see your repo:**
- Click "Configure account" 
- Give Render access to your repositories
- Come back and refresh

---

## Step 5: Configure Your Service

Fill in these settings EXACTLY as shown:

### Basic Settings:

**Name:**
```
nexora-ticket-system
```
(or any name you like - this will be in your URL)

**Region:**
- Choose the one closest to you (e.g., "Oregon (US West)")

**Branch:**
```
main
```

**Root Directory:**
```
backend
```
⚠️ IMPORTANT: Type exactly "backend" (no slashes)

**Runtime:**
- Select **"Python 3"** from dropdown

---

### Build & Deploy Settings:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app:app
```

---

### Instance Type:

**Select:**
- **"Free"** (for testing)
- Or **"Starter"** ($7/month for always-on)

For now, choose **Free** to test.

---

## Step 6: Environment Variables (Optional)

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add these:

**Variable 1:**
- Key: `FLASK_ENV`
- Value: `production`

**Variable 2:**
- Key: `SECRET_KEY`
- Value: `your-secret-key-12345` (or any random string)

**Variable 3:**
- Key: `JWT_SECRET_KEY`
- Value: `your-jwt-secret-67890` (or any random string)

---

## Step 7: Create Web Service

1. Scroll to the bottom
2. Click the big blue **"Create Web Service"** button
3. Wait for deployment to start

---

## Step 8: Watch the Build

You'll see a logs screen showing:

```
==> Cloning from GitHub...
==> Installing dependencies...
==> Building...
==> Starting service...
```

This takes **3-5 minutes**. Watch for:

✅ "Build succeeded"
✅ "Your service is live"

---

## Step 9: Get Your URL

Once deployed, you'll see your URL at the top:

```
https://nexora-ticket-system.onrender.com
```

Copy this URL!

---

## Step 10: Test Your Deployment

### Test 1: Health Check
Open in browser:
```
https://your-service-name.onrender.com/api/health
```

Should see:
```json
{"status": "healthy", "message": "NexoraAI API is running"}
```

### Test 2: Try Signup
1. Go to your Vercel frontend: `https://ticket-creation-c1xe.vercel.app`
2. But first, update the API URL...

---

## Step 11: Update Frontend to Use Render Backend

Now we need to tell your Vercel frontend to use the Render backend.

I'll update the config file for you. Just tell me your Render URL!

---

## Troubleshooting

### If Build Fails:

**Check the error in logs:**

1. **"gunicorn: command not found"**
   - Make sure Root Directory is set to `backend`
   - Make sure Build Command is `pip install -r requirements.txt`

2. **"No module named 'flask'"**
   - Dependencies didn't install
   - Check that `requirements.txt` exists in backend folder

3. **"Port already in use"**
   - This shouldn't happen on Render
   - Try redeploying

### If Build Succeeds But App Doesn't Work:

1. Check the logs for errors
2. Make sure Start Command is `gunicorn app:app`
3. Try manual deploy: Settings → Manual Deploy → Deploy latest commit

---

## Quick Settings Summary

Copy these settings:

```
Name: nexora-ticket-system
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

---

## After Successful Deployment

Once your backend is live on Render, I'll help you:

1. ✅ Update your Vercel frontend to use the Render backend
2. ✅ Test signup/login
3. ✅ Test all features
4. ✅ Make sure everything works!

---

## Need Help?

If you get stuck at any step, tell me:
1. Which step you're on
2. What you see on screen
3. Any error messages

I'll help you through it!

---

## Ready to Start?

1. Go to https://render.com
2. Sign in with GitHub
3. Follow the steps above
4. Tell me when you reach Step 9 (got your URL)!

Let's get your app deployed! 🚀
