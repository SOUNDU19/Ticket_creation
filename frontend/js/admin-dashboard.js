// Admin Dashboard Logic
(function() {
  'use strict';

  // Protect page - admin only
  if (!authUtils.protectAdminPage()) {
    throw new Error('Unauthorized');
  }

  let currentSection = 'overview';
  let selectedTickets = new Set();
  let charts = {};

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    loadAdminName();
    loadOverview();
    loadNotifications();
  });

  // Load admin name
  function loadAdminName() {
    const user = authUtils.getCurrentUser();
    if (user) {
      document.getElementById('adminName').textContent = user.name;
    }
  }

  // Show section
  window.showSection = function(section) {
    currentSection = section;
    
    // Update sidebar
    document.querySelectorAll('.sidebar-link').forEach(link => {
      link.classList.remove('active');
    });
    event.target.closest('.sidebar-link').classList.add('active');
    
    // Update sections
    document.querySelectorAll('.admin-section').forEach(sec => {
      sec.classList.remove('active');
    });
    document.getElementById(`${section}-section`).classList.add('active');
    
    // Load section data
    switch(section) {
      case 'overview':
        loadOverview();
        break;
      case 'tickets':
        loadTickets();
        break;
      case 'analytics':
        loadAnalytics();
        break;
      case 'ai-monitoring':
        loadAIMonitoring();
        break;
      case 'users':
        loadUsers();
        break;
      case 'audit-logs':
        loadAuditLogs();
        break;
      case 'settings':
        loadSettings();
        break;
    }
  };

  // Load Overview
  async function loadOverview() {
    try {
      const response = await fetch(API_ENDPOINTS.adminDashboardStats, {
        headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
      });
      const data = await response.json();
      
      const stats = data.stats;
      
      document.getElementById('statsGrid').innerHTML = `
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #667eea, #764ba2);">🎫</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.total_tickets}">0</h3>
            <p>Total Tickets</p>
            <span class="stat-trend">+${stats.recent_tickets} this week</span>
          </div>
        </div>
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #f093fb, #f5576c);">👥</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.total_users}">0</h3>
            <p>Total Users</p>
            <span class="stat-trend">${stats.active_users} active</span>
          </div>
        </div>
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">🔓</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.open_tickets}">0</h3>
            <p>Open Tickets</p>
            <span class="stat-trend">${stats.in_progress_tickets} in progress</span>
          </div>
        </div>
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #fa709a, #fee140);">⚠️</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.high_priority}">0</h3>
            <p>High Priority</p>
            <span class="stat-trend">Needs attention</span>
          </div>
        </div>
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #a8edea, #fed6e3);">✅</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.resolved_tickets}">0</h3>
            <p>Resolved</p>
            <span class="stat-trend">${stats.closed_tickets} closed</span>
          </div>
        </div>
        <div class="stat-card-admin">
          <div class="stat-icon-admin" style="background: linear-gradient(135deg, #a855f7, #f97316);">🤖</div>
          <div class="stat-content-admin">
            <h3 class="stat-number" data-target="${stats.avg_ai_confidence}">0</h3>
            <p>Avg AI Confidence</p>
            <span class="stat-trend">${stats.low_confidence_count} low confidence</span>
          </div>
        </div>
      `;
      
      // Animate counters
      animateCounters();
      
      // Load recent tickets
      loadRecentTickets();
      
    } catch (error) {
      showToast('Failed to load overview', 'error');
    }
  }

  // Animate counters
  function animateCounters() {
    document.querySelectorAll('.stat-number').forEach(el => {
      const target = parseInt(el.dataset.target);
      const duration = 1000;
      const increment = target / (duration / 16);
      let current = 0;

      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          el.textContent = target;
          clearInterval(timer);
        } else {
          el.textContent = Math.floor(current);
        }
      }, 16);
    });
  }

  // Load recent tickets
  async function loadRecentTickets() {
    try {
      const response = await fetch(`${API_ENDPOINTS.adminTickets}?per_page=5`, {
        headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
      });
      const data = await response.json();
      
      const html = data.tickets.map(ticket => `
        <div class="recent-ticket-item">
          <div>
            <strong>${ticket.title}</strong>
            <div style="font-size: 0.875rem; color: rgba(255,255,255,0.6); margin-top: 0.25rem;">
              ${ticket.user_email} • ${new Date(ticket.created_at).toLocaleDateString()}
            </div>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <span class="priority-badge priority-${ticket.priority}">${ticket.priority.toUpperCase()}</span>
            <span class="status-badge status-${ticket.status}">${ticket.status.replace('_', ' ').toUpperCase()}</span>
          </div>
        </div>
      `).join('');
      
      document.getElementById('recentTicketsTable').innerHTML = html || '<p style="text-align: center; color: rgba(255,255,255,0.5);">No recent tickets</p>';
      
    } catch (error) {
      console.error('Failed to load recent tickets:', error);
    }
  }

  // Load Tickets
  window.loadTickets = async function(page = 1) {
    try {
      const search = document.getElementById('ticketSearch').value;
      const status = document.getElementById('statusFilter').value;
      const priority = document.getElementById('priorityFilter').value;
      const category = document.getElementById('categoryFilter').value;
      
      const params = new URLSearchParams({
        page,
        per_page: 20,
        ...(search && { search }),
        ...(status && { status }),
        ...(priority && { priority }),
        ...(category && { category })
      });
      
      const response = await fetch(`${API_ENDPOINTS.adminTickets}?${params}`, {
        headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
      });
      const data = await response.json();
      
      renderTicketsTable(data.tickets);
      renderPagination('ticketsPagination', data.current_page, data.pages, loadTickets);
      
    } catch (error) {
      showToast('Failed to load tickets', 'error');
    }
  };

  // Render tickets table
  function renderTicketsTable(tickets) {
    const tbody = document.getElementById('ticketsTableBody');
    
    if (!tickets.length) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.5);">No tickets found</td></tr>';
      return;
    }
    
    tbody.innerHTML = tickets.map(ticket => `
      <tr>
        <td><input type="checkbox" class="ticket-checkbox" value="${ticket.id}" onchange="updateSelection()"></td>
        <td><code>${ticket.id.substring(0, 8)}</code></td>
        <td>${ticket.user_email}</td>
        <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">${ticket.title}</td>
        <td>${ticket.category}</td>
        <td>
          <select class="inline-select priority-${ticket.priority}" onchange="updateTicketPriority('${ticket.id}', this.value)">
            <option value="low" ${ticket.priority === 'low' ? 'selected' : ''}>Low</option>
            <option value="medium" ${ticket.priority === 'medium' ? 'selected' : ''}>Medium</option>
            <option value="high" ${ticket.priority === 'high' ? 'selected' : ''}>High</option>
          </select>
        </td>
        <td>
          <select class="inline-select status-${ticket.status}" onchange="updateTicketStatus('${ticket.id}', this.value)">
            <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
            <option value="in_progress" ${ticket.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
            <option value="resolved" ${ticket.status === 'resolved' ? 'selected' : ''}>Resolved</option>
            <option value="closed" ${ticket.status === 'closed' ? 'selected' : ''}>Closed</option>
          </select>
        </td>
        <td>${Math.round(ticket.ai_confidence * 100)}%</td>
        <td>${new Date(ticket.created_at).toLocaleDateString()}</td>
        <td>
          <button class="btn-icon" onclick="viewTicket('${ticket.id}')" title="View">👁️</button>
          <button class="btn-icon" onclick="deleteTicket('${ticket.id}')" title="Delete">🗑️</button>
        </td>
      </tr>
    `).join('');
  }

  // Update ticket status
  window.updateTicketStatus = async function(ticketId, status) {
    try {
      const response = await fetch(API_ENDPOINTS.adminTicket(ticketId), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authUtils.getToken()}`
        },
        body: JSON.stringify({ status })
      });
      
      if (response.ok) {
        showToast('Status updated', 'success');
      }
    } catch (error) {
      showToast('Failed to update status', 'error');
    }
  };

  // Update ticket priority
  window.updateTicketPriority = async function(ticketId, priority) {
    try {
      const response = await fetch(API_ENDPOINTS.adminTicket(ticketId), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authUtils.getToken()}`
        },
        body: JSON.stringify({ priority })
      });
      
      if (response.ok) {
        showToast('Priority updated', 'success');
      }
    } catch (error) {
      showToast('Failed to update priority', 'error');
    }
  };

  // Delete ticket
  window.deleteTicket = async function(ticketId) {
    if (!confirm('Are you sure you want to delete this ticket?')) return;
    
    try {
      const response = await fetch(API_ENDPOINTS.adminTicket(ticketId), {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
      });
      
      if (response.ok) {
        showToast('Ticket deleted', 'success');
        loadTickets();
      }
    } catch (error) {
      showToast('Failed to delete ticket', 'error');
    }
  };

  // View ticket
  window.viewTicket = function(ticketId) {
    window.location.href = `ticket-details.html?id=${ticketId}`;
  };

  // Toggle select all
  window.toggleSelectAll = function() {
    const checked = document.getElementById('selectAll').checked;
    document.querySelectorAll('.ticket-checkbox').forEach(cb => {
      cb.checked = checked;
    });
    updateSelection();
  };

  // Update selection
  window.updateSelection = function() {
    selectedTickets.clear();
    document.querySelectorAll('.ticket-checkbox:checked').forEach(cb => {
      selectedTickets.add(cb.value);
    });
    
    const bulkActions = document.getElementById('bulkActions');
    const selectedCount = document.getElementById('selectedCount');
    
    if (selectedTickets.size > 0) {
      bulkActions.style.display = 'flex';
      selectedCount.textContent = `${selectedTickets.size} selected`;
    } else {
      bulkActions.style.display = 'none';
    }
  };

  // Bulk update status
  window.bulkUpdateStatus = async function(status) {
    if (selectedTickets.size === 0) return;
    
    try {
      const response = await fetch(API_ENDPOINTS.adminBulkUpdate, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authUtils.getToken()}`
        },
        body: JSON.stringify({
          ticket_ids: Array.from(selectedTickets),
          updates: { status }
        })
      });
      
      if (response.ok) {
        showToast('Tickets updated', 'success');
        selectedTickets.clear();
        loadTickets();
      }
    } catch (error) {
      showToast('Failed to update tickets', 'error');
    }
  };

  // Bulk update priority
  window.bulkUpdatePriority = async function(priority) {
    if (selectedTickets.size === 0) return;
    
    try {
      const response = await fetch(API_ENDPOINTS.adminBulkUpdate, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authUtils.getToken()}`
        },
        body: JSON.stringify({
          ticket_ids: Array.from(selectedTickets),
          updates: { priority }
        })
      });
      
      if (response.ok) {
        showToast('Tickets updated', 'success');
        selectedTickets.clear();
        loadTickets();
      }
    } catch (error) {
      showToast('Failed to update tickets', 'error');
    }
  };

  // Bulk delete
  window.bulkDelete = async function() {
    if (selectedTickets.size === 0) return;
    if (!confirm(`Delete ${selectedTickets.size} tickets?`)) return;
    
    try {
      const promises = Array.from(selectedTickets).map(id =>
        fetch(API_ENDPOINTS.adminTicket(id), {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
        })
      );
      
      await Promise.all(promises);
      showToast('Tickets deleted', 'success');
      selectedTickets.clear();
      loadTickets();
    } catch (error) {
      showToast('Failed to delete tickets', 'error');
    }
  };

  // Load Analytics
  async function loadAnalytics() {
    try {
      const response = await fetch(API_ENDPOINTS.adminAnalytics, {
        headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
      });
      const data = await response.json();
      
      // Tickets Timeline Chart
      createTimelineChart(data.tickets_timeline);
      
      // Category Chart
      createCategoryChart(data.categories);
      
      // Priority Chart
      createPriorityChart(data.priorities);
      
      // Status Chart
      createStatusChart(data.statuses);
      
    } catch (error) {
      showToast('Failed to load analytics', 'error');
    }
  }

  // Create timeline chart
  function createTimelineChart(timeline) {
    const ctx = document.getElementById('ticketsTimelineChart');
    if (charts.timeline) charts.timeline.destroy();
    
    charts.timeline = new Chart(ctx, {
      type: 'line',
      data: {
        labels: timeline.map(t => new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
        datasets: [{
          label: 'Tickets Created',
          data: timeline.map(t => t.count),
          borderColor: '#a855f7',
          backgroundColor: 'rg