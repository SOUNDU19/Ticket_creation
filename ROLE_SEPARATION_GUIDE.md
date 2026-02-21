# 🎭 Role Separation Guide - User vs Admin

## Overview

NexoraAI now has clear separation between User and Admin roles to maintain logical workflow and security.

---

## 👤 User Role

### Purpose
End users who need support and want to create/track tickets.

### Access
- Login: http://localhost:8000/login.html
- Dashboard: http://localhost:8000/dashboard.html

### Features Available
✅ Create tickets
✅ View their own tickets
✅ Track ticket status
✅ View personal analytics
✅ Update profile
✅ Manage notifications

### Navigation Menu
- Dashboard
- Create Ticket
- My Tickets
- Analytics
- Profile
- Logout

### What Users CANNOT Do
❌ Access admin panel
❌ View all tickets
❌ Manage other users
❌ Change system settings
❌ View audit logs
❌ Impersonate users

---

## 🔐 Admin Role

### Purpose
System administrators who manage tickets, users, and system operations.

### Access
- Login: http://localhost:8000/login.html (same as users)
- Admin Panel: http://localhost:8000/admin-dashboard-enhanced.html

### Features Available
✅ View all tickets
✅ Manage tickets (assign, merge, override)
✅ Add internal notes
✅ View user context
✅ Impersonate users
✅ Monitor SLA
✅ View audit logs
✅ Manage users
✅ Configure system settings
✅ View advanced analytics

### Navigation Menu (Admin Panel)
- Overview
- Tickets
- Users
- Analytics
- SLA Monitor
- Audit Logs
- Settings
- Logout

### What Admins CANNOT Do
❌ Create tickets (admins manage, not create)
❌ View "My Tickets" (admins see all tickets)
❌ Use user-specific features

---

## 🎯 Role-Based Behavior

### When Admin Logs In

**User Dashboard (dashboard.html):**
- Shows admin notice banner
- Hides "Create Ticket" button
- Hides user navigation items (Create Ticket, My Tickets, Analytics)
- Shows "🔐 Admin Panel" link
- Displays message: "Manage tickets and oversee system operations"

**Admin Panel (admin-dashboard-enhanced.html):**
- Full access to all admin features
- No user-specific features shown
- Clean admin-focused interface

### When User Logs In

**User Dashboard (dashboard.html):**
- Shows "Create Ticket" button
- Shows all user navigation items
- No admin panel link
- Displays message: "Track your tickets and manage your support requests"

**Admin Panel:**
- Access denied (403 Forbidden)
- Redirected to user dashboard

---

## 🔄 Workflow Examples

### User Workflow
1. Login → User Dashboard
2. Click "Create Ticket"
3. Fill ticket details
4. Submit ticket
5. View in "My Tickets"
6. Track status and updates

### Admin Workflow
1. Login → User Dashboard
2. See admin notice banner
3. Click "Go to Admin Panel"
4. View all tickets in system
5. Open ticket → See 4 tabs
6. Add internal notes
7. Assign to admin
8. Update status
9. Monitor SLA
10. Review audit logs

---

## 🚫 Logical Separation Rationale

### Why Admins Don't Create Tickets

**Reason 1: Role Clarity**
- Admins manage and resolve tickets
- Users create and submit tickets
- Clear separation of responsibilities

**Reason 2: Workflow Logic**
- Tickets represent user issues/requests
- Admins respond to tickets, not create them
- Maintains proper support workflow

**Reason 3: Audit Trail**
- Tickets should come from actual users
- Admin actions are tracked separately
- Clear accountability

**Reason 4: System Design**
- User dashboard = ticket creation
- Admin panel = ticket management
- Each interface optimized for its purpose

---

## 🔐 Security Implications

### Access Control
- **Frontend:** UI elements hidden/shown based on role
- **Backend:** API endpoints enforce role-based access
- **JWT:** Token contains role information
- **Validation:** Every admin endpoint checks role

