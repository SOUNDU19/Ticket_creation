// Enterprise Admin Dashboard JavaScript
if (!authUtils.protectAdminPage()) throw new Error('Unauthorized');

let currentTicketId = null;
let elevatedToken = null;
let elevatedTimer = null;

// Section Navigation
function showSection(section) {
  document.querySelectorAll('.section-content').forEach(el => el.style.display = 'none');
  document.querySelectorAll('.admin-sidebar-item').forEach(el => el.classList.remove('active'));
  
  document.getElementById(`${section}-section`).style.display = 'block';
  event.target.classList.add('active');
  
  // Load section data
  switch(section) {
    case 'overview':
      loadOverview();
      break;
    case 'tickets':
      loadTickets();
      break;
    case 'users':
      loadUsers();
      break;
    case 'analytics':
      loadAnalytics();
      break;
    case 'sla':
      loadSLABreaches();
      break;
    case 'audit':
      loadAuditLogs();
      break;
    case 'settings':
      loadSettings();
      break;
  }
}

// Elevated Privilege Mode
async function requestElevatedPrivilege() {
  const password = prompt('Enter your admin password to enable elevated privilege mode:');
  if (!password) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/verify-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      elevatedToken = data.elevated_token;
      showElevatedBanner(data.expires_in);
      showToast('Elevated privilege mode activated', 'success');
    } else {
      showToast(data.error || 'Invalid password', 'error');
    }
  } catch (error) {
    showToast('Failed to verify password', 'error');
  }
}

