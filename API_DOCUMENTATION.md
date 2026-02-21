# NexoraAI Support Suite - API Documentation

## Base URL

```
http://localhost:5000/api
```

Production: `https://your-domain.com/api`

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Response Format

All responses are in JSON format:

### Success Response
```json
{
  "message": "Success message",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error message",
  "message": "Detailed error description"
}
```

## Endpoints

### 1. Health Check

Check API status.

**Endpoint:** `GET /health`  
**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "message": "NexoraAI API is running"
}
```

---

### 2. User Registration

Register a new user account.

**Endpoint:** `POST /signup`  
**Authentication:** Not required

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "password": "password123",
  "confirmPassword": "password123"
}
```

**Validation Rules:**
- `name`: Required, non-empty string
- `email`: Required, valid email format
- `mobile`: Required, valid phone number (10-15 digits)
- `password`: Required, minimum 6 characters
- `confirmPassword`: Must match password

**Success Response (201):**
```json
{
  "message": "Registration successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "role": "user",
    "profile_image": "default.png",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `400`: Validation error (missing fields, invalid format)
- `400`: Email already registered
- `500`: Server error

---

### 3. User Login

Authenticate user and receive JWT token.

**Endpoint:** `POST /login`  
**Authentication:** Not required

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "role": "user",
    "profile_image": "default.png",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `400`: Missing email or password
- `401`: Invalid credentials
- `500`: Server error

---

### 4. AI Ticket Prediction

Get AI prediction for ticket categorization.

**Endpoint:** `POST /predict`  
**Authentication:** Required

**Request Body:**
```json
{
  "description": "The application crashes when I click the submit button. Error code 500 appears."
}
```

**Success Response (200):**
```json
{
  "category": "bug",
  "priority": "high",
  "confidence": 0.97,
  "entities": {
    "persons": [],
    "software": [],
    "error_codes": ["500"]
  }
}
```

**Response Fields:**
- `category`: Predicted ticket category
- `priority`: Assigned priority (high/medium/low)
- `confidence`: Model confidence score (0-1)
- `entities`: Extracted named entities

**Error Responses:**
- `400`: Missing description
- `401`: Invalid or missing token
- `500`: Prediction error

---

### 5. Create Ticket

Create a new support ticket.

**Endpoint:** `POST /create-ticket`  
**Authentication:** Required

**Request Body:**
```json
{
  "title": "Application Crash on Submit",
  "description": "The application crashes when I click the submit button. Error code 500 appears.",
  "category": "bug",
  "priority": "high",
  "confidence": 0.97
}
```

**Success Response (201):**
```json
{
  "message": "Ticket created successfully",
  "ticket": {
    "id": "uuid-string",
    "user_id": "user-uuid",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "title": "Application Crash on Submit",
    "description": "The application crashes...",
    "category": "bug",
    "priority": "high",
    "status": "open",
    "ai_confidence": 0.97,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `400`: Missing required fields
- `401`: Invalid or missing token
- `500`: Server error

---

### 6. Get User Tickets

Retrieve tickets for the authenticated user.

**Endpoint:** `GET /tickets`  
**Authentication:** Required

**Query Parameters:**
- `status` (optional): Filter by status (open/in_progress/closed)
- `category` (optional): Filter by category
- `priority` (optional): Filter by priority (high/medium/low)
- `search` (optional): Search in title and description
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Example:**
```
GET /tickets?status=open&priority=high&page=1&per_page=10
```

**Success Response (200):**
```json
{
  "tickets": [
    {
      "id": "uuid-string",
      "user_id": "user-uuid",
      "user_name": "John Doe",
      "user_email": "john@example.com",
      "title": "Application Crash",
      "description": "Description text...",
      "category": "bug",
      "priority": "high",
      "status": "open",
      "ai_confidence": 0.97,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `500`: Server error

---

### 7. Get Ticket Details

Retrieve details of a specific ticket.

**Endpoint:** `GET /ticket/<ticket_id>`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "ticket": {
    "id": "uuid-string",
    "user_id": "user-uuid",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "title": "Application Crash",
    "description": "Full description...",
    "category": "bug",
    "priority": "high",
    "status": "open",
    "ai_confidence": 0.97,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: Access denied (not ticket owner or admin)
- `404`: Ticket not found
- `500`: Server error

---

### 8. Update Ticket

Update ticket status (admin or ticket owner).

**Endpoint:** `PUT /update-ticket`  
**Authentication:** Required

**Request Body:**
```json
{
  "ticket_id": "uuid-string",
  "status": "in_progress"
}
```

**Status Values:**
- `open`
- `in_progress`
- `closed`

**Success Response (200):**
```json
{
  "message": "Ticket updated successfully",
  "ticket": {
    "id": "uuid-string",
    "status": "in_progress",
    "updated_at": "2024-01-01T00:00:00",
    ...
  }
}
```

**Error Responses:**
- `400`: Missing ticket_id
- `401`: Invalid or missing token
- `403`: Access denied
- `404`: Ticket not found
- `500`: Server error

---

### 9. Update Profile

Update user profile information.

**Endpoint:** `PUT /update-profile`  
**Authentication:** Required

**Request Body:**
```json
{
  "mobile": "+1234567890",
  "name": "John Doe Updated"
}
```

**Success Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": "uuid-string",
    "name": "John Doe Updated",
    "email": "john@example.com",
    "mobile": "+1234567890",
    "role": "user",
    "profile_image": "default.png",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses:**
- `400`: Invalid mobile number
- `401`: Invalid or missing token
- `404`: User not found
- `500`: Server error

---

### 10. Change Password

Change user password.

**Endpoint:** `PUT /change-password`  
**Authentication:** Required

**Request Body:**
```json
{
  "currentPassword": "oldpassword123",
  "newPassword": "newpassword123",
  "confirmPassword": "newpassword123"
}
```

**Success Response (200):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400`: Missing fields or passwords don't match
- `401`: Current password incorrect or invalid token
- `500`: Server error

---

### 11. Delete Account

Delete user account and all associated tickets.

**Endpoint:** `DELETE /delete-account`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "message": "Account deleted successfully"
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `404`: User not found
- `500`: Server error

---

### 12. Get Analytics

Get analytics data for authenticated user.

**Endpoint:** `GET /analytics`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "stats": {
    "total": 25,
    "open": 10,
    "in_progress": 5,
    "closed": 10,
    "high_priority": 8
  },
  "categories": {
    "bug": 10,
    "feature": 8,
    "performance": 5,
    "security": 2
  },
  "priorities": {
    "high": 8,
    "medium": 12,
    "low": 5
  },
  "monthly": {
    "2024-01": 5,
    "2024-02": 10,
    "2024-03": 10
  }
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `500`: Server error

---

### 13. Get All Tickets (Admin)

Get all tickets from all users (admin only).

**Endpoint:** `GET /admin/tickets`  
**Authentication:** Required (Admin role)

**Query Parameters:**
Same as `/tickets` endpoint

**Success Response (200):**
```json
{
  "tickets": [ ... ],
  "total": 100,
  "pages": 10,
  "current_page": 1
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: Admin access required
- `500`: Server error

---

### 14. Get All Users (Admin)

Get all registered users (admin only).

**Endpoint:** `GET /admin/users`  
**Authentication:** Required (Admin role)

**Success Response (200):**
```json
{
  "users": [
    {
      "id": "uuid-string",
      "name": "John Doe",
      "email": "john@example.com",
      "mobile": "+1234567890",
      "role": "user",
      "profile_image": "default.png",
      "created_at": "2024-01-01T00:00:00",
      "ticket_count": 15
    }
  ]
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: Admin access required
- `500`: Server error

---

### 15. Get Admin Analytics

Get system-wide analytics (admin only).

**Endpoint:** `GET /admin/analytics`  
**Authentication:** Required (Admin role)

**Success Response (200):**
```json
{
  "stats": {
    "total_tickets": 100,
    "total_users": 25,
    "open": 30,
    "closed": 50,
    "high_priority": 20
  },
  "categories": {
    "bug": 40,
    "feature": 30,
    "performance": 20,
    "security": 10
  },
  "priorities": {
    "high": 20,
    "medium": 50,
    "low": 30
  }
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: Admin access required
- `500`: Server error

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per user

## CORS

CORS is enabled for all origins in development. Configure `CORS_ORIGINS` in `.env` for production.

## JWT Token

- Expiry: 24 hours
- Algorithm: HS256
- Refresh: Not implemented (re-login required)

## Example Usage (JavaScript)

```javascript
// Login
const response = await fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
const token = data.token;

// Create Ticket
const ticketResponse = await fetch('http://localhost:5000/api/create-ticket', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    title: 'Bug Report',
    description: 'Application crashes',
    category: 'bug',
    priority: 'high',
    confidence: 0.95
  })
});
```

## Example Usage (Python)

```python
import requests

# Login
response = requests.post('http://localhost:5000/api/login', json={
    'email': 'user@example.com',
    'password': 'password123'
})

token = response.json()['token']

# Create Ticket
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

ticket_response = requests.post(
    'http://localhost:5000/api/create-ticket',
    headers=headers,
    json={
        'title': 'Bug Report',
        'description': 'Application crashes',
        'category': 'bug',
        'priority': 'high',
        'confidence': 0.95
    }
)
```

---

**Designed & Developed by Soundarya**