### Protection Layers
1. **UI Layer:** Hide/show features based on role
2. **Route Layer:** Redirect unauthorized access
3. **API Layer:** Validate JWT and role
4. **Database Layer:** Audit all actions

---

## 📊 Feature Matrix

| Feature | User | Admin |
|---------|------|-------|
| Create Tickets | ✅ | ❌ |
| View Own Tickets | ✅ | ❌ |
| View All Tickets | ❌ | ✅ |
| Update Ticket Status | ❌ | ✅ |
| Add Internal Notes | ❌ | ✅ |
| Assign Tickets | ❌ | ✅ |
| Merge Tickets | ❌ | ✅ |
| Override AI Category | ❌ | ✅ |
| View User Context | ❌ | ✅ |
| Impersonate Users | ❌ | ✅ |
| Monitor SLA | ❌ | ✅ |
| View Audit Logs | ❌ | ✅ |
| Manage Users | ❌ | ✅ |
| System Settings | ❌ | ✅ |
| Personal Analytics | ✅ | ❌ |
| Profile Management | ✅ | ✅ |

---

## 🎨 UI Differences

### User Dashboard
- Bright, welcoming design
- "Create Ticket" CTA prominent
- Personal statistics
- Recent tickets view
- User-focused messaging

### Admin Panel
- Professional, data-focused design
- Sidebar navigation
- System-wide statistics
- All tickets view
- Admin-focused messaging

---

## 🔄 Role Switching

### Can Admins Act as Users?
**Yes, through impersonation:**
1. Admin opens ticket
2. Goes to "User Context" tab
3. Clicks "Impersonate User"
4. Views system as that user
5. Can create tickets as that user
6. Exits impersonation to return

### Why Impersonation?
- Troubleshoot user issues
- Test user experience
- Verify user-reported problems
- Maintain audit trail

---

## 📝 Best Practices

### For Admins
1. Use admin panel for all management tasks
2. Don't create tickets as admin
3. Use impersonation for testing only
4. Review audit logs regularly
5. Keep admin credentials secure

### For Users
1. Create tickets through user dashboard
2. Track tickets in "My Tickets"
3. Don't try to access admin features
4. Update profile as needed
5. Use analytics to track progress

---

## 🚀 Implementation Details

### Frontend Changes
- **dashboard.html:** Role-based UI rendering
- **admin-dashboard-enhanced.html:** Admin-only navigation
- **JavaScript:** Dynamic feature hiding/showing

### Backend Enforcement
- **@admin_required decorator:** Protects admin endpoints
- **JWT validation:** Checks role in token
- **RBAC:** Role-based access control throughout

---

## 🎯 Testing Role Separation

### Test as User
1. Signup new account
2. Login
3. Verify can create tickets
4. Verify cannot access admin panel
5. Check navigation shows user features

### Test as Admin
1. Login as admin@nexora.ai
2. Verify admin notice shows
3. Verify cannot create tickets from dashboard
4. Verify can access admin panel
5. Check navigation shows admin link only

---

## 📞 Common Questions

**Q: Why can't admins create tickets?**
A: Admins manage tickets, users create them. This maintains clear workflow and accountability.

**Q: What if admin needs to create a ticket?**
A: Use impersonation to act as a user, or have a separate user account.

**Q: Can a user become an admin?**
A: Yes, through database update or admin user management (if implemented).

**Q: Can admin see user analytics?**
A: Yes, through the "User Context" panel when viewing tickets.

**Q: Is role separation enforced on backend?**
A: Yes, all admin endpoints require admin role validation.

---

## ✅ Summary

**Clear Separation:**
- Users create and track tickets
- Admins manage and resolve tickets
- Each role has dedicated interface
- No feature mixing or confusion

**Benefits:**
- Logical workflow
- Clear responsibilities
- Better security
- Improved user experience
- Professional system design

---

**🎭 Role separation ensures NexoraAI operates like a professional enterprise system!**

**Built with ❤️ by Soundarya**