function showElevatedBanner(expiresIn) {
  const banner = document.getElementById('elevatedBanner');
  banner.style.display = 'flex';
  
  let remaining = expiresIn;
  elevatedTimer = setInterval(() => {
    remaining--;
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    document.getElementById('elevatedTimer').textContent = 
      `Expires in: ${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    if (remaining <= 0) {
      clearInterval(elevatedTimer);
      banner.style.display = 'none';
      elevatedToken = null;
      showToast('Elevated privilege mode expired', 'warning');
    }
  }, 1000);
}

// Load Overview
async function loadOverview() {
  try {
    const analytics = await fetch(`${API_BASE_URL}/admin/advanced-analytics`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    }).then(r => r.json());
    
    // Display stats
    document.getElementById('overviewStats').innerHTML = `
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">🎫</div>
        <div class="stat-content">
          <h3>${analytics.total_tickets}</h3>
          <p>Total Tickets</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb, #f5576c);">✅</div>
        <div class="stat-content">
          <h3>${analytics.resolved_tickets}</h3>
          <p>Resolved</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">⏱️</div>
        <div class="stat-content">
          <h3>${analytics.avg_resolution_time_hours}h</h3>
          <p>Avg Resolution Time</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a, #fee140);">🤖</div>
        <div class="stat-content">
          <h3>${analytics.ai_accuracy}%</h3>
          <p>AI Accuracy</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #a8edea, #fed6e3);">📊</div>
        <div class="stat-content">
          <h3>${analytics.sla_breach_rate}%</h3>
          <p>SLA Breach Rate</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #ff9a9e, #fecfef);">⚠️</div>
        <div class="stat-content">
          <h3>${analytics.breached_tickets}</h3>
          <p>Breached Tickets</p>
        </div>
      </div>
    `;
    
    // Ticket Growth Chart
    const growthCtx = document.getElementById('ticketGrowthChart').getContext('2d');
    new Chart(growthCtx, {
      type: 'line',
      data: {
        labels: analytics.ticket_growth.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
        datasets: [{
          label: 'Tickets Created',
          data: analytics.ticket_growth.map(d => d.count),
          borderColor: '#a855f7',
          backgroundColor: 'rgba(168, 85, 247, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#fff' } },
          x: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#fff' } }
        }
      }
    });
    
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(analytics.category_distribution),
        datasets: [{
          data: Object.values(analytics.category_distribution),
          backgroundColor: ['#a855f7', '#f97316', '#3b82f6', '#22c55e', '#eab308']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom', labels: { color: '#fff' } } }
      }
    });
    
    // Priority Chart
    const priorityCtx = document.getElementById('priorityChart').getContext('2d');
    new Chart(priorityCtx, {
      type: 'bar',
      data: {
        labels: Object.keys(analytics.priority_distribution).map(p => p.toUpperCase()),
        datasets: [{
          label: 'Tickets',
          data: Object.values(analytics.priority_distribution),
          backgroundColor: ['#dc2626', '#f97316', '#eab308', '#22c55e']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#fff' } },
          x: { grid: { display: false }, ticks: { color: '#fff' } }
        }
      }
    });
    
  } catch (error) {
    showToast('Failed to load overview', 'error');
  }
}

// Load Tickets
async function loadTickets() {
  try {
    const search = document.getElementById('ticketSearch')?.value || '';
    const status = document.getElementById('statusFilter')?.value || '';
    const priority = document.getElementById('priorityFilter')?.value || '';
    
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    if (priority) params.append('priority', priority);
    
    const response = await fetch(`${API_BASE_URL}/admin/tickets?${params}`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    
    const data = await response.json();
    const tbody = document.getElementById('ticketsTable');
    
    if (data.tickets.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem;">No tickets found</td></tr>';
      return;
    }
    
    tbody.innerHTML = data.tickets.map(ticket => `
      <tr>
        <td style="font-family: monospace;">#${ticket.id.substring(0, 8)}</td>
        <td>${ticket.user_name}</td>
        <td style="font-weight: 600;">${ticket.title}</td>
        <td>${ticket.category}</td>
        <td><span class="badge badge-${getPriorityColor(ticket.priority)}">${ticket.priority.toUpperCase()}</span></td>
        <td><span class="badge badge-${getStatusColor(ticket.status)}">${ticket.status.replace('_', ' ').toUpperCase()}</span></td>
        <td>
          <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;" onclick="openTicketModal('${ticket.id}')">View</button>
        </td>
      </tr>
    `).join('');
    
  } catch (error) {
    showToast('Failed to load tickets', 'error');
  }
}

async function loadSLAStatus(ticketId) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/sla-status`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    const badge = document.getElementById(`sla-${ticketId}`);
    
    if (badge) {
      if (data.sla.status === 'met') {
        badge.className = 'sla-badge active';
        badge.textContent = '✓ Met';
      } else if (data.sla.is_breached) {
        badge.className = 'sla-badge breached';
        badge.textContent = `⚠ Breached`;
      } else {
        badge.className = 'sla-badge active';
        badge.textContent = `${data.sla.time_remaining_hours}h left`;
      }
    }
  } catch (error) {
    console.error('Failed to load SLA status:', error);
  }
}

function getPriorityColor(priority) {
  const colors = { critical: 'danger', high: 'danger', medium: 'warning', low: 'success' };
  return colors[priority] || 'primary';
}

function getStatusColor(status) {
  const colors = { open: 'primary', in_progress: 'warning', resolved: 'success', closed: 'success' };
  return colors[status] || 'primary';
}

// Ticket Modal Functions
async function openTicketModal(ticketId) {
  console.log('Opening ticket modal for ID:', ticketId);
  currentTicketId = ticketId;
  document.getElementById('ticketModal').classList.add('active');
  
  // Show loading state
  document.getElementById('ticketDetails').innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="loading-spinner"></div><p>Loading ticket details...</p></div>';
  
  // Load all tabs data
  try {
    await Promise.all([
      loadTicketDetails(ticketId),
      loadTicketTimeline(ticketId),
      loadInternalNotes(ticketId),
      loadUserContext(ticketId)
    ]);
  } catch (error) {
    console.error('Error loading ticket modal data:', error);
  }
}

function closeTicketModal() {
  document.getElementById('ticketModal').classList.remove('active');
  currentTicketId = null;
}

function switchTab(tabName) {
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  
  event.target.classList.add('active');
  document.getElementById(`${tabName}-tab`).classList.add('active');
}

async function loadTicketDetails(ticketId) {
  console.log('Loading ticket details for ID:', ticketId);
  try {
    const url = `${API_BASE_URL}/admin/ticket/${ticketId}`;
    console.log('Fetching from URL:', url);
    
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error response:', errorData);
      throw new Error(errorData.error || 'Failed to fetch ticket details');
    }
    
    const data = await response.json();
    console.log('Ticket data received:', data);
    const ticket = data.ticket;
    
    if (!ticket) {
      throw new Error('Ticket data not found in response');
    }
    
    console.log('Rendering ticket details...');
    document.getElementById('modalTicketTitle').textContent = `Ticket #${ticket.id.substring(0, 8)}`;
    document.getElementById('ticketDetails').innerHTML = `
      <div style="display: grid; gap: 1.5rem;">
        <div>
          <h3 style="margin-bottom: 0.5rem;">${ticket.title || 'No title'}</h3>
          <p style="color: rgba(255, 255, 255, 0.7);">${ticket.description || 'No description'}</p>
        </div>
        
        ${ticket.overridden_by_admin ? `
          <div style="background: rgba(249, 115, 22, 0.2); padding: 1rem; border-radius: 8px; border-left: 3px solid #f97316;">
            <strong>⚠️ AI Override</strong>
            <p style="margin: 0.5rem 0 0; font-size: 0.875rem;">
              Original AI Category: ${ticket.original_ai_category || 'N/A'} → Changed to: ${ticket.category}
            </p>
          </div>
        ` : ''}
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div>
            <label style="color: rgba(255, 255, 255, 0.6); font-size: 0.875rem;">Category</label>
            <p style="font-weight: 600;">${ticket.category || 'N/A'}</p>
          </div>
          <div>
            <label style="color: rgba(255, 255, 255, 0.6); font-size: 0.875rem;">Priority</label>
            <p><span class="badge badge-${getPriorityColor(ticket.priority)}">${(ticket.priority || 'medium').toUpperCase()}</span></p>
          </div>
          <div>
            <label style="color: rgba(255, 255, 255, 0.6); font-size: 0.875rem;">Status</label>
            <p><span class="badge badge-${getStatusColor(ticket.status)}">${(ticket.status || 'open').replace('_', ' ').toUpperCase()}</span></p>
          </div>
          <div>
            <label style="color: rgba(255, 255, 255, 0.6); font-size: 0.875rem;">AI Confidence</label>
            <p style="font-weight: 600;">${Math.round((ticket.ai_confidence || 0) * 100)}%</p>
          </div>
        </div>
        
        <div style="background: rgba(168, 85, 247, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.3);">
          <label style="color: rgba(255, 255, 255, 0.9); font-size: 0.95rem; font-weight: 600; display: block; margin-bottom: 0.75rem;">Update Ticket Status</label>
          <div style="display: flex; gap: 1rem; align-items: center;">
            <select id="statusUpdateSelect" class="form-input" style="flex: 1; max-width: 300px;">
              <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
              <option value="in_progress" ${ticket.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
              <option value="resolved" ${ticket.status === 'resolved' ? 'selected' : ''}>Resolved</option>
              <option value="closed" ${ticket.status === 'closed' ? 'selected' : ''}>Closed</option>
            </select>
            <button class="btn btn-primary" onclick="updateTicketStatus('${ticket.id}')" style="white-space: nowrap;">
              Update Status
            </button>
          </div>
        </div>
        
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="overrideCategory('${ticket.id}')">Override Category</button>
          <button class="btn btn-primary" onclick="assignTicket('${ticket.id}')">Assign Ticket</button>
          <button class="btn btn-secondary" onclick="mergeTicket('${ticket.id}')">Merge Ticket</button>
        </div>
      </div>
    `;
  } catch (error) {
    console.error('Error loading ticket details:', error);
    document.getElementById('ticketDetails').innerHTML = `
      <div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7);">
        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">⚠️ Failed to load ticket details</p>
        <p style="font-size: 0.9rem;">${error.message}</p>
        <button class="btn btn-secondary" onclick="closeTicketModal()" style="margin-top: 1rem;">Close</button>
      </div>
    `;
    showToast('Failed to load ticket details', 'error');
  }
}

