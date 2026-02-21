# 🚀 Enterprise Admin Dashboard - Access Guide

## Quick Access Links

### 🔐 Enterprise Admin Dashboard (NEW!)
```
http://localhost:8000/admin-dashboard-enhanced.html
```
**Features:** 12 advanced enterprise features including SLA monitoring, internal notes, AI override tracking, ticket merging, impersonation, and more!

### 📊 User Dashboard
```
http://localhost:8000/dashboard.html
```
**Note:** Admin users will see an "🔐 Enterprise Admin" link in the navigation menu.

### 🎫 Basic Admin Panel (Legacy)
```
http://localhost:8000/admin.html
```
**Note:** This page now shows an upgrade notice to the Enterprise Dashboard.

---

## Login Credentials

### Admin Account
- **Email:** admin@nexora.ai
- **Password:** admin123
- **Access:** Full enterprise admin features

### Test User Accounts
Create your own by signing up at:
```
http://localhost:8000/signup.html
```

---

## Navigation Paths

### From Login Page
1. Go to: http://localhost:8000/login.html
2. Login as admin (admin@nexora.ai / admin123)
3. You'll be redirected to: http://localhost:8000/dashboard.html
4. Click "🔐 Enterprise Admin" in the navigation menu
5. Or directly access: http://localhost:8000/admin-dashboard-enhanced.html

### From User Dashboard
1. Login as admin
2. Look for "🔐 Enterprise Admin" link in the top navigation
3. Click to access Enterprise Dashboard

### From Basic Admin Panel
1. Go to: http://localhost:8000/admin.html
2. See the upgrade notice banner
3. Click "Access Enterprise Dashboard →" button

---

## Enterprise Dashboard Sections

Once you're in the Enterprise Dashboard, you'll see 7 sections in the sidebar:

### 1. 📊 Overview
- Real-time statistics
- Ticket growth chart (30 days)
- Category distribution (pie chart)
- Priority breakdown (bar chart)

### 2. 🎫 Tickets
- Advanced ticket management
- Filters by status, priority, category
- Search functionality
- SLA status badges
- Click "View" to open ticket modal with 4 tabs

### 3. 👥 Users
- User management
- Activate/deactivate users
- View user statistics
- Impersonation capability

### 4. 📈 Analytics
- Comprehensive metrics
- AI accuracy tracking
- SLA breach rate
- Resolution time analysis

### 5. ⏱️ SLA Monitor
- View all breached tickets
- See overdue time
- Quick action buttons
- Real-time countdown

### 6. 📋 Audit Logs
- Complete action history
- Filter by admin/action/date
- IP address tracking
- Compliance tracking

### 7. ⚙️ Settings
- System configuration
- SLA hour settings
- AI threshold adjustment
- Feature toggles
- **Requires elevated privilege mode**

---

## Ticket Modal Tabs

When you click "View" on any ticket, you'll see 4 tabs:

### Details Tab
- Ticket information
- AI override badge (if applicable)
- Actions:
  - Override Category
  - Assign Ticket
  - Merge Ticket

### Timeline Tab
- Chronological event history
- Visual timeline with icons
- All ticket activities tracked

### Internal Notes Tab
- Add admin-only notes
- View all internal notes
- Delete your own notes
- Not visible to users

### User Context Tab
- User profile information
- User statistics
- Recent ticket history
- Impersonation button

---

## Key Features to Access

### 🔐 Elevated Privilege Mode
**Location:** Settings section
**How to access:**
1. Click "Settings" in sidebar
2. Click "Enter Elevated Privilege Mode"
3. Enter password: admin123
4. See 10-minute countdown timer

### 📝 Internal Notes
**Location:** Any ticket → Internal Notes tab
**How to access:**
1. Open any ticket
2. Click "Internal Notes" tab
3. Type note and click "Add Note"

### 🤖 AI Override
**Location:** Any ticket → Details tab
**How to access:**
1. Open any ticket
2. Click "Override Category" button
3. Enter new category

