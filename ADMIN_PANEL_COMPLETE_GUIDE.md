# Complete Admin Panel Guide - Simple Explanation

## Table of Contents
1. [Getting Started](#getting-started)
2. [Overview Section](#1-overview-section)
3. [Tickets Section](#2-tickets-section)
4. [Users Section](#3-users-section)
5. [Analytics Section](#4-analytics-section)
6. [SLA Monitoring](#5-sla-monitoring)
7. [Audit Logs](#6-audit-logs)
8. [Settings](#7-settings)

---

## Getting Started

### How to Access Admin Panel

1. **Open your browser** and go to: `http://localhost:8000/login.html`

2. **Click on "Admin Login" tab** (the one with 🔐 icon)

3. **Enter admin credentials:**
   - Email: `admin@nexora.ai`
   - Password: `admin123`

4. **Click "Sign In"**

5. You'll be automatically redirected to the **Enterprise Admin Dashboard**

---

## 1. Overview Section

**What is it?**
The first page you see when you login. It shows a quick summary of everything happening in the system.

### What You'll See:

#### A. Statistics Cards (Top of Page)
Six colorful cards showing:

1. **Total Tickets** 🎫
   - How many tickets exist in total
   - Example: "25 tickets"

2. **Resolved Tickets** ✅
   - How many tickets have been fixed
   - Example: "18 resolved"

3. **Average Resolution Time** ⏱️
   - How long it takes to fix tickets on average
   - Example: "4.5 hours"

4. **AI Accuracy** 🤖
   - How accurate the AI is at categorizing tickets
   - Example: "94.5%"

5. **SLA Breach Rate** 📊
   - Percentage of tickets that took too long to fix
   - Example: "5%"

6. **Breached Tickets** ⚠️
   - Number of tickets that missed their deadline
   - Example: "2 tickets"

#### B. Charts (Middle of Page)

1. **Ticket Growth Chart** (Line Graph)
   - Shows how many tickets were created each day
   - Helps you see if tickets are increasing or decreasing

2. **Category Distribution** (Pie Chart)
   - Shows what types of issues people report
   - Example: 40% Technical, 30% Billing, 20% Account, 10% General

3. **Priority Breakdown** (Bar Chart)
   - Shows how urgent tickets are
   - Example: 5 Critical, 10 High, 15 Medium, 5 Low

**Why is this useful?**
- Quick overview of system health
- Spot trends (are tickets increasing?)
- See which categories need more attention

---

## 2. Tickets Section

**What is it?**
The main workspace where you manage all support tickets.

### A. Ticket List (Table View)

You'll see a table with these columns:

1. **Ticket ID** - Unique identifier (like #0c300896)
2. **User** - Who created the ticket
3. **Title** - Brief description of the issue
4. **Category** - Type of issue (Technical, Billing, etc.)
5. **Priority** - How urgent (Critical, High, Medium, Low)
6. **Status** - Current state (Open, In Progress, Resolved, Closed)
7. **SLA Status** - Is it on time or overdue?
8. **Actions** - "View" button to see details

### B. Filters (Top of Table)

1. **Search Box** 🔍
   - Type keywords to find specific tickets
   - Searches in title and description

2. **Status Filter** 📋
   - Show only: Open, In Progress, Resolved, or Closed tickets
   - Or "All" to see everything

3. **Priority Filter** ⚡
   - Show only: Critical, High, Medium, or Low priority
   - Or "All" to see everything

**Example:** Filter by "Open" status and "High" priority to see urgent tickets that need attention.

### C. Viewing Ticket Details

**Click the "View" button** on any ticket to open a detailed modal with 4 tabs:

#### Tab 1: Details

**What you see:**
- Full ticket title and description
- Category, Priority, Status
- AI Confidence score
- If admin overrode AI's decision (shows warning)

**What you can do:**

1. **Update Ticket Status** (Purple Box)
   - Select new status from dropdown:
     - **Open**: Just created, not started yet
     - **In Progress**: Someone is working on it
     - **Resolved**: Issue is fixed
     - **Closed**: Completely done
   - Click "Update Status" button
   - Confirm the change
   - ✅ Status updates immediately!

2. **Override Category** Button
   - If AI got the category wrong
   - Click button, enter correct category
   - System remembers AI was overridden

3. **Assign Ticket** Button
   - Assign ticket to a specific admin
   - Helps distribute workload
   - Admin gets notified

4. **Merge Ticket** Button
   - If two tickets are about the same issue
   - Combine them into one
   - Keeps everything organized

#### Tab 2: Timeline

**What is it?**
A chronological history of everything that happened to this ticket.

**What you see:**
- When ticket was created
- When AI categorized it
- Every status change
- Every priority change
- Admin comments
- Who did what and when

**Example Timeline:**
```
🎫 Ticket Created - 2 hours ago
🤖 AI Categorized as "Technical" - 2 hours ago
🔄 Status changed to "In Progress" - 1 hour ago
✅ Status changed to "Resolved" - 10 minutes ago
```

**Why is this useful?**
- See complete ticket history
- Track who worked on it
- Understand what actions were taken

#### Tab 3: Internal Notes

**What is it?**
Private notes that only admins can see. Users never see these.

**What you can do:**
1. **Add a Note**
   - Type your note in the text box
   - Click "Add Note"
   - Note is saved with your name and timestamp

2. **View All Notes**
   - See notes from all admins
   - Each note shows who wrote it and when

3. **Delete Your Notes**
   - Click "Delete" button on your own notes
   - Can't delete other admins' notes

**Example Use Cases:**
- "Called customer, they confirmed issue is fixed"
- "This is related to ticket #abc123"
- "Need to follow up tomorrow"
- "Escalated to engineering team"

**Why is this useful?**
- Team communication
- Document actions taken
- Remember important details
- Coordinate with other admins

#### Tab 4: User Context

**What is it?**
Information about the user who created the ticket.

**What you see:**
- User's full name
- Email address
- Account creation date
- Last login time
- **Total tickets** they've created
- **Open tickets** they currently have
- **High priority tickets** count
- **Average AI confidence** for their tickets

**Why is this useful?**
- Understand user's history
- See if they're a frequent reporter
- Identify patterns
- Provide better support

---

## 3. Users Section

**What is it?**
Manage all users in the system.

### What You See:

A table with all users showing:
- Name
- Email
- Role (User or Admin)
- Status (Active or Inactive)
- Account created date
- Actions button

### What You Can Do:

1. **View User Details**
   - Click on any user
   - See their complete profile
   - View their ticket history

2. **Activate/Deactivate Users**
   - Click "Deactivate" to disable a user account
   - They won't be able to login
   - Click "Activate" to re-enable them

3. **Change User Role**
   - Promote user to admin
   - Demote admin to user
   - (If this feature is enabled)

**Why is this useful?**
- Manage user access
- Disable problematic accounts
- See who's using the system

---

## 4. Analytics Section

**What is it?**
Detailed statistics and insights about the ticket system.

### What You See:

#### A. Key Metrics (Top Cards)

1. **Total Tickets**
   - All tickets ever created

2. **Resolved Tickets**
   - Successfully fixed tickets

3. **Average Resolution Time**
   - How fast you solve problems

4. **AI Accuracy**
   - How often AI gets it right

5. **SLA Breach Rate**
   - Percentage of late tickets

6. **Breached Tickets**
   - Number of overdue tickets

#### B. Detailed Charts

1. **Ticket Growth Over Time**
   - Line chart showing daily ticket creation
   - See trends and patterns

2. **Category Distribution**
   - Pie chart of ticket types
   - See which issues are most common

3. **Priority Distribution**
   - Bar chart of urgency levels
   - See how many critical vs low priority

4. **Resolution Time Trends**
   - How resolution time changes over time
   - Are you getting faster or slower?

**Why is this useful?**
- Identify problem areas
- Track performance improvements
- Make data-driven decisions
- Report to management

---

## 5. SLA Monitoring

**What is SLA?**
SLA = Service Level Agreement
It's a promise about how fast you'll fix tickets based on priority.

### Default SLA Times:

- **Critical**: Must fix within 4 hours
- **High**: Must fix within 8 hours
- **Medium**: Must fix within 24 hours
- **Low**: Must fix within 48 hours

### What You See:

A list of tickets that are **overdue** (breached SLA):

For each breached ticket:
- Ticket ID and title
- How long it's been open
- How overdue it is
- Priority level
- Current status

**Example:**
```
Ticket #abc123: "Login not working"
Priority: Critical
Time Open: 6 hours
Overdue by: 2 hours (should have been fixed in 4 hours)
Status: In Progress
```

### What You Can Do:

1. **Click on breached ticket**
   - Opens ticket details
   - You can work on it immediately

2. **Sort by most overdue**
   - Focus on worst cases first

3. **Filter by priority**
   - See only critical breaches

**Why is this useful?**
- Ensure you meet deadlines
- Prioritize urgent work
- Maintain service quality
- Keep customers happy

---

## 6. Audit Logs

**What is it?**
A complete record of every action every admin has taken.

### What You See:

A table showing:
- **Date & Time** - When action happened
- **Admin** - Who did it
- **Action** - What they did
- **Target** - What they changed
- **Details** - Additional information

### Types of Actions Logged:

1. **Ticket Actions**
   - Status changed
   - Priority changed
   - Category overridden
   - Ticket assigned
   - Ticket merged

2. **User Actions**
   - User activated
   - User deactivated
   - Role changed

3. **System Actions**
   - Settings changed
   - SLA times updated
   - Admin logged in
   - Elevated privilege used

**Example Log Entry:**
```
Time: 2:30 PM
Admin: admin@nexora.ai
Action: Status Changed
Target: Ticket #abc123
Details: Changed from "Open" to "Resolved"
```

### What You Can Do:

1. **Filter by Admin**
   - See what a specific admin did

2. **Filter by Action Type**
   - See all status changes
   - See all category overrides

3. **Filter by Date**
   - See actions from specific time period

4. **Search**
   - Find specific ticket or user

**Why is this useful?**
- Accountability - know who did what
- Security - detect unauthorized changes
- Troubleshooting - trace back problems
- Compliance - required for some industries

---

## 7. Settings

**What is it?**
Configure how the system works.

### What You Can Change:

#### A. SLA Configuration

Set how long you have to fix tickets:

1. **Critical Priority SLA**
   - Default: 4 hours
   - Change to your needs

2. **High Priority SLA**
   - Default: 8 hours

3. **Medium Priority SLA**
   - Default: 24 hours

4. **Low Priority SLA**
   - Default: 48 hours

**How to change:**
- Enter new number of hours
- Click "Save Settings"
- New SLA applies to future tickets

#### B. AI Configuration

1. **AI Confidence Threshold**
   - Minimum confidence for AI to auto-categorize
   - Default: 0.7 (70%)
   - If AI is less confident, it asks for human review

2. **Enable/Disable Duplicate Detection**
   - Turn on to automatically find duplicate tickets
   - Turn off if causing issues

#### C. System Configuration

1. **Ticket Categories**
   - Add new categories
   - Remove unused categories
   - Rename existing categories

2. **Priority Levels**
   - Customize priority names
   - Add new priority levels

3. **Email Notifications**
   - Configure when to send emails
   - Set email templates

**Why is this useful?**
- Customize system to your needs
- Adjust SLA times for your team
- Fine-tune AI behavior
- Match your business processes

---

## Common Workflows

### Workflow 1: Resolving a Ticket

1. Login as admin
2. Click "Tickets" in sidebar
3. Find the ticket (use filters if needed)
4. Click "View" button
5. Read the ticket details
6. Add internal note about what you'll do
7. Change status to "In Progress"
8. Work on fixing the issue
9. Add another note about what you did
10. Change status to "Resolved"
11. Done! ✅

### Workflow 2: Handling Urgent Tickets

1. Login as admin
2. Click "SLA Monitoring" in sidebar
3. See list of overdue tickets
4. Click on most overdue ticket
5. Assign to yourself or another admin
6. Change status to "In Progress"
7. Work on it immediately
8. Update status when done

### Workflow 3: Checking System Health

1. Login as admin
2. Look at Overview section (default page)
3. Check key metrics:
   - Is SLA breach rate low? (Good if under 10%)
   - Is AI accuracy high? (Good if over 90%)
   - Are tickets being resolved? (Check resolved count)
4. Look at charts:
   - Are tickets increasing? (May need more staff)
   - Which category has most tickets? (May need training)
5. Take action based on insights

### Workflow 4: Team Coordination

1. Open a ticket
2. Go to "Internal Notes" tab
3. Add note: "I'm working on this, will update in 1 hour"
4. Other admins see your note
5. They won't duplicate your work
6. When done, add note: "Fixed! Changed database settings"
7. Team learns from your solution

---

## Tips for Admins

### Best Practices:

1. **Check SLA Monitoring Daily**
   - Don't let tickets become overdue
   - Prioritize breached tickets

2. **Use Internal Notes**
   - Document everything you do
   - Helps team coordination
   - Useful for training new admins

3. **Update Status Regularly**
   - Keep status current
   - Users can see progress
   - Helps with reporting

4. **Review Analytics Weekly**
   - Spot trends early
   - Identify problem areas
   - Celebrate improvements

5. **Use Filters Effectively**
   - Don't get overwhelmed by all tickets
   - Focus on what matters
   - Example: "Open" + "High Priority"

6. **Assign Tickets**
   - Distribute workload evenly
   - Clear ownership
   - Better accountability

### Keyboard Shortcuts:

- **Ctrl+F5**: Refresh page (clear cache)
- **Esc**: Close modal
- **Tab**: Navigate between fields

---

## Troubleshooting

### Problem: Can't see ticket details

**Solution:**
1. Refresh page (Ctrl+F5)
2. Check if you're logged in as admin
3. Check browser console for errors (F12)

### Problem: Status not updating

**Solution:**
1. Make sure you clicked "Update Status" button
2. Check if you confirmed the dialog
3. Refresh the page
4. Check if backend is running

### Problem: Dropdown text not visible

**Solution:**
1. Refresh page with Ctrl+F5
2. Clear browser cache
3. Check if CSS loaded properly

### Problem: Can't login as admin

**Solution:**
1. Make sure you're on "Admin Login" tab
2. Check credentials: admin@nexora.ai / admin123
3. Check if backend is running on port 5000

---

## Summary

The admin panel has 7 main sections:

1. **Overview** - Quick summary and charts
2. **Tickets** - Manage all support tickets
3. **Users** - Manage user accounts
4. **Analytics** - Detailed statistics
5. **SLA Monitoring** - Track overdue tickets
6. **Audit Logs** - See all admin actions
7. **Settings** - Configure the system

**Most Important Features:**
- Update ticket status (resolve tickets)
- View ticket details and history
- Add internal notes for team
- Monitor SLA breaches
- Check analytics for insights

**Remember:**
- Always update ticket status
- Use internal notes for documentation
- Check SLA monitoring daily
- Review analytics weekly
- Keep audit logs for accountability

---

## Need Help?

- Check `HOW_TO_RESOLVE_TICKETS.md` for detailed ticket resolution guide
- Check `ENTERPRISE_ADMIN_GUIDE.md` for technical details
- Check `API_DOCUMENTATION.md` for API reference
- Check backend terminal for error logs
- Check browser console (F12) for frontend errors

---

**Last Updated:** February 2026
**Version:** 1.0
**System:** NexoraAI Enterprise Admin Dashboard