async function loadTicketTimeline(ticketId) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/timeline`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    document.getElementById('ticketTimeline').innerHTML = data.timeline.map(item => `
      <div class="timeline-item">
        <div class="timeline-icon">${item.icon}</div>
        <div class="timeline-content">
          <h4 style="margin: 0 0 0.5rem;">${item.title}</h4>
          <p style="margin: 0; color: rgba(255, 255, 255, 0.7); font-size: 0.875rem;">${item.description}</p>
          <p style="margin: 0.5rem 0 0; color: rgba(255, 255, 255, 0.5); font-size: 0.75rem;">
            ${new Date(item.timestamp).toLocaleString()}
          </p>
        </div>
      </div>
    `).join('');
  } catch (error) {
    showToast('Failed to load timeline', 'error');
  }
}

async function loadInternalNotes(ticketId) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/internal-notes`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    const notesList = document.getElementById('internalNotesList');
    if (data.notes.length === 0) {
      notesList.innerHTML = '<p style="text-align: center; color: rgba(255, 255, 255, 0.5);">No internal notes yet</p>';
      return;
    }
    
    notesList.innerHTML = data.notes.map(note => `
      <div class="note-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
          <div>
            <strong>${note.admin_name}</strong>
            <span style="color: rgba(255, 255, 255, 0.5); font-size: 0.875rem; margin-left: 0.5rem;">
              ${new Date(note.created_at).toLocaleString()}
            </span>
          </div>
          <button class="btn btn-secondary" style="padding: 0.25rem 0.75rem; font-size: 0.75rem;" 
                  onclick="deleteInternalNote('${ticketId}', '${note.id}')">Delete</button>
        </div>
        <p style="margin: 0; white-space: pre-wrap;">${note.note}</p>
      </div>
    `).join('');
  } catch (error) {
    showToast('Failed to load internal notes', 'error');
  }
}

