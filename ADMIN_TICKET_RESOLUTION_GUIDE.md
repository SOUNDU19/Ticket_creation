# Admin Ticket Resolution Guide

## How to Resolve Tickets in Admin Dashboard

### Current Implementation

The admin dashboard (`admin-dashboard-enhanced.html`) displays tickets but needs a status update feature to resolve them.

### Step-by-Step Guide to Resolve Tickets

#### Method 1: Using the Ticket Modal (Recommended)

1. **Login as Admin**
   - Go to: `http://localhost:8000/login.html`
   - Email: `admin@nexora.ai`
   - Password: `admin123`

2. **Navigate to Tickets Section**
   - Click on "Tickets" in the left sidebar
   - You'll see a list of all tickets with their current status

3. **Open Ticket Details**
   - Click the "View" button on any ticket
   - A modal will open showing full ticket details

4. **Update Ticket Status** (Feature to be added)
   - In the ticket modal, there should be a status dropdown
   - Select new status: Open, In Progress, Resolved, or Closed
   - Click "Update Status" button
   - Ticket will be updated and modal will close

#### Method 2: Using Bulk Actions (Future Enhancement)

1. Select multiple tickets using checkboxes
2. Choose action from bulk actions dropdown
3. Apply to all selected tickets

### Available Ticket Statuses

- **Open**: Newly created, awaiting assignment
- **In Progress**: Being worked on
- **Resolved**: Issue fixed, awaiting user confirmation
- **Closed**: Completed and confirmed

### Backend API Endpoint

The system uses the following endpoint to update tickets:

```
PUT /api/update-ticket
Authorization: Bearer <admin_token>

Body:
{
  "ticket_id": "uuid-here",
  "status": "resolved"
}
```

### Features Needed in Admin Dashboard

1. **Status Dropdown in Ticket Modal**
   - Add a select dropdown with status options
   - Add "Update Status" button
   - Show success/error toast messages

2. **Quick Status Actions**
   - Add quick action buttons in ticket list
   - "Mark as Resolved" button
   - "Close Ticket" button

3. **Status Change History**
   - Log all status changes in audit logs
   - Show who changed status and when

### Implementation Notes

The admin dashboard JavaScript (`admin-enhanced.js`) needs:
- `updateTicketStatus(ticketId, newStatus)` function
- UI elements in the ticket modal for status selection
- Event handlers for status update buttons

### Workaround (Until UI is Added)

Admins can currently:
1. View all tickets and their details
2. Use internal notes to communicate
3. Assign tickets to specific admins
4. Override AI categorization
5. Merge duplicate tickets

To manually update status, you would need to:
- Use the API directly via Postman/curl
- Or add the UI feature as described above
