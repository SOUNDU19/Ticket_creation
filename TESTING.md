# NexoraAI Support Suite - Testing Guide

## 🧪 Testing Overview

This guide covers manual testing procedures for all features of NexoraAI Support Suite.

## Prerequisites

- Backend running on `http://localhost:5000`
- Frontend running on `http://localhost:8000`
- ML model trained (model.pkl and vectorizer.pkl exist)
- Database initialized

## 🔐 Authentication Testing

### Test 1: User Registration

1. Navigate to `http://localhost:8000/signup.html`
2. Fill in the form:
   - Name: Test User
   - Email: test@example.com
   - Mobile: +1234567890
   - Password: test123
   - Confirm Password: test123
3. Click "Create Account"
4. **Expected:** Success message, redirect to dashboard
5. **Verify:** User appears in database, JWT token stored in localStorage

### Test 2: User Login

1. Navigate to `http://localhost:8000/login.html`
2. Enter credentials:
   - Email: test@example.com
   - Password: test123
3. Click "Login"
4. **Expected:** Success message, redirect to dashboard
5. **Verify:** JWT token stored, user data in localStorage

### Test 3: Admin Login

1. Navigate to `http://localhost:8000/login.html`
2. Enter admin credentials:
   - Email: admin@nexora.ai
   - Password: admin123
3. Click "Login"
4. **Expected:** Success message, redirect to dashboard with admin link
5. **Verify:** Admin panel link visible in navigation

### Test 4: Invalid Login

1. Navigate to login page
2. Enter invalid credentials
3. **Expected:** Error message "Invalid email or password"

### Test 5: Logout

1. Click "Logout" in navigation
2. **Expected:** Redirect to login page
3. **Verify:** localStorage cleared, cannot access protected pages

## 🎫 Ticket Management Testing

### Test 6: Create Ticket with AI

1. Login as user
2. Navigate to "Create Ticket"
3. Enter:
   - Title: "Application crashes on startup"
   - Description: "The application crashes immediately when I try to open it. Error code 500 appears on screen."
4. Click "Analyze with AI"
5. **Expected:** 
   - AI preview shows category (e.g., "bug", "technical")
   - Priority assigned (likely "high")
   - Confidence score displayed (>0.8)
   - Entities extracted (error code "500")
6. Click "Create Ticket"
7. **Expected:** Success message, redirect to history
8. **Verify:** Ticket appears in database and history

### Test 7: View Ticket History

1. Navigate to "History"
2. **Expected:** List of all user tickets
3. **Verify:** 
   - Tickets display correctly
   - Filters work (status, priority, category)
   - Search functionality works
   - Pagination appears if >10 tickets

### Test 8: View Ticket Details

1. Click on any ticket in history
2. **Expected:** 
   - Full ticket details displayed
   - Category, priority, status badges
   - AI confidence score
   - Created/updated timestamps
3. Click "Download PDF"
4. **Expected:** PDF file downloads with ticket information

### Test 9: Update Ticket Status (Admin)

1. Login as admin
2. Navigate to any ticket details
3. Change status dropdown
4. Click "Update Status"
5. **Expected:** Success message, status updated
6. **Verify:** Status change reflected in database

## 📊 Analytics Testing

### Test 10: User Analytics

1. Login as user
2. Navigate to "Analytics"
3. **Expected:**
   - Category distribution chart (doughnut)
   - Priority distribution chart (bar)
   - Monthly trends chart (line)
4. **Verify:** Charts render correctly with actual data

### Test 11: Admin Analytics

1. Login as admin
2. Navigate to "Admin Panel"
3. **Expected:**
   - System-wide statistics
   - Total users count
   - Total tickets count
   - High priority count
4. **Verify:** Numbers match database records

## 👤 Profile Management Testing

### Test 12: Update Profile

1. Navigate to "Profile"
2. Change mobile number
3. Click "Update Profile"
4. **Expected:** Success message
5. **Verify:** Mobile number updated in database

### Test 13: Change Password

1. Navigate to "Profile"
2. Enter:
   - Current Password: test123
   - New Password: newpass123
   - Confirm Password: newpass123
3. Click "Change Password"
4. **Expected:** Success message
5. **Verify:** Can login with new password

### Test 14: Delete Account

1. Navigate to "Profile"
2. Scroll to "Danger Zone"
3. Click "Delete Account"
4. Confirm deletion
5. **Expected:** Success message, redirect to login
6. **Verify:** User and all tickets deleted from database

## 🔍 Search and Filter Testing

### Test 15: Search Tickets

1. Navigate to "History"
2. Enter search term in search box
3. Click "Apply Filters"
4. **Expected:** Only matching tickets displayed

### Test 16: Filter by Status

1. Navigate to "History"
2. Select status filter (e.g., "Open")
3. Click "Apply Filters"
4. **Expected:** Only open tickets displayed

### Test 17: Filter by Priority

1. Navigate to "History"
2. Select priority filter (e.g., "High")
3. Click "Apply Filters"
4. **Expected:** Only high priority tickets displayed

### Test 18: Combined Filters

1. Apply multiple filters simultaneously
2. **Expected:** Results match all filter criteria

## 🎨 UI/UX Testing

### Test 19: Responsive Design