async function addInternalNote(event) {
  event.preventDefault();
  const noteText = document.getElementById('newNoteText').value;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${currentTicketId}/internal-notes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ note: noteText })
    });
    
    if (response.ok) {
      document.getElementById('newNoteText').value = '';
      await loadInternalNotes(currentTicketId);
      showToast('Internal note added', 'success');
    } else {
      showToast('Failed to add note', 'error');
    }
  } catch (error) {
    showToast('Failed to add note', 'error');
  }
}

async function deleteInternalNote(ticketId, noteId) {
  if (!confirm('Delete this internal note?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/internal-notes/${noteId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    
    if (response.ok) {
      await loadInternalNotes(ticketId);
      showToast('Note deleted', 'success');
    } else {
      showToast('Failed to delete note', 'error');
    }
  } catch (error) {
    showToast('Failed to delete note', 'error');
  }
}

async function loadUserContext(ticketId) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/user-context`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    document.getElementById('userContext').innerHTML = `
      <div class="user-context-panel">
        <h3 style="margin-bottom: 1.5rem;">User Information</h3>
        
        <div style="display: grid; gap: 1rem; margin-bottom: 2rem;">
          <div><strong>Name:</strong> ${data.user.name}</div>
          <div><strong>Email:</strong> ${data.user.email}</div>
          <div><strong>Company:</strong> ${data.user.company || 'N/A'}</div>
          <div><strong>Department:</strong> ${data.user.department || 'N/A'}</div>
          <div><strong>Account Created:</strong> ${new Date(data.user.created_at).toLocaleDateString()}</div>
          <div><strong>Last Login:</strong> ${data.user.last_login ? new Date(data.user.last_login).toLocaleString() : 'Never'}</div>
        </div>
        
        <h4 style="margin-bottom: 1rem;">Statistics</h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
          <div style="background: rgba(168, 85, 247, 0.1); padding: 1rem; border-radius: 8px;">
            <div style="font-size: 1.5rem; font-weight: 600;">${data.statistics.total_tickets}</div>
            <div style="font-size: 0.875rem; color: rgba(255, 255, 255, 0.7);">Total Tickets</div>
          </div>
          <div style="background: rgba(249, 115, 22, 0.1); padding: 1rem; border-radius: 8px;">
            <div style="font-size: 1.5rem; font-weight: 600;">${data.statistics.open_tickets}</div>
            <div style="font-size: 0.875rem; color: rgba(255, 255, 255, 0.7);">Open Tickets</div>
          </div>
          <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px;">
            <div style="font-size: 1.5rem; font-weight: 600;">${data.statistics.high_priority_tickets}</div>
            <div style="font-size: 0.875rem; color: rgba(255, 255, 255, 0.7);">High Priority</div>
          </div>
          <div style="background: rgba(34, 197, 94, 0.1); padding: 1rem; border-radius: 8px;">
            <div style="font-size: 1.5rem; font-weight: 600;">${data.statistics.avg_ai_confidence}%</div>
            <div style="font-size: 0.875rem; color: rgba(255, 255, 255, 0.7);">Avg AI Confidence</div>
          </div>
        </div>
        
        <button class="btn btn-primary" style="margin-top: 1.5rem;" onclick="impersonateUser('${data.user.id}')">
          👤 Impersonate User
        </button>
      </div>
    `;
  } catch (error) {
    showToast('Failed to load user context', 'error');
  }
}

// Admin Actions
async function overrideCategory(ticketId) {
  const newCategory = prompt('Enter new category:\n- Technical\n- Billing\n- Account\n- General Inquiry\n- Fraud');
  if (!newCategory) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/override-category`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ category: newCategory })
    });
    
    if (response.ok) {
      await loadTicketDetails(ticketId);
      await loadTicketTimeline(ticketId);
      showToast('Category overridden successfully', 'success');
    } else {
      showToast('Failed to override category', 'error');
    }
  } catch (error) {
    showToast('Failed to override category', 'error');
  }
}

