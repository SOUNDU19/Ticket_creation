// Profile Page Logic
'use strict';

// Protect page
if (!authUtils.protectPage()) {
  throw new Error('Unauthorized');
}

let currentProfile = null;

// Setup event listeners when DOM is ready
function setupEventListeners() {
  // Profile form
  const profileForm = document.getElementById('profileForm');
  if (profileForm) {
    profileForm.addEventListener('submit', handleProfileUpdate);
  }
  
  // Password form
  const passwordForm = document.getElementById('passwordForm');
  if (passwordForm) {
    passwordForm.addEventListener('submit', handlePasswordChange);
  }
  
  // Delete form
  const deleteForm = document.getElementById('deleteForm');
  if (deleteForm) {
    deleteForm.addEventListener('submit', handleAccountDelete);
  }
  
  // Avatar upload
  const avatarInput = document.getElementById('avatarInput');
  if (avatarInput) {
    avatarInput.addEventListener('change', handleAvatarUpload);
  }
  
  // Password strength indicator
  const newPassword = document.getElementById('newPassword');
  if (newPassword) {
    newPassword.addEventListener('input', updatePasswordStrength);
  }
  
  // Notification toggles - auto-save on change
  const toggles = ['emailNotifications', 'ticketStatusUpdates', 'criticalAlerts', 'aiInsightUpdates'];
  toggles.forEach(id => {
    const element = document.getElementById(id);
    if (element) {
      element.addEventListener('change', () => {
        // Auto-save after a short delay
        clearTimeout(window.notificationSaveTimeout);
        window.notificationSaveTimeout = setTimeout(saveNotifications, 500);
      });
    }
  });
}