1. Open application in browser
2. Resize window to mobile size (375px width)
3. **Expected:** 
   - Layout adapts to mobile
   - Navigation collapses
   - Cards stack vertically
   - All content readable

### Test 20: Toast Notifications

1. Perform any action (create ticket, update profile)
2. **Expected:** 
   - Toast appears in top-right
   - Appropriate icon and color
   - Auto-dismisses after 3 seconds

### Test 21: Loading States

1. Perform action that requires API call
2. **Expected:** 
   - Loading spinner appears
   - Button disabled during loading
   - Loading text displayed

### Test 22: Form Validation

1. Try to submit forms with:
   - Empty fields
   - Invalid email format
   - Short password (<6 chars)
   - Mismatched passwords
2. **Expected:** Appropriate error messages

## 🔒 Security Testing

### Test 23: Protected Routes

1. Logout
2. Try to access `http://localhost:8000/dashboard.html` directly
3. **Expected:** Redirect to login page

### Test 24: Admin-Only Access

1. Login as regular user
2. Try to access `http://localhost:8000/admin.html`
3. **Expected:** Redirect to dashboard

### Test 25: JWT Expiration

1. Login
2. Wait 24 hours (or modify JWT expiry for testing)
3. Try to access protected page
4. **Expected:** Redirect to login, "Token expired" message

### Test 26: SQL Injection Prevention

1. Try to login with:
   - Email: `admin' OR '1'='1`
   - Password: anything
2. **Expected:** Login fails, no SQL injection

## 🤖 ML Model Testing

### Test 27: Category Prediction Accuracy

Test with various ticket descriptions:

1. **Bug Report:**
   - Description: "Application crashes when clicking submit button"
   - **Expected:** Category: "bug" or "technical", Priority: "high"

2. **Feature Request:**
   - Description: "Please add dark mode to the application"
   - **Expected:** Category: "feature" or "enhancement", Priority: "low/medium"

3. **Security Issue:**
   - Description: "Found security vulnerability in login system"
   - **Expected:** Category: "security", Priority: "high"

4. **Performance Issue:**
   - Description: "Application is very slow when loading data"
   - **Expected:** Category: "performance", Priority: "medium/high"

### Test 28: Entity Extraction

1. Create ticket with description: "John Smith reported error 404 in Microsoft Office"
2. **Expected Entities:**
   - Persons: ["John Smith"]
   - Software: ["Microsoft Office"]
   - Error Codes: ["404"]

### Test 29: Confidence Scoring

1. Create ticket with clear, detailed description
2. **Expected:** Confidence >0.9

3. Create ticket with vague description
4. **Expected:** Confidence <0.7

## 📱 Cross-Browser Testing

### Test 30: Browser Compatibility

Test in multiple browsers:
- Chrome
- Firefox
- Safari
- Edge

**Verify:**
- All pages load correctly
- Styles render properly
- JavaScript functions work
- Charts display correctly

## 🚀 Performance Testing

### Test 31: Page Load Time

1. Open browser DevTools (Network tab)
2. Load each page
3. **Expected:** Load time <2 seconds

### Test 32: API Response Time

1. Open browser DevTools (Network tab)
2. Perform API calls
3. **Expected:** Response time <200ms for most endpoints

### Test 33: Large Dataset Handling

1. Create 100+ tickets
2. Navigate to history page
3. **Expected:** 
   - Pagination works correctly
   - Page remains responsive
   - No performance degradation

## 🐛 Error Handling Testing

### Test 34: Network Error

1. Stop backend server
2. Try to perform any action
3. **Expected:** Appropriate error message

### Test 35: Invalid Data

1. Send invalid data to API (use browser console)
2. **Expected:** Validation error message

### Test 36: 404 Page

1. Navigate to non-existent page
2. **Expected:** Custom 404 page displays

## 📋 Test Results Template

```
Test ID: [Test Number]
Test Name: [Test Name]
Date: [Date]
Tester: [Name]
Status: [PASS/FAIL]
Notes: [Any observations]
```

## 🎯 Acceptance Criteria

All tests must pass for production deployment:

- [ ] All authentication tests pass
- [ ] All ticket management tests pass
- [ ] All analytics tests pass
- [ ] All profile management tests pass
- [ ] All search/filter tests pass
- [ ] All UI/UX tests pass
- [ ] All security tests pass
- [ ] All ML model tests pass
- [ ] All cross-browser tests pass
- [ ] All performance tests pass
- [ ] All error handling tests pass

## 🔄 Regression Testing

After any code changes, run:
1. Authentication tests (1-5)
2. Core ticket tests (6-9)
3. Security tests (23-26)

## 📊 Test Coverage

- Backend API: 100% endpoints tested
- Frontend Pages: 100% pages tested
- ML Pipeline: Core functionality tested
- Security: All critical paths tested
- UI/UX: All major components tested

## 🆘 Troubleshooting Test Failures

### Backend Not Responding
```bash
cd backend
python app.py
```

### ML Model Missing
```bash
cd backend/ml
python train.py
```

### Database Issues
```bash
rm backend/nexora.db
python backend/app.py
```

### Frontend Not Loading
```bash
cd frontend
python -m http.server 8000
```

---

**Designed & Developed by Soundarya**

Happy Testing! 🧪
