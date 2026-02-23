# Notification Preferences System - Complete Guide

## Overview

The notification preferences system allows users to customize which types of notifications they want to receive. This is a fully functional feature that stores user preferences in the database and can be used by future notification systems (email, push notifications, etc.).

---

## How It Works

### 1. Database Structure

**Table: `notification_settings`**

Each user has one notification settings record linked via `user_id`.

**Fields:**
- `id` - Unique identifier (UUID)
- `user_id` - Foreign key to users table (unique, one-to-one relationship)
- `email_notifications` - Boolean (default: True) - Master switch for email notifications
- `ticket_status_updates` - Boolean (default: True) - Notifications when ticket status changes
- `critical_alerts` - Boolean (default: True) - Alerts for high-priority/critical tickets
- `weekly_summary` - Boolean (default: False) - Weekly activity summary emails
- `ai_insight_updates` - Boolean (default: True) - AI-powered insights and suggestions
- `created_at` - Timestamp when settings were created
- `updated_at` - Timestamp when settings were last modified

**Relationship:**
```python
# In User model
notification_settings = db.relationship('NotificationSettings', 
                                       backref='user', 
                                       uselist=False, 
                                       cascade='all, delete-orphan')
```

This creates a one-to-one relationship between User and NotificationSettings.

---

### 2. Backend Implementation

#### Location: `backend/routes/profile.py`

**Endpoint: GET `/api/profile`**
- Fetches user profile including notification settings
- Automatically creates notification settings if they don't exist
- Returns user data with nested notification_settings object

**Endpoint: PUT `/api/profile/notifications`**
- Updates notification preferences
- Creates settings record if it doesn't exist
- Validates boolean values
- Returns updated settings

**Code Flow:**
```python
@profile_bp.route('/profile/notifications', methods=['PUT'])
@token_required
def update_notifications():
    # 1. Get user from JWT token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # 2. Get or create notification settings
    settings = user.notification_settings
    if not settings:
        settings = NotificationSettings(user_id=user.id)
        db.session.add(settings)
    
    # 3. Update preferences from request
    data = request.get_json()
    if 'email_notifications' in data:
        settings.email_notifications = bool(data['email_notifications'])
    # ... (same for other fields)
    
    # 4. Save to database
    db.session.commit()
    
    return jsonify({'message': 'Preferences updated'})
```

---

### 3. Frontend Implementation

#### Location: `frontend/profile.html`

**UI Components:**

Each notification preference has:
- Toggle switch (checkbox styled as a switch)
- Title (e.g., "Email Notifications")
- Description (e.g., "Receive notifications via email")

**HTML Structure:**
```html
<div class="notification-item">
  <div class="notification-info">
    <h4>Email Notifications</h4>
    <p>Receive notifications via email</p>
  </div>
  <label class="toggle-switch">
    <input type="checkbox" id="emailNotifications">
    <span class="toggle-slider"></span>
  </label>
</div>
```

**Available Preferences:**

1. **Email Notifications** (`emailNotifications`)
   - Master switch for all email notifications
   - When OFF, user receives no emails

2. **Ticket Status Updates** (`ticketStatusUpdates`)
   - Notifications when ticket status changes (open → in_progress → resolved)
   - Useful for tracking ticket progress

3. **Critical Alerts** (`criticalAlerts`)
   - Immediate notifications for high-priority or critical tickets
   - Important for urgent issues

4. **Weekly Summary** (`weeklySummary`)
   - Weekly digest of ticket activity
   - Includes: tickets created, resolved, pending

5. **AI Insight Updates** (`aiInsightUpdates`)
   - AI-powered suggestions and insights
   - Pattern detection, optimization tips

---

### 4. JavaScript Implementation

#### Location: `frontend/js/profile.js`

**Loading Preferences:**

When the profile page loads:
```javascript
async function loadProfile() {
  const response = await api.getProfile();
  currentProfile = response.profile;
  
  // Load notification settings
  if (currentProfile.notification_settings) {
    const settings = currentProfile.notification_settings;
    document.getElementById('emailNotifications').checked = settings.email_notifications;
    document.getElementById('ticketStatusUpdates').checked = settings.ticket_status_updates;
    // ... (same for other toggles)
  }
}
```

**Auto-Save Feature:**

Preferences are saved automatically 500ms after toggling:
```javascript
// Setup event listeners for each toggle
const toggles = ['emailNotifications', 'ticketStatusUpdates', ...];
toggles.forEach(id => {
  const element = document.getElementById(id);
  if (element) {
    element.addEventListener('change', () => {
      // Debounce: wait 500ms before saving
      clearTimeout(window.notificationSaveTimeout);
      window.notificationSaveTimeout = setTimeout(saveNotifications, 500);
    });
  }
});
```

**Manual Save:**

Users can also click "Save Preferences" button:
```javascript
window.saveNotifications = async function() {
  const data = {
    email_notifications: document.getElementById('emailNotifications').checked,
    ticket_status_updates: document.getElementById('ticketStatusUpdates').checked,
    critical_alerts: document.getElementById('criticalAlerts').checked,
    weekly_summary: document.getElementById('weeklySummary').checked,
    ai_insight_updates: document.getElementById('aiInsightUpdates').checked
  };
  
  await api.updateNotifications(data);
  showToast('Notification preferences saved', 'success');
};
```

---

## User Flow

### Step-by-Step Process:

1. **User navigates to Profile page**
   - URL: `/profile.html`
   - Authentication required (redirects to login if not authenticated)

