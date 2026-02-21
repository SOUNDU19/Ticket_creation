// API utilities

// Show toast notification
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.5rem;">
      <span style="font-size: 1.25rem;">${type === 'success' ? '✓' : type === 'error' ? '✗' : '⚠'}</span>
      <span>${message}</span>
    </div>
  `;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'toastSlideIn 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Show loading spinner
function showLoading(element) {
  const spinner = document.createElement('div');
  spinner.className = 'spinner';
  spinner.id = 'loading-spinner';
  element.appendChild(spinner);
}

// Hide loading spinner
function hideLoading() {
  const spinner = document.getElementById('loading-spinner');
  if (spinner) spinner.remove();
}

// Make API request
async function apiRequest(url, options = {}) {
  try {
    const token = window.authUtils.getToken();
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    console.log('Making API request to:', url);
    
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    // Check content type before parsing
    const contentType = response.headers.get('content-type');
    
    if (!contentType || !contentType.includes('application/json')) {
      // Response is not JSON (probably HTML error page)
      const text = await response.text();
      console.error('Non-JSON response:', text.substring(0, 200));
      throw new Error('Server returned an invalid response. Please check if the backend is running correctly.');
    }
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || data.message || 'Request failed');
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    
    // Provide more helpful error messages
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      throw new Error('Cannot connect to server. Please check if the backend is running.');
    }
    
    throw error;
  }
}

// API methods
const api = {
  // Auth
  signup: (data) => apiRequest(API_ENDPOINTS.signup, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  
  login: (data) => apiRequest(API_ENDPOINTS.login, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  
  // Tickets
  predict: (description) => apiRequest(API_ENDPOINTS.predict, {
    method: 'POST',
    body: JSON.stringify({ description })
  }),
  
  createTicket: (data) => apiRequest(API_ENDPOINTS.createTicket, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  
  getTickets: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`${API_ENDPOINTS.tickets}?${queryString}`);
  },
  
  getTicket: (id) => apiRequest(API_ENDPOINTS.ticket(id)),
  
  updateTicket: (data) => apiRequest(API_ENDPOINTS.updateTicket, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  
  // User
  updateProfile: (data) => apiRequest(API_ENDPOINTS.updateProfile, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  
  changePassword: (data) => apiRequest(API_ENDPOINTS.changePassword, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  
  deleteAccount: () => apiRequest(API_ENDPOINTS.deleteAccount, {
    method: 'DELETE'
  }),
  
  // Profile endpoints
  getProfile: () => apiRequest(API_ENDPOINTS.profile, {
    method: 'GET'
  }),

  updateProfile: (data) => apiRequest(API_ENDPOINTS.profile, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),

  uploadAvatar: async (file) => {
    const formData = new FormData();
    formData.append('avatar', file);
    
    const token = window.authUtils.getToken();
    const response = await fetch(API_ENDPOINTS.profileAvatar, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Avatar upload failed');
    }
    
    return response.json();
  },

  changePassword: (data) => apiRequest(API_ENDPOINTS.profilePassword, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),

  updateNotifications: (data) => apiRequest(API_ENDPOINTS.updateNotifications, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),

  deactivateAccount: () => apiRequest(API_ENDPOINTS.deactivateAccount, {
    method: 'POST'
  }),

  deleteAccount: (password) => apiRequest(API_ENDPOINTS.profile, {
    method: 'DELETE',
    body: JSON.stringify({ password })
  }),

  getProfileStats: () => apiRequest(API_ENDPOINTS.profileStats, {
    method: 'GET'
  }),
  getAnalytics: () => apiRequest(API_ENDPOINTS.analytics),
  
  // Admin
  getAdminTickets: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`${API_ENDPOINTS.adminTickets}?${queryString}`);
  },
  
  getAdminUsers: () => apiRequest(API_ENDPOINTS.adminUsers),
  
  getAdminAnalytics: () => apiRequest(API_ENDPOINTS.adminAnalytics)
};

// Export
window.api = api;
window.showToast = showToast;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
