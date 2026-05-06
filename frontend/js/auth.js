// Authentication utilities — No login required, guest mode enabled

// Default guest user used when no real user is logged in
const GUEST_USER = {
  id: 'guest',
  name: 'Guest',
  email: 'guest@nexoraai.com',
  role: 'user'
};

// Check if user is logged in (always true in guest mode)
function isLoggedIn() {
  return true;
}

// Get current user — returns stored user or guest
function getCurrentUser() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : GUEST_USER;
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

// Go to landing page (replaces logout)
function logout() {
  clearAuthData();
  window.location.href = 'landing.html';
}

// Check if user is admin
function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

// No longer blocks access — always returns true
function protectPage() {
  return true;
}

// Admin page — still requires admin role
function protectAdminPage() {
  if (!isAdmin()) {
    window.location.href = 'dashboard.html';
    return false;
  }
  return true;
}

// No-op — no redirect needed
function redirectIfLoggedIn() {}

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