2. **Page loads user data**
   - JavaScript calls `api.getProfile()`
   - Backend fetches user + notification settings
   - If no settings exist, creates default settings
   - Returns data to frontend

3. **UI displays current preferences**
   - Toggle switches show current state (ON/OFF)
   - Each toggle reflects database value

4. **User changes a preference**
   - Clicks toggle switch
   - JavaScript detects `change` event
   - Starts 500ms countdown timer

5. **Auto-save triggers**
   - After 500ms of no changes
   - Collects all toggle states
   - Sends PUT request to `/api/profile/notifications`
   - Backend updates database
   - Shows success toast notification

6. **Manual save (optional)**
   - User clicks "Save Preferences" button
   - Immediately saves without waiting
   - Same API call as auto-save

---

## API Reference

### Get Profile (includes notification settings)

**Request:**
```http
GET /api/profile
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "profile": {
    "id": "user-uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "notification_settings": {
      "email_notifications": true,
      "ticket_status_updates": true,
      "critical_alerts": true,
      "weekly_summary": false,
      "ai_insight_updates": true
    }
  }
}
```

### Update Notification Preferences

**Request:**
```http
PUT /api/profile/notifications
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "email_notifications": true,
  "ticket_status_updates": false,
  "critical_alerts": true,
  "weekly_summary": true,
  "ai_insight_updates": false
}
```

**Response:**
```json
{
  "message": "Notification preferences updated successfully",
  "notification_settings": {
    "email_notifications": true,
    "ticket_status_updates": false,
    "critical_alerts": true,
    "weekly_summary": true,
    "ai_insight_updates": false
  }
}
```

---

## Testing the Feature

### Manual Testing Steps:

1. **Test Loading:**
   ```
   1. Login to the application
   2. Navigate to Profile page
   3. Scroll to "Notification Preferences" section
   4. Verify all toggles are displayed
   5. Check browser console for any errors
   ```

2. **Test Auto-Save:**
   ```
   1. Toggle "Email Notifications" OFF
   2. Wait 1 second
   3. Look for success toast: "Notification preferences saved"
   4. Refresh the page
   5. Verify toggle is still OFF
   ```

3. **Test Manual Save:**
   ```
   1. Toggle multiple preferences
   2. Click "Save Preferences" button immediately
   3. Verify success toast appears
   4. Refresh page to confirm changes persisted
   ```

4. **Test Database Persistence:**
   ```
   1. Change preferences
   2. Logout
   3. Login again
   4. Navigate to Profile
   5. Verify preferences are still as you set them
   ```

### Backend Testing (Python):

```python
# Test script: backend/test_notifications.py
import requests

BASE_URL = "http://localhost:5000/api"

# 1. Login
response = requests.post(f"{BASE_URL}/login", json={
    "email": "user@example.com",
    "password": "password123"
})
token = response.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Get current settings
response = requests.get(f"{BASE_URL}/profile", headers=headers)
print("Current settings:", response.json()["profile"]["notification_settings"])

# 3. Update settings
response = requests.put(f"{BASE_URL}/profile/notifications", 
    headers=headers,
    json={
        "email_notifications": False,
        "weekly_summary": True
    }
)
print("Update response:", response.json())

# 4. Verify update
response = requests.get(f"{BASE_URL}/profile", headers=headers)
print("Updated settings:", response.json()["profile"]["notification_settings"])
```

---

## Future Integration

### How to Use These Preferences:

When implementing actual notification sending (email, SMS, push):

```python
# Example: Sending ticket status update notification

def send_ticket_status_notification(user_id, ticket):
    user = User.query.get(user_id)
    settings = user.notification_settings
    
    # Check if user wants this type of notification
    if not settings or not settings.ticket_status_updates:
        return  # User opted out
    
    # Check master email switch
    if not settings.email_notifications:
        return  # User disabled all emails
    
    # Send the notification
    send_email(
        to=user.email,
        subject=f"Ticket #{ticket.id} status updated",
        body=f"Your ticket status changed to: {ticket.status}"
    )
```

### Integration Points:

1. **Ticket Status Changes** (`ticket_status_updates`)
   - Hook into `update_ticket` endpoint
   - Check preference before sending email

2. **Critical Alerts** (`critical_alerts`)
   - When ticket priority is "critical" or "high"
   - Send immediate notification if enabled

3. **Weekly Summary** (`weekly_summary`)
   - Cron job runs every Monday
   - Queries users where `weekly_summary = True`
   - Generates and sends summary email

4. **AI Insights** (`ai_insight_updates`)
   - When ML model detects patterns
   - Send suggestions if user opted in

---

## Troubleshooting

### Common Issues:

**1. Toggles not loading:**
- Check browser console for errors
- Verify API endpoint is accessible
- Check if user has notification_settings record

**2. Changes not saving:**
- Check network tab for failed requests
- Verify JWT token is valid
- Check backend logs for errors

**3. Settings reset after refresh:**
- Database not persisting changes
- Check database connection
- Verify commit() is called in backend

**4. Auto-save not working:**
- Check if event listeners are attached
- Verify setTimeout is not being cleared prematurely
- Check browser console for JavaScript errors

---

## Summary

✅ **Fully Functional**: The notification preferences system is complete and working
✅ **Database Backed**: All preferences are stored in PostgreSQL/SQLite
✅ **Auto-Save**: Changes save automatically after 500ms
✅ **Manual Save**: Users can also click "Save Preferences" button
✅ **Persistent**: Preferences survive logout/login cycles
✅ **Extensible**: Ready for integration with email/SMS/push notification systems

The system is production-ready and can be extended to actually send notifications based on user preferences!