async function assignTicket(ticketId) {
  const assigneeId = prompt('Enter admin user ID to assign (or leave empty to unassign):');
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${ticketId}/assign`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ assignee_id: assigneeId || null })
    });
    
    if (response.ok) {
      showToast('Ticket assigned successfully', 'success');
    } else {
      showToast('Failed to assign ticket', 'error');
    }
  } catch (error) {
    showToast('Failed to assign ticket', 'error');
  }
}

async function mergeTicket(sourceTicketId) {
  const targetTicketId = prompt('Enter target ticket ID to merge into:');
  if (!targetTicketId) return;
  
  if (!confirm(`Merge ticket #${sourceTicketId.substring(0, 8)} into #${targetTicketId.substring(0, 8)}?`)) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/ticket/${sourceTicketId}/merge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ target_ticket_id: targetTicketId })
    });
    
    if (response.ok) {
      closeTicketModal();
      loadTickets();
      showToast('Tickets merged successfully', 'success');
    } else {
      const data = await response.json();
      showToast(data.error || 'Failed to merge tickets', 'error');
    }
  } catch (error) {
    showToast('Failed to merge tickets', 'error');
  }
}

// Update Ticket Status
async function updateTicketStatus(ticketId) {
  const newStatus = document.getElementById('statusUpdateSelect').value;
  
  if (!newStatus) {
    showToast('Please select a status', 'warning');
    return;
  }
  
  if (!confirm(`Update ticket status to "${newStatus.replace('_', ' ').toUpperCase()}"?`)) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/update-ticket`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ 
        ticket_id: ticketId,
        status: newStatus 
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      showToast('Ticket status updated successfully', 'success');
      closeTicketModal();
      
      // Reload the currently visible section
      const sections = ['overview', 'tickets', 'users', 'analytics', 'sla', 'audit', 'settings'];
      for (const section of sections) {
        const sectionEl = document.getElementById(`${section}-section`);
        if (sectionEl && sectionEl.style.display !== 'none') {
          // Reload the visible section
          switch(section) {
            case 'overview':
              loadOverview();
              break;
            case 'tickets':
              loadTickets();
              break;
            case 'users':
              loadUsers();
              break;
            case 'analytics':
              loadAnalytics();
              break;
            case 'sla':
              loadSLABreaches();
              break;
          }
          break;
        }
      }
    } else {
      showToast(data.error || 'Failed to update ticket status', 'error');
    }
  } catch (error) {
    showToast('Failed to update ticket status', 'error');
  }
}

async function impersonateUser(userId) {
  if (!confirm('Start impersonation mode for this user?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/impersonate/${userId}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store impersonation token
      localStorage.setItem('impersonation_token', data.impersonation_token);
      localStorage.setItem('impersonated_user', JSON.stringify(data.user));
      
      // Show banner and redirect
      showToast('Impersonation started', 'success');
      window.location.href = 'dashboard.html';
    } else {
      showToast(data.error || 'Failed to start impersonation', 'error');
    }
  } catch (error) {
    showToast('Failed to start impersonation', 'error');
  }
}

function exitImpersonation() {
  localStorage.removeItem('impersonation_token');
  localStorage.removeItem('impersonated_user');
  window.location.reload();
}

// Load Users
async function loadUsers() {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/users`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = data.users.map(user => `
      <tr>
        <td style="font-weight: 600;">${user.name}</td>
        <td>${user.email}</td>
        <td>${user.company || 'N/A'}</td>
        <td>${user.ticket_count} (${user.open_tickets} open)</td>
        <td><span class="badge badge-${user.is_active ? 'success' : 'danger'}">${user.is_active ? 'Active' : 'Inactive'}</span></td>
        <td>
          <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.875rem;" 
                  onclick="toggleUserStatus('${user.id}', ${user.is_active})">
            ${user.is_active ? 'Deactivate' : 'Activate'}
          </button>
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showToast('Failed to load users', 'error');
  }
}

async function toggleUserStatus(userId, currentStatus) {
  const action = currentStatus ? 'deactivate' : 'activate';
  if (!confirm(`${action.charAt(0).toUpperCase() + action.slice(1)} this user?`)) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authUtils.getToken()}`
      },
      body: JSON.stringify({ is_active: !currentStatus })
    });
    
    if (response.ok) {
      loadUsers();
      showToast(`User ${action}d successfully`, 'success');
    } else {
      showToast(`Failed to ${action} user`, 'error');
    }
  } catch (error) {
    showToast(`Failed to ${action} user`, 'error');
  }
}