### ⏱️ SLA Status
**Location:** SLA Monitor section or ticket lists
**How to access:**
1. Click "SLA Monitor" in sidebar
2. View all breached tickets
3. Or see SLA badges on ticket lists

### 🔗 Ticket Merging
**Location:** Any ticket → Details tab
**How to access:**
1. Open source ticket
2. Click "Merge Ticket" button
3. Enter target ticket ID

### 👥 User Impersonation
**Location:** Any ticket → User Context tab
**How to access:**
1. Open any ticket
2. Click "User Context" tab
3. Click "Impersonate User" button
4. Confirm action

---

## Troubleshooting Access Issues

### Issue: Can't see Enterprise Admin link
**Solution:** 
- Ensure you're logged in as admin (admin@nexora.ai)
- Check that you're on the dashboard page
- Refresh the page

### Issue: 403 Forbidden error
**Solution:**
- Verify you're logged in as admin
- Check your JWT token is valid
- Try logging out and logging back in

### Issue: Page not loading
**Solution:**
- Verify both servers are running:
  - Backend: http://localhost:5000
  - Frontend: http://localhost:8000
- Check browser console for errors
- Clear browser cache

### Issue: Features not working
**Solution:**
- Check browser console for JavaScript errors
- Verify API endpoints are accessible
- Ensure database migration was successful

---

## Server Status Check

### Backend Server
```bash
# Should be running on port 5000
curl http://localhost:5000/api/health
```

### Frontend Server
```bash
# Should be running on port 8000
# Open in browser: http://localhost:8000
```

---

## Direct URL Reference

### Main Pages
- Landing: http://localhost:8000/landing.html
- Login: http://localhost:8000/login.html
- Signup: http://localhost:8000/signup.html
- Dashboard: http://localhost:8000/dashboard.html
- **Enterprise Admin: http://localhost:8000/admin-dashboard-enhanced.html**

### User Pages
- Create Ticket: http://localhost:8000/create-ticket.html
- My Tickets: http://localhost:8000/history.html
- Analytics: http://localhost:8000/analytics.html
- Profile: http://localhost:8000/profile.html

### Admin Pages
- Basic Admin: http://localhost:8000/admin.html
- **Enterprise Admin: http://localhost:8000/admin-dashboard-enhanced.html**

---

## Browser Recommendations

### Recommended Browsers
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Edge (latest)
- ✅ Safari (latest)

### Browser Settings
- Enable JavaScript
- Allow cookies
- Enable local storage
- Disable ad blockers (if issues occur)

---

## Quick Test Workflow

### 1. Access Enterprise Dashboard
```
http://localhost:8000/admin-dashboard-enhanced.html
```

### 2. Login as Admin
- Email: admin@nexora.ai
- Password: admin123

### 3. Explore Sections
- Click through all 7 sidebar sections
- View statistics and charts
- Check SLA monitor
- Review audit logs

### 4. Test Ticket Features
- Go to "Tickets" section
- Click "View" on any ticket
- Try all 4 tabs
- Add an internal note
- Check timeline

### 5. Try Elevated Privilege
- Go to "Settings"
- Enter elevated privilege mode
- Modify a setting
- Save changes

---

## Support & Documentation

### Documentation Files
- **Quick Start:** ENTERPRISE_QUICKSTART.md
- **Full Guide:** ENTERPRISE_ADMIN_GUIDE.md
- **What's New:** WHATS_NEW_ENTERPRISE.md
- **This Guide:** ENTERPRISE_ACCESS_GUIDE.md

### Need Help?
1. Check browser console for errors
2. Review audit logs for admin actions
3. Verify server status
4. Check documentation files

---

## Security Notes

### Access Control
- Only admin users can access enterprise features
- All admin actions are logged
- Elevated privilege required for sensitive operations
- Impersonation is time-limited and tracked

### Best Practices
- Don't share admin credentials
- Review audit logs regularly
- Use elevated privilege sparingly
- Exit impersonation immediately after use

---

**🎉 You're all set to use the Enterprise Admin Dashboard!**

**Built with ❤️ by Soundarya**
**NexoraAI Enterprise v2.0**
