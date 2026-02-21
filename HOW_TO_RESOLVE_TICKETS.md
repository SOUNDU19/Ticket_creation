# How to Resolve Tickets as Admin

## Quick Guide

### Step 1: Login as Admin
1. Go to: `http://localhost:8000/login.html`
2. Click on the "🔐 Admin Login" tab
3. Enter credentials:
   - Email: `admin@nexora.ai`
   - Password: `admin123`
4. Click "Sign In"
5. You'll be redirected to the Enterprise Admin Dashboard

### Step 2: Navigate to Tickets
1. In the left sidebar, click on "Tickets"
2. You'll see a table with all tickets in the system
3. You can filter by:
   - Search (title/description)
   - Status (Open, In Progress, Resolved, Closed)
   - Priority (Critical, High, Medium, Low)

### Step 3: Open Ticket Details
1. Find the ticket you want to resolve
2. Click the "View" button in the Actions column
3. A modal will open showing full ticket details

### Step 4: Update Ticket Status
1. In the ticket modal, you'll see a purple section labeled "Update Ticket Status"
2. Use the dropdown to select the new status:
   - **Open**: Newly created, awaiting assignment
   - **In Progress**: Currently being worked on
   - **Resolved**: Issue has been fixed
   - **Closed**: Completed and confirmed
3. Click the "Update Status" button
4. Confirm the action in the popup dialog
5. The ticket will be updated and the modal will close

### Step 5: Verify Update
1. The ticket list will automatically refresh
2. You'll see the updated status in the Status column
3. A success message will appear at the top right

## Additional Admin Actions

While viewing a ticket, you can also:

### Override AI Category
- Click "Override Category" button
- Enter the correct category
- Useful when AI misclassifies a ticket

### Assign Ticket
- Click "Assign Ticket" button
- Select an admin to assign the ticket to
- Helps with workload distribution

### Merge Tickets
- Click "Merge Ticket" button
- Enter the target ticket ID
- Combines duplicate tickets

### Add Internal Notes
- Switch to the "Internal Notes" tab
- Add notes visible only to admins
- Useful for internal communication

### View Timeline
- Switch to the "Timeline" tab
- See all actions taken on the ticket
- Track the ticket's history

### View User Context
- Switch to the "User Context" tab
- See user's ticket history
- Understand user's patterns

## Ticket Status Workflow

Recommended workflow:

```
Open → In Progress → Resolved → Closed
```

- **Open**: User creates ticket
- **In Progress**: Admin starts working on it
- **Resolved**: Admin fixes the issue
- **Closed**: User confirms or auto-closed after time

## Tips

1. **Use Filters**: Filter by status to focus on open tickets
2. **Check SLA**: Monitor the SLA column to prioritize breached tickets
3. **Add Notes**: Use internal notes for team communication
4. **Bulk Actions**: Select multiple tickets for bulk status updates (if needed)
5. **Review Analytics**: Check the Overview section for insights

## Troubleshooting

**Can't see tickets?**
- Make sure you're logged in as admin
- Check that tickets exist in the system
- Try refreshing the page

**Status not updating?**
- Check your internet connection
- Verify you have admin permissions
- Check browser console for errors

**Modal not opening?**
- Refresh the page
- Clear browser cache
- Check if JavaScript is enabled

## API Endpoint Used

The admin dashboard uses this endpoint to update tickets:

```
PUT /api/update-ticket
Authorization: Bearer <admin_token>

Request Body:
{
  "ticket_id": "uuid-of-ticket",
  "status": "resolved"
}

Response:
{
  "message": "Ticket updated successfully",
  "ticket": { ... }
}
```

## Need Help?

- Check the Enterprise Admin Guide: `ENTERPRISE_ADMIN_GUIDE.md`
- Review API Documentation: `API_DOCUMENTATION.md`
- Check system logs in the backend terminal
