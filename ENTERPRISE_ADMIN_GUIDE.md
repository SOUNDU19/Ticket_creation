# NexoraAI Enterprise Admin System Guide

## 🚀 Overview

The NexoraAI Enterprise Admin System is a comprehensive, production-grade administrative platform with advanced features for managing tickets, users, and system operations.

## 📋 Table of Contents

1. [Features](#features)
2. [Security](#security)
3. [Getting Started](#getting-started)
4. [Feature Documentation](#feature-documentation)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)

---

## ✨ Features

### 1. **Elevated Privilege Mode** 🔐
- Password re-confirmation required for sensitive operations
- 10-minute session timeout
- Visual countdown timer
- Required for:
  - User management
  - System settings changes
  - Ticket deletion
  - User impersonation

### 2. **User Context Panel** 👤
- Comprehensive user information display
- Real-time statistics:
  - Total tickets
  - Open tickets
  - High priority tickets
  - Average AI confidence
- Recent ticket history
- Quick access to user actions

### 3. **Internal Notes** 📝
- Admin-only private notes on tickets
- Not visible to end users
- Full CRUD operations
- Audit trail logging
- Timestamped with admin attribution

### 4. **Ticket Timeline** 📅
- Chronological activity view
- Tracks all ticket events:
  - Creation
  - AI categorization
  - Status changes
  - Priority changes
  - Admin actions
  - Merges
  - Resolution
- Visual timeline UI with icons

### 5. **AI Override Tracking** 🤖
- Track when admins override AI predictions
- Store original AI category
- Visual badges for overridden tickets
- Calculate AI accuracy metrics
- Audit logging for all overrides

### 6. **SLA Monitoring System** ⏱️
- Configurable SLA hours per priority:
  - Critical: 4 hours (default)
  - High: 24 hours (default)
  - Medium: 48 hours (default)
  - Low: 72 hours (default)
- Real-time SLA status calculation
- Breach detection and alerts
- Countdown timers
- SLA breach dashboard

### 7. **Ticket Merging** 🔗
- Merge duplicate tickets
- Combine internal notes
- Preserve timeline history
- Mark source ticket as merged
- Audit trail for merges

### 8. **Admin Impersonation Mode** 👥
- View system as any user
- 1-hour session limit
- Visual impersonation banner
- Cannot impersonate other admins
- Full audit logging
- Easy exit mechanism

### 9. **Advanced Analytics** 📊
- Ticket growth trends (30 days)
- Category distribution (pie chart)
- Priority breakdown (bar chart)
- Average resolution time
- SLA breach rate
- AI accuracy percentage
- Real-time Chart.js visualizations

### 10. **System Configuration Panel** ⚙️
- SLA hour configuration
- AI confidence threshold
- Duplicate detection toggle
- Auto-categorization settings
- Requires elevated privilege
- Full audit logging

### 11. **Comprehensive Audit Logging** 📋
- Log every admin action
- Filterable by:
  - Admin user
  - Action type
  - Date range
  - Target type
- IP address tracking
- JSON metadata storage
- Paginated results

### 12. **Ticket Assignment** 👨‍💼
- Assign tickets to specific admins
- Track assigned tickets
- Reassignment capability
- Audit trail

---

## 🔒 Security

### Role-Based Access Control (RBAC)
- All `/admin/*` endpoints require `role="admin"`
- Non-admin users blocked with 403 Forbidden
- JWT token validation on every request

### Elevated Privilege System
- Password re-confirmation for sensitive operations
- Time-limited elevated sessions (10 minutes)
- Automatic expiration
- Visual indicators

### Audit Trail
- Every admin action logged
- IP address tracking
- Timestamp precision
- Immutable log records

### Impersonation Safety
- Cannot impersonate admin users
- Time-limited sessions
- Clear visual indicators
- Full audit trail

---

## 🚀 Getting Started

### Access the Enterprise Admin Dashboard

1. **Login as Admin**
   ```
   URL: http://localhost:8000/login.html
   Email: admin@nexora.ai
   Password: admin123
   ```

2. **Navigate to Enterprise Dashboard**
   ```
   URL: http://localhost:8000/admin-dashboard-enhanced.html
   ```

### Dashboard Sections

- **Overview**: Key metrics and charts
- **Tickets**: Advanced ticket management
- **Users**: User management and impersonation
- **Analytics**: Detailed analytics and reports
- **SLA Monitor**: SLA breach tracking
- **Audit Logs**: Complete action history
- **Settings**: System configuration

---

## 📖 Feature Documentation

### Using Elevated Privilege Mode

1. Navigate to **Settings** section
2. Click **"Enter Elevated Privilege Mode"**
3. Enter your admin password
4. Elevated mode active for 10 minutes
5. Timer displayed in banner

### Managing Internal Notes

1. Open any ticket
2. Click **"Internal Notes"** tab
3. Type note in text area
4. Click **"Add Note"**
5. Notes visible only to admins
6. Delete your own notes anytime

### Viewing Ticket Timeline

1. Open any ticket
2. Click **"Timeline"** tab
3. View chronological events
4. Each event shows:
   - Icon
   - Title
   - Description
   - Timestamp

### Overriding AI Category

1. Open ticket details
2. Click **"Override Category"**
3. Enter new category
4. Original AI category preserved
5. Badge shows "AI Overridden"

### Monitoring SLA

1. Navigate to **SLA Monitor** section
2. View all breached tickets
3. See overdue time for each
4. Click **"View"** to take action
5. SLA badges on all ticket lists

### Merging Tickets

1. Open source ticket
2. Click **"Merge Ticket"**
3. Enter target ticket ID
4. Confirm merge
5. Notes and timeline combined
6. Source ticket marked as merged

### Impersonating Users

1. Open ticket or user list
2. Click **"Impersonate User"**
3. Confirm action
4. Redirected to user dashboard
5. Banner shows impersonation mode
6. Click **"Exit Impersonation"** to return

### Configuring System Settings

1. Navigate to **Settings**
2. Enter elevated privilege mode
3. Modify SLA hours
4. Adjust AI threshold
5. Toggle features
6. Click **"Save Settings"**

---

## 🔌 API Endpoints

### Elevated Privilege
```
POST /api/admin/verify-password
Body: { "password": "admin123" }
Response: { "elevated_token": "...", "expires_in": 600 }
```

### User Context
```
GET /api/admin/ticket/{ticket_id}/user-context
Response: { "user": {...}, "statistics": {...}, "recent_tickets": [...] }
```

### Internal Notes
```
GET /api/admin/ticket/{ticket_id}/internal-notes
POST /api/admin/ticket/{ticket_id}/internal-notes
Body: { "note": "Internal note text" }
DELETE /api/admin/ticket/{ticket_id}/internal-notes/{note_id}
```

### Timeline
```
GET /api/admin/ticket/{ticket_id}/timeline
Response: { "timeline": [{type, title, description, timestamp, icon}] }
```

### AI Override
```
PUT /api/admin/ticket/{ticket_id}/override-category
Body: { "category": "Technical" }
```

### SLA Status
```
GET /api/admin/ticket/{ticket_id}/sla-status
Response: { "sla": {status, deadline, time_remaining_hours, is_breached} }

GET /api/admin/sla-breaches
Response: { "breached_tickets": [...], "count": 5 }
```

### Ticket Merging
```
POST /api/admin/ticket/{ticket_id}/merge
Body: { "target_ticket_id": "uuid" }
```

### Impersonation
```
POST /api/admin/impersonate/{user_id}
Response: { "impersonation_token": "...", "user": {...} }

POST /api/admin/exit-impersonation
```

### Advanced Analytics
```
GET /api/admin/advanced-analytics
Response: {
  ticket_growth: [...],
  category_distribution: {...},
  priority_distribution: {...},
  avg_resolution_time_hours: 12.5,
  sla_breach_rate: 5.2,
  ai_accuracy: 95.8
}
```

### Ticket Assignment
```
PUT /api/admin/ticket/{ticket_id}/assign
Body: { "assignee_id": "admin_user_id" }
```

### Audit Logs
```
GET /api/admin/audit-logs?action=ticket_updated&page=1
Response: { "logs": [...], "total": 100, "pages": 5 }
```

### System Settings
```
GET /api/admin/settings
PUT /api/admin/settings
Body: {
  sla_critical_hours: 4,
  sla_high_hours: 24,
  sla_medium_hours: 48,
  sla_low_hours: 72,
  ai_confidence_threshold: 0.7,
  duplicate_detection_enabled: true
}
```

---

## 🗄️ Database Schema

### Updated Ticket Model
```python
- id (UUID)
- user_id (FK)
- title
- description
- category
- priority
- status
- ai_confidence
- original_ai_category (NEW)
- overridden_by_admin (FK, NEW)
- merged_into_ticket_id (FK, NEW)
- is_merged (Boolean, NEW)
- assigned_to (FK, NEW)
- created_at
- updated_at
- resolved_at (NEW)
```

### Internal Notes Model (NEW)
```python
- id (UUID)
- ticket_id (FK)
- admin_id (FK)
- note (Text)
- created_at
```

### System Settings Model (Enhanced)
```python
- id
- ai_confidence_threshold
- duplicate_detection_enabled
- sla_critical_hours (NEW)
- sla_high_hours (NEW)
- sla_medium_hours (NEW)
- sla_low_hours (NEW)
- updated_at
- updated_by (FK)
```

### Audit Log Model
```python
- id (UUID)
- admin_id (FK)
- action
- target_type
- target_id
- details (JSON)
- ip_address
- timestamp
```

---

## 🎨 UI Components

### Glassmorphism Design
- Dark theme with glass effects
- Purple (#a855f7) and Orange (#f97316) gradients
- Smooth animations
- Responsive layout

### Sidebar Navigation
- Fixed sidebar
- Active state indicators
- Icon + text labels
- Smooth transitions

### Timeline UI
- Vertical timeline with gradient line
- Icon badges for events
- Glass card content
- Chronological ordering

### SLA Badges
- Active (green): Within SLA
- Breached (red): SLA exceeded
- Pulsing animation for breaches
- Countdown timers

### Modal System
- Full-screen overlay
- Tabbed interface
- Smooth animations
- Responsive design

---

## 📊 Analytics & Reporting

### Available Charts
1. **Ticket Growth**: 30-day line chart
2. **Category Distribution**: Doughnut chart
3. **Priority Breakdown**: Bar chart

### Key Metrics
- Total tickets
- Resolved tickets
- Average resolution time
- AI accuracy percentage
- SLA breach rate
- Breached ticket count

---

## 🔧 Configuration

### SLA Configuration
Adjust SLA hours based on your business needs:
- Critical: 2-8 hours recommended
- High: 8-48 hours recommended
- Medium: 24-72 hours recommended
- Low: 48-168 hours recommended

### AI Threshold
- Default: 0.7 (70%)
- Range: 0.0 - 1.0
- Higher = stricter categorization
- Lower = more lenient

---

## 🚨 Best Practices

1. **Use Elevated Privilege Sparingly**
   - Only when needed
   - Re-authenticate frequently
   - Monitor audit logs

2. **Internal Notes Guidelines**
   - Be professional
   - Include context
   - Don't expose to users
   - Use for coordination

3. **SLA Management**
   - Review breaches daily
   - Adjust thresholds as needed
   - Escalate critical breaches
   - Track trends

4. **Impersonation Usage**
   - Only for troubleshooting
   - Limited duration
   - Document reason
   - Exit immediately after

5. **Audit Log Review**
   - Regular monitoring
   - Look for anomalies
   - Export for compliance
   - Retain for security

---

## 📞 Support

For issues or questions:
- Check audit logs for errors
- Review browser console
- Verify admin permissions
- Contact system administrator

---

## 🎓 Training Resources

### For New Admins
1. Start with Overview section
2. Practice with test tickets
3. Review audit logs
4. Learn SLA monitoring
5. Master internal notes

### For Power Users
1. Elevated privilege workflows
2. Advanced analytics interpretation
3. Ticket merging strategies
4. Impersonation best practices
5. System configuration optimization

---

**Built with ❤️ by Soundarya**
**NexoraAI Enterprise Admin System v2.0**
