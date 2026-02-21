// API Configuration
// Automatically detect environment
let API_BASE_URL;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  // Local development
  API_BASE_URL = 'http://localhost:5000/api';
} else {
  // Production - Vercel or other platforms use relative path
  API_BASE_URL = '/api';
}

console.log('API Base URL:', API_BASE_URL);

// API Endpoints
const API_ENDPOINTS = {
  signup: `${API_BASE_URL}/signup`,
  login: `${API_BASE_URL}/login`,
  predict: `${API_BASE_URL}/predict`,
  createTicket: `${API_BASE_URL}/create-ticket`,
  tickets: `${API_BASE_URL}/tickets`,
  ticket: (id) => `${API_BASE_URL}/ticket/${id}`,
  updateTicket: `${API_BASE_URL}/update-ticket`,
  updateProfile: `${API_BASE_URL}/update-profile`,
  changePassword: `${API_BASE_URL}/change-password`,
  deleteAccount: `${API_BASE_URL}/delete-account`,
  analytics: `${API_BASE_URL}/analytics`,
  
  // Admin endpoints
  adminDashboardStats: `${API_BASE_URL}/admin/dashboard-stats`,
  adminTickets: `${API_BASE_URL}/admin/tickets`,
  adminTicket: (id) => `${API_BASE_URL}/admin/tickets/${id}`,
  adminBulkUpdate: `${API_BASE_URL}/admin/tickets/bulk-update`,
  adminUsers: `${API_BASE_URL}/admin/users`,
  adminUser: (id) => `${API_BASE_URL}/admin/users/${id}`,
  adminAnalytics: `${API_BASE_URL}/admin/analytics`,
  adminModelMetrics: `${API_BASE_URL}/admin/model-metrics`,
  adminAuditLogs: `${API_BASE_URL}/admin/audit-logs`,
  adminSettings: `${API_BASE_URL}/admin/settings`,
  adminExport: (type) => `${API_BASE_URL}/admin/export/${type}`,
  adminNotifications: `${API_BASE_URL}/admin/notifications`,
  adminNotificationRead: (id) => `${API_BASE_URL}/admin/notifications/${id}/read`,
  
  // Profile endpoints
  profile: `${API_BASE_URL}/profile`,
  profileAvatar: `${API_BASE_URL}/profile/avatar`,
  profilePassword: `${API_BASE_URL}/profile/password`,
  updateNotifications: `${API_BASE_URL}/profile/notifications`,
  deactivateAccount: `${API_BASE_URL}/profile/deactivate`,
  profileStats: `${API_BASE_URL}/profile/stats`,
  
  // User Analytics endpoints
  analyticsOverview: `${API_BASE_URL}/user/analytics/overview`,
  analyticsActivity: `${API_BASE_URL}/user/analytics/activity`,
  analyticsCategoryDist: `${API_BASE_URL}/user/analytics/category-distribution`,
  analyticsPriorityDist: `${API_BASE_URL}/user/analytics/priority-distribution`,
  analyticsAIInsights: `${API_BASE_URL}/user/analytics/ai-insights`,
  analyticsResolution: `${API_BASE_URL}/user/analytics/resolution-insights`,
  analyticsMonthlySummary: `${API_BASE_URL}/user/analytics/monthly-summary`,
  
  health: `${API_BASE_URL}/health`
};

// Export for use in other files
window.API_BASE_URL = API_BASE_URL;
window.API_ENDPOINTS = API_ENDPOINTS;