// Load Analytics
async function loadAnalytics() {
  try {
    const analytics = await fetch(`${API_BASE_URL}/admin/advanced-analytics`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    }).then(r => r.json());
    
    document.getElementById('analyticsStats').innerHTML = `
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">📊</div>
        <div class="stat-content">
          <h3>${analytics.total_tickets}</h3>
          <p>Total Tickets</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb, #f5576c);">✅</div>
        <div class="stat-content">
          <h3>${analytics.resolved_tickets}</h3>
          <p>Resolved Tickets</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">⏱️</div>
        <div class="stat-content">
          <h3>${analytics.avg_resolution_time_hours}h</h3>
          <p>Avg Resolution Time</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a, #fee140);">🤖</div>
        <div class="stat-content">
          <h3>${analytics.ai_accuracy}%</h3>
          <p>AI Accuracy</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #a8edea, #fed6e3);">📈</div>
        <div class="stat-content">
          <h3>${analytics.sla_breach_rate}%</h3>
          <p>SLA Breach Rate</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #ff9a9e, #fecfef);">⚠️</div>
        <div class="stat-content">
          <h3>${analytics.breached_tickets}</h3>
          <p>Breached Tickets</p>
        </div>
      </div>
    `;
  } catch (error) {
    showToast('Failed to load analytics', 'error');
  }
}

