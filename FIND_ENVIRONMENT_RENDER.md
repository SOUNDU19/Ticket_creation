# How to Find Environment Variables in Render

## Method 1: Using Environment Tab (Recommended)

### Step-by-Step:

1. **Go to Render Dashboard**
   - Open: https://dashboard.render.com
   - Login if needed

2. **Click on Your Service**
   - You'll see a list of services
   - Click on "ticket-creation-6" (or your service name)

3. **Look at the LEFT SIDEBAR**
   - You should see a menu with these options:
     ```
     📊 Overview
     📅 Events  
     📝 Logs
     💻 Shell
     🔧 Environment  ← CLICK HERE
     ⚙️ Settings
     ```

4. **Add Environment Variable**
   - Click the blue **"Add Environment Variable"** button
   - Key: `DATABASE_URL`
   - Value: (paste your PostgreSQL URL)
   - Click **"Save Changes"**

---

## Method 2: Using Settings (Alternative)

If you don't see "Environment" in the sidebar:

1. Click **"Settings"** in the left sidebar
2. Scroll down the page
3. Look for section titled **"Environment Variables"**
4. Click **"Add Environment Variable"**
5. Add your variable

---

## Method 3: Using Blueprint (Easiest)

If the above methods don't work, use the render.yaml file:

1. I've already updated `render.yaml` in your project
2. Just commit and push:
   ```bash
   git add render.yaml
   git commit -m "Add PostgreSQL to render.yaml"
   git push origin main
   ```
3. Render will automatically:
   - Create PostgreSQL database
   - Connect it to your service
   - Set DATABASE_URL automatically

---

## What the Screen Should Look Like:

When you click on your service, you should see:

```
┌─────────────────────────────────────────────┐
│  ticket-creation-6                          │
├─────────────────────────────────────────────┤
│                                             │
│  [Left Sidebar]        [Main Content]      │
│  • Overview            Service Details      │
│  • Events              Status: Live         │
│  • Logs                                     │
│  • Shell                                    │
│  • Environment  ← HERE                      │
│  • Settings                                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Still Can't Find It?

### Option A: Create PostgreSQL Separately

1. Go to Render Dashboard
2. Click **"New +"** at the top
3. Select **"PostgreSQL"**
4. Create the database
5. Copy the "Internal Database URL"
6. Tell me the URL and I'll help you add it

### Option B: Use render.yaml (Automatic)

Just run these commands:
```bash
git add render.yaml
git commit -m "Add PostgreSQL"
git push origin main
```

Render will automatically create and connect the database!

---

## Need Help?

If you're still stuck:
1. Take a screenshot of your Render dashboard
2. Or tell me what you see on the screen
3. I'll guide you through it!