// Load profile data
async function loadProfile() {
    try {
      const response = await api.getProfile();
      currentProfile = response.profile;
      
      // Populate profile display
      document.getElementById('profileName').textContent = currentProfile.name;
      document.getElementById('profileEmail').textContent = currentProfile.email;
      document.getElementById('profileRole').textContent = currentProfile.role.toUpperCase();
      
      // Update avatar
      const avatarDisplay = document.getElementById('avatarDisplay');
      if (currentProfile.avatar_url) {
        avatarDisplay.innerHTML = `<img src="${currentProfile.avatar_url}" alt="Avatar" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
      } else {
        avatarDisplay.textContent = currentProfile.name.charAt(0).toUpperCase();
      }
      
      // Populate form fields
      document.getElementById('name').value = currentProfile.name || '';
      document.getElementById('email').value = currentProfile.email || '';
      document.getElementById('phone').value = currentProfile.phone || '';
      document.getElementById('mobile').value = currentProfile.mobile || '';
      document.getElementById('department').value = currentProfile.department || '';
      document.getElementById('timezone').value = currentProfile.timezone || 'UTC';
      
      // Last login
      if (currentProfile.last_login) {
        const lastLogin = new Date(currentProfile.last_login);
        document.getElementById('lastLogin').textContent = lastLogin.toLocaleString();
      } else {
        document.getElementById('lastLogin').textContent = 'Never';
      }
      
      // Notification settings
      if (currentProfile.notification_settings) {
        const settings = currentProfile.notification_settings;
        document.getElementById('emailNotifications').checked = settings.email_notifications;
        document.getElementById('ticketStatusUpdates').checked = settings.ticket_status_updates;
        document.getElementById('criticalAlerts').checked = settings.critical_alerts;
        document.getElementById('aiInsightUpdates').checked = settings.ai_insight_updates;
      }
      
    } catch (error) {
      showToast('Failed to load profile', 'error');
      console.error(error);
    }
  }

  // Load profile statistics
  async function loadProfileStats() {
    try {
      const response = await api.getProfileStats();
      const stats = response.stats;
      
      // Animate counters
      animateCounter(document.getElementById('statTotal'), stats.total_tickets);
      animateCounter(document.getElementById('statOpen'), stats.open_tickets);
      animateCounter(document.getElementById('statClosed'), stats.closed_tickets);
      animateCounter(document.getElementById('statHigh'), stats.high_priority);
      
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  }

  // Animate counter
  function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  }

  // Handle profile update
  async function handleProfileUpdate(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving...';
    
    try {
      const data = {
        name: document.getElementById('name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        mobile: document.getElementById('mobile').value.trim(),
        department: document.getElementById('department').value.trim(),
        timezone: document.getElementById('timezone').value
      };
      
      const response = await api.updateProfile(data);
      currentProfile = response.profile;
      
      // Update display
      document.getElementById('profileName').textContent = currentProfile.name;
      
      // Update stored user data
      const user = authUtils.getCurrentUser();
      user.name = currentProfile.name;
      localStorage.setItem('user', JSON.stringify(user));
      
      showToast('Profile updated successfully', 'success');
      
    } catch (error) {
      showToast(error.message || 'Failed to update profile', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Save Changes';
    }
  }

  // Handle avatar upload
  async function handleAvatarUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
      showToast('Invalid file type. Please upload PNG, JPG, or GIF', 'error');
      return;
    }
    
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      showToast('File too large. Maximum size is 5MB', 'error');
      return;
    }
    
    try {
      showToast('Uploading avatar...', 'info');
      
      const response = await api.uploadAvatar(file);
      
      // Update avatar display
      const avatarDisplay = document.getElementById('avatarDisplay');
      avatarDisplay.innerHTML = `<img src="${response.avatar_url}?t=${Date.now()}" alt="Avatar" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
      
      showToast('Avatar uploaded successfully', 'success');
      
    } catch (error) {
      showToast(error.message || 'Failed to upload avatar', 'error');
    }
  }

  // Handle password change
  async function handlePasswordChange(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Validate passwords match
    if (newPassword !== confirmPassword) {
      showToast('New passwords do not match', 'error');
      return;
    }
    
    // Validate password strength
    if (newPassword.length < 8) {
      showToast('Password must be at least 8 characters long', 'error');
      return;
    }
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Changing...';
    
    try {
      await api.changePassword({
        current_password: currentPassword,
        new_password: newPassword
      });
      
      // Clear form
      document.getElementById('passwordForm').reset();
      document.getElementById('strengthFill').style.width = '0';
      document.getElementById('strengthText').textContent = 'Password strength';
      
      showToast('Password changed successfully', 'success');
      
    } catch (error) {
      showToast(error.message || 'Failed to change password', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Change Password';
    }
  }

  // Update password strength indicator
  function updatePasswordStrength(e) {
    const password = e.target.value;
    const strength = calculatePasswordStrength(password);
    
    const fill = document.getElementById('strengthFill');
    const text = document.getElementById('strengthText');
    
    fill.style.width = strength.percent + '%';
    fill.style.background = strength.color;
    text.textContent = strength.label;
    text.style.color = strength.color;
  }

  // Calculate password strength
  function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength += 25;
    if (password.length >= 12) strength += 25;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 20;
    if (/\d/.test(password)) strength += 15;
    if (/[^a-zA-Z\d]/.test(password)) strength += 15;
    
    if (strength < 40) return { percent: strength, color: '#ef4444', label: 'Weak' };
    if (strength < 70) return { percent: strength, color: '#f59e0b', label: 'Medium' };
    return { percent: strength, color: '#10b981', label: 'Strong' };
  }

// Save notification preferences
window.saveNotifications = async function() {
    try {
      const data = {
        email_notifications: document.getElementById('emailNotifications').checked,
        ticket_status_updates: document.getElementById('ticketStatusUpdates').checked,
        critical_alerts: document.getElementById('criticalAlerts').checked,
  
        ai_insight_updates: document.getElementById('aiInsightUpdates').checked
      };
      
      await api.updateNotifications(data);
      showToast('Notification preferences saved', 'success');
      
    } catch (error) {
      showToast(error.message || 'Failed to save preferences', 'error');
    }
  };

// Deactivate account
window.deactivateAccount = async function() {
    if (!confirm('Are you sure you want to deactivate your account? You can reactivate it by logging in again.')) {
      return;
    }
    
    try {
      await api.deactivateAccount();
      showToast('Account deactivated. Logging out...', 'success');
      
      setTimeout(() => {
        authUtils.logout();
      }, 2000);
      
    } catch (error) {
      showToast(error.message || 'Failed to deactivate account', 'error');
    }
  };

// Show delete modal
window.showDeleteModal = function() {
    document.getElementById('deleteModal').classList.add('active');
  };

// Close delete modal
window.closeDeleteModal = function() {
    document.getElementById('deleteModal').classList.remove('active');
    document.getElementById('deleteForm').reset();
  };

  // Handle account deletion
  async function handleAccountDelete(e) {
    e.preventDefault();
    
    const password = document.getElementById('deletePassword').value;
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Deleting...';
    
    try {
      await api.deleteAccount(password);
      
      showToast('Account deleted successfully. Logging out...', 'success');
      
      setTimeout(() => {
        authUtils.logout();
      }, 2000);
      
    } catch (error) {
      showToast(error.message || 'Failed to delete account', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Delete My Account';
    }
  }

  // Toast notification
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.style.cssText = `
      position: fixed;
      top: 2rem;
      right: 2rem;
      background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
      z-index: 3000;
      max-width: 400px;
      animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOutRight 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Add CSS animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initProfile);
} else {
  initProfile();
}

function initProfile() {
  console.log('Initializing profile page...');
  setupEventListeners();
  loadProfile();
  loadProfileStats();
}
