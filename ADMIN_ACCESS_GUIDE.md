# 🔐 NexoraAI Admin Panel Access Guide

## 📋 Quick Access Steps

### Step 1: Make Sure Servers Are Running

Check if both servers are running:
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:8000

If not running, start them:
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd frontend
python -m http.server 8000
```

---

### Step 2: Open Login Page

**Option A: Direct URL**
```
http://localhost:8000/login.html
```

**Option B: From Landing Page**
1. Go to: http://localhost:8000/landing.html
2. Click "Get Started" or "Login" button

---

### Step 3: Login with Admin Credentials

**Default Admin Account:**
```
Email: admin@nexora.ai
Password: admin123
```

**Login Steps:**
1. Enter email: `admin@nexora.ai`
2. Enter password: `admin123`
3. Click "Login" button
4. You'll be redirected to the dashboard

---

### Step 4: Access Admin Panel

**Option A: Direct URL (After Login)**
```
http://localhost:8000/admin.html
```

**Option B: From Navigation**
1. After logging in, look at the top navigation bar
2. If you're logged in as admin, you'll see admin-specific links
3. Click on "Admin" or navigate to admin.html

---

## 🎯 Admin Panel Features

Once you're in the admin panel, you can:

### 📊 Dashboard Overview
- Total users count
- Total tickets count
- System statistics
- Recent activity

### 👥 User Management
- View all users
- See user roles (Admin/User)
- View user activity
- Manage user accounts

### 🎫 Ticket Management
- View all tickets from all users
- Filter by status, priority, category
- Update ticket status
- Assign tickets
- Bulk operations

### 📈 Analytics
- System-wide analytics
- User activity trends
- Ticket resolution metrics
- AI model performance

### ⚙️ Settings
- System configuration
- ML model settings
- Notification settings

---

## 🔍 Troubleshooting

### Problem: "Cannot access admin page"

**Solution 1: Check if logged in as admin**
```javascript
// Open browser console (F12) and run:
console.log(localStorage.getItem('user'));
// Should show role: "admin"
```

**Solution 2: Clear cache and login again**
```javascript
// Open browser console (F12) and run:
localStorage.clear();
// Then login again with admin credentials
```

**Solution 3: Verify admin account exists**
```bash
cd backend
python view_db.py users
# Should show admin@nexora.ai with role: ADMIN
```

---

### Problem: "Page redirects to login"

**Cause**: Not logged in or session expired

**Solution**:
1. Go to http://localhost:8000/login.html
2. Login with admin@nexora.ai / admin123
3. Then navigate to admin.html

---

### Problem: "Servers not running"

**Check Backend**:
```bash
# Try accessing:
http://localhost:5000/api/health
# Should return: {"status": "healthy"}
```

**Check Frontend**:
```bash
# Try accessing:
http://localhost:8000/landing.html
# Should load the landing page
```

**Restart Servers**:
```bash
# Stop any running servers (Ctrl+C)
# Then restart:

# Backend
cd backend
python app.py

# Frontend (new terminal)
cd frontend
python -m http.server 8000
```

---

## 📱 Complete Access Flow

```
1. Start Servers
   ↓
2. Open Browser → http://localhost:8000/login.html
   ↓
3. Enter Credentials
   Email: admin@nexora.ai
   Password: admin123
   ↓
4. Click Login
   ↓
5. Redirected to Dashboard
   ↓
6. Navigate to Admin Panel
   → http://localhost:8000/admin.html
   ↓
7. Access Admin Features ✅
```

---

## 🎨 Visual Guide

### Login Screen
```
┌─────────────────────────────────────┐
│         NexoraAI Login              │
├─────────────────────────────────────┤
│                                     │
│  Email:    [admin@nexora.ai      ] │
│                                     │
│  Password: [admin123             ] │
│                                     │
│         [  Login  ]                 │
│                                     │
└─────────────────────────────────────┘
```

### Admin Navigation
```
┌──────────────────────────────────────────────────┐
│ NexoraAI  Dashboard  Tickets  Users  Admin  ⚙️   │
└──────────────────────────────────────────────────┘
                                      ↑
                                Click here
```

---

## 🔑 Admin Credentials Summary

| Field    | Value              |
|----------|-------------------|
| Email    | admin@nexora.ai   |
| Password | admin123          |
| Role     | admin             |
| Access   | Full system access|

---

## 🚀 Quick Commands

### View Admin in Database
```bash
cd backend
python view_db.py users
```

### Check if Admin Exists
```bash
cd backend
python -c "import sqlite3; conn = sqlite3.connect('instance/nexora.db'); cursor = conn.cursor(); cursor.execute('SELECT name, email, role FROM users WHERE role=\"admin\"'); print(cursor.fetchall())"
```

### Reset Admin Password (if needed)
```bash
cd backend
python -c "from models import db; from models.user import User; from app import create_app; app = create_app(); app.app_context().push(); admin = User.query.filter_by(email='admin@nexora.ai').first(); admin.set_password('admin123'); db.session.commit(); print('Password reset!')"
```

---

## 📞 Need Help?

If you still can't access the admin panel:

1. **Check browser console** (F12) for errors
2. **Check backend logs** for authentication errors
3. **Verify servers are running** on correct ports
4. **Clear browser cache** and try again
5. **Check database** to confirm admin user exists

---

## ✅ Success Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 8000
- [ ] Can access login page
- [ ] Can login with admin@nexora.ai
- [ ] Can see admin navigation
- [ ] Can access admin.html
- [ ] Admin panel loads successfully

---

**Last Updated**: February 21, 2026
**Version**: 1.0