// Load SLA Breaches
async function loadSLABreaches() {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/sla-breaches`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    const container = document.getElementById('slaBreaches');
    
    if (data.breached_tickets.length === 0) {
      container.innerHTML = `
        <div class="glass-container" style="text-align: center; padding: 3rem;">
          <h3 style="color: #22c55e; margin-bottom: 1rem;">✅ No SLA Breaches</h3>
          <p style="color: rgba(255, 255, 255, 0.7);">All tickets are within SLA limits</p>
        </div>
      `;
      return;
    }
    
    container.innerHTML = `
      <div class="glass-container">
        <h3 style="margin-bottom: 1.5rem; color: #ef4444;">⚠️ ${data.count} SLA Breaches</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Ticket</th>
                <th>User</th>
                <th>Priority</th>
                <th>Created</th>
                <th>Overdue By</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              ${data.breached_tickets.map(ticket => `
                <tr>
                  <td style="font-family: monospace;">#${ticket.id.substring(0, 8)}</td>
                  <td>${ticket.user_name}</td>
                  <td><span class="badge badge-danger">${ticket.priority.toUpperCase()}</span></td>
                  <td>${new Date(ticket.created_at).toLocaleString()}</td>
                  <td style="color: #ef4444; font-weight: 600;">${Math.abs(ticket.sla.time_remaining_hours)}h</td>
                  <td>
                    <button class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.875rem;" 
                            onclick="openTicketModal('${ticket.id}')">View</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } catch (error) {
    showToast('Failed to load SLA breaches', 'error');
  }
}

// Load Audit Logs
async function loadAuditLogs() {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/audit-logs`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    
    const tbody = document.getElementById('auditLogsTable');
    tbody.innerHTML = data.logs.map(log => `
      <tr>
        <td>${new Date(log.timestamp).toLocaleString()}</td>
        <td>${log.admin_name}</td>
        <td><span class="badge badge-primary">${log.action.replace(/_/g, ' ').toUpperCase()}</span></td>
        <td>${log.target_type} ${log.target_id ? `#${log.target_id.substring(0, 8)}` : ''}</td>
        <td style="font-size: 0.875rem; color: rgba(255, 255, 255, 0.7);">
          ${log.details ? log.details.substring(0, 50) + '...' : 'N/A'}
        </td>
      </tr>
    `).join('');
  } catch (error) {
    showToast('Failed to load audit logs', 'error');
  }
}

// Load Settings
async function loadSettings() {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/settings`, {
      headers: { 'Authorization': `Bearer ${authUtils.getToken()}` }
    });
    const data = await response.json();
    const settings = data.settings;
    
    document.getElementById('sla_critical').value = settings.sla_critical_hours;
    document.getElementById('sla_high').value = settings.sla_high_hours;
    document.getElementById('sla_medium').value = settings.sla_medium_hours;
    document.getElementById('sla_low').value = settings.sla_low_hours;
    document.getElementById('ai_threshold').value = settings.ai_confidence_threshold;
    document.getElementById('duplicate_detection').checked = settings.duplicate_detection_enabled;
  } catch (error) {
    showToast('Failed to load settings', 'error');
  }
}

async function saveSettings(event) {
  event.preventDefault();
  
  if (!elevatedToken) {
    showToast('Elevated privilege required to change settings', 'error');
    return;
  }
  
  const settings = {
    sla_critical_hours: parseInt(document.getElementById('sla_critical').value),
    sla_high_hours: parseInt(document.getElementById('sla_high').value),
    sla_medium_hours: parseInt(document.getElementById('sla_medium').value),
    sla_low_hours: parseInt(document.getElementById('sla_low').value),
    ai_confidence_threshold: parseFloat(document.getElementById('ai_threshold').value),
    duplicate_detection_enabled: document.getElementById('duplicate_detection').checked
  };
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${elevatedToken}`
      },
      body: JSON.stringify(settings)
    });
    
    if (response.ok) {
      showToast('Settings saved successfully', 'success');
    } else {
      showToast('Failed to save settings', 'error');
    }
  } catch (error) {
    showToast('Failed to save settings', 'error');
  }
}

// Toast notification
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    top: 100px;
    right: 20px;
    background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    z-index: 10000;
    animation: slideIn 0.3s ease;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Initialize
loadOverview();

// Check for impersonation mode
const impersonatedUser = localStorage.getItem('impersonated_user');
if (impersonatedUser) {
  const user = JSON.parse(impersonatedUser);
  document.getElementById('impersonationBanner').style.display = 'flex';
  document.getElementById('impersonatedUserName').textContent = user.name;
}
