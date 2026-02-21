# 🚀 Enterprise Admin System - Quick Start Guide

## Prerequisites

✅ Database migrated successfully
✅ Backend server ready
✅ Frontend server ready

---

## Step 1: Start the Backend Server

```bash
cd backend
py app.py
```

**Expected Output:**
```
============================================================
NEXORAAI SUPPORT SUITE - BACKEND SERVER
============================================================
Server running on: http://localhost:5000
API Base URL: http://localhost:5000/api
Default Admin: admin@nexora.ai / admin123
============================================================
```

---

## Step 2: Start the Frontend Server

Open a new terminal:

```bash
cd frontend
python -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

---

## Step 3: Access Enterprise Admin Dashboard

Open your browser and navigate to:

```
http://localhost:8000/admin-dashboard-enhanced.html
```

### Login Credentials
- **Email:** admin@nexora.ai
- **Password:** admin123

---

## Step 4: Explore Enterprise Features

### 1. Overview Dashboard
- View real-time statistics
- See ticket growth chart (30 days)
- Analyze category and priority distributions

### 2. Ticket Management
- Click **"Tickets"** in sidebar
- Apply advanced filters
- Click **"View"** on any ticket to open modal

### 3. Ticket Modal Tabs

#### Details Tab
- View ticket information
- See AI override badge (if applicable)
- Actions:
  - **Override Category** - Change AI prediction
  - **Assign Ticket** - Assign to admin
  - **Merge Ticket** - Combine duplicates

#### Timeline Tab
- View chronological events
- See all ticket activities
- Track admin actions

#### Internal Notes Tab
- Add admin-only notes
- View all internal notes
- Delete your own notes

#### User Context Tab
- View user information
- See user statistics
- Access impersonation

### 4. SLA Monitoring
- Click **"SLA Monitor"** in sidebar
- View all breached tickets
- See overdue time for each
- Take immediate action

### 5. Audit Logs
- Click **"Audit Logs"** in sidebar
- Review all admin actions
- Filter by admin/action/date
- Track system changes

### 6. System Settings
- Click **"Settings"** in sidebar
- Click **"Enter Elevated Privilege Mode"**
- Enter password: `admin123`
- Modify SLA hours
- Adjust AI threshold
- Toggle features
- Click **"Save Settings"**

---

## Key Features to Try

### 🔐 Elevated Privilege Mode
1. Go to Settings
2. Click "Enter Elevated Privilege Mode"
3. Enter password
4. See 10-minute countdown timer
5. Modify system settings

### 📝 Internal Notes
1. Open any ticket
2. Go to "Internal Notes" tab
3. Type a note
4. Click "Add Note"
5. Note is admin-only (users can't see it)

### 🤖 AI Override
1. Open a ticket
2. Click "Override Category"
3. Enter new category (e.g., "Technical")
4. See "AI Overridden" badge
5. Check timeline for logged action

### ⏱️ SLA Status
1. Go to "SLA Monitor"
2. View breached tickets
3. See countdown timers on ticket list
4. Take action on critical breaches

### 🔗 Ticket Merging
1. Open source ticket
2. Click "Merge Ticket"
3. Enter target ticket ID
4. Confirm merge
5. Notes and timeline combined

### 👥 User Impersonation
1. Open ticket
2. Go to "User Context" tab
3. Click "Impersonate User"
4. Confirm action
5. View system as that user
6. Click "Exit Impersonation" to return

### 📊 Advanced Analytics
1. Go to "Analytics" section
2. View comprehensive metrics:
   - Total tickets
   - Resolved tickets
   - Average resolution time
   - AI accuracy
   - SLA breach rate

---

## Testing Workflow

### Create Test Ticket (as User)
1. Logout from admin
2. Login as regular user or signup
3. Go to "Create Ticket"
4. Fill in details
5. Submit ticket

### Manage Ticket (as Admin)
1. Login as admin
2. Go to Enterprise Dashboard
3. Find ticket in "Tickets" section
4. Click "View"
5. Try all features:
   - Add internal note
   - Override category
   - Check SLA status
   - View user context
   - Assign to yourself

---

## API Testing

### Test Elevated Privilege
```bash
curl -X POST http://localhost:5000/api/admin/verify-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"password":"admin123"}'
```

### Test User Context
```bash
curl http://localhost:5000/api/admin/ticket/TICKET_ID/user-context \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Internal Notes
```bash
curl -X POST http://localhost:5000/api/admin/ticket/TICKET_ID/internal-notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"note":"This is an internal note"}'
```

### Test SLA Status
```bash
curl http://localhost:5000/api/admin/ticket/TICKET_ID/sla-status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Advanced Analytics
```bash
curl http://localhost:5000/api/admin/advanced-analytics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Troubleshooting

### Issue: Can't access admin dashboard
**Solution:** Ensure you're logged in as admin (admin@nexora.ai)

### Issue: Elevated privilege not working
**Solution:** Check password is correct (admin123)

### Issue: Charts not displaying
**Solution:** Ensure Chart.js is loaded (check browser console)

### Issue: SLA badges showing "Loading..."
**Solution:** Check backend server is running and API is accessible

### Issue: Internal notes not saving
**Solution:** Verify you're logged in as admin with valid token

### Issue: Impersonation not working
**Solution:** Ensure target user is not an admin

---

## Next Steps

1. ✅ Explore all dashboard sections
2. ✅ Create test tickets
3. ✅ Try all admin features
4. ✅ Review audit logs
5. ✅ Configure system settings
6. ✅ Test SLA monitoring
7. ✅ Practice ticket merging
8. ✅ Use impersonation mode

---

## Documentation

- **Full Guide:** `ENTERPRISE_ADMIN_GUIDE.md`
- **Implementation:** `ENTERPRISE_IMPLEMENTATION_SUMMARY.md`
- **API Docs:** `API_DOCUMENTATION.md`

---

## Support

For issues:
1. Check browser console for errors
2. Verify backend server is running
3. Check audit logs for admin actions
4. Review database with `backend/view_db.py`

---

**🎉 You're all set! Enjoy the Enterprise Admin System!**

**Built with ❤️ by Soundarya**
