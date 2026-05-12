// Authentication utilities

// Check if user is logged in
function isLoggedIn() {
  return localStorage.getItem('token') !== null;
}

// Get current user
function getCurrentUser() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

// Get auth token
function getToken() {
  return localStorage.getItem('token') || null;
}

// Save auth data
function saveAuthData(token, user) {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
}

// Clear auth data
function clearAuthData() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

// Logout — clear session and go to login
function logout() {
  clearAuthData();
  window.location.href = 'login.html';
}

// Check if user is admin
function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

// Protect page — redirect to login if not authenticated
function protectPage() {
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

// Protect admin page — redirect if not admin
function protectAdminPage() {
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return false;
  }
  if (!isAdmin()) {
    window.location.href = 'dashboard.html';
    return false;
  }
  return true;
}

// Redirect if already logged in
function redirectIfLoggedIn() {
  if (isLoggedIn()) {
    const user = getCurrentUser();
    if (user && user.role === 'admin') {
      window.location.href = 'admin-dashboard-enhanced.html';
    } else {
      window.location.href = 'dashboard.html';
    }
  }
}

// Export functions
window.authUtils = {
  isLoggedIn,
  getCurrentUser,
  getToken,
  saveAuthData,
  clearAuthData,
  logout,
  isAdmin,
  protectPage,
  protectAdminPage,
  redirectIfLoggedIn
};
