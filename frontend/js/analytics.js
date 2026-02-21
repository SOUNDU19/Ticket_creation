// Analytics Page Logic
(function() {
  'use strict';

  // Protect page
  if (!authUtils.protectPage()) {
    throw new Error('Unauthorized');
  }

  let charts = {};

  // Load all analytics on page load
  document.addEventListener('DOMContentLoaded', () => {
    loadAllAnalytics();
    setupEventListeners();
  });

  // Setup event listeners
  function setupEventListeners() {
    document.getElementById('dateFilter').addEventListener('change', () => {
      // Date filter functionality can be added later
      showToast('Date filtering coming soon!', 'info');
    });
  }

  // Load all analytics data
  async function loadAllAnalytics() {
    try {
      // First check if user has any tickets
      const overviewResponse = await fetch(API_ENDPOINTS.analyticsOverview, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (overviewResponse.ok) {
        const overviewData = await overviewResponse.json();
        
        // If no tickets, show message
        if (overviewData.total_tickets === 0) {
          showNoDataMessage();
          return;
        }
      }
      
      await Promise.all([
        loadOverview(),
        loadActivity(),
        loadCategoryDistribution(),
        loadPriorityDistribution(),
        loadAIInsights(),
        loadResolutionInsights(),
        loadMonthlySummary()
      ]);
    } catch (error) {
      console.error('Failed to load analytics:', error);
      showToast('Failed to load analytics data. Please try again.', 'error');
    }
  }
  
  // Show no data message
  function showNoDataMessage() {
    // Hide all stat cards and charts
    document.querySelectorAll('.stats-grid, .glass-container').forEach(el => {
      el.style.display = 'none';
    });
    
    // Show message
    const container = document.querySelector('.container');
    const message = document.createElement('div');
    message.style.cssText = 'text-align: center; padding: 4rem 2rem;';
    message.innerHTML = `
      <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">📊</div>
      <h2 style="font-size: 2rem; margin-bottom: 1rem;">No Analytics Data Yet</h2>
      <p style="color: rgba(255,255,255,0.7); margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
        Create some tickets to see your analytics dashboard come to life! Your ticket statistics, AI insights, and trends will appear here.
      </p>
      <a href="create-ticket.html" class="btn btn-primary" style="display: inline-block;">Create Your First Ticket</a>
    `;
    container.appendChild(message);
  }

  // Load overview stats
  async function loadOverview() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsOverview, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) {
        console.error('Overview fetch failed:', response.status);
        throw new Error('Failed to fetch overview');
      }
      
      const data = await response.json();
      
      // Animate counters
      animateCounter(document.getElementById('statTotal'), data.total_tickets || 0);
      animateCounter(document.getElementById('statOpen'), data.open_tickets || 0);
      animateCounter(document.getElementById('statInProgress'), data.in_progress || 0);
      animateCounter(document.getElementById('statClosed'), data.closed_tickets || 0);
      animateCounter(document.getElementById('statHighPriority'), data.high_priority_count || 0);
      
      const confidence = data.average_ai_confidence || 0;
      document.getElementById('statConfidence').textContent = confidence.toFixed(1) + '%';
      
    } catch (error) {
      console.error('Overview error:', error);
      // Set default values
      document.getElementById('statTotal').textContent = '0';
      document.getElementById('statOpen').textContent = '0';
      document.getElementById('statInProgress').textContent = '0';
      document.getElementById('statClosed').textContent = '0';
      document.getElementById('statHighPriority').textContent = '0';
      document.getElementById('statConfidence').textContent = '0%';
    }
  }

  // Load activity chart
  async function loadActivity() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsActivity, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) {
        console.error('Activity fetch failed:', response.status);
        throw new Error('Failed to fetch activity');
      }
      
      const data = await response.json();
      
      // Check if we have data
      if (!data || data.length === 0) {
        console.log('No activity data available');
        return;
      }
      
      const ctx = document.getElementById('activityChart').getContext('2d');
      
      if (charts.activity) charts.activity.destroy();
      
      charts.activity = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(d => {
            const date = new Date(d.date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }),
          datasets: [{
            label: 'Tickets Created',
            data: data.map(d => d.count),
            borderColor: '#a855f7',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#a855f7',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(31, 31, 31, 0.9)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: 'rgba(168, 85, 247, 0.5)',
              borderWidth: 1,
              padding: 12,
              displayColors: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)',
                stepSize: 1
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)',
                maxRotation: 45,
                minRotation: 45
              },
              grid: {
                display: false
              }
            }
          },
          animation: {
            duration: 1500,
            easing: 'easeInOutQuart'
          }
        }
      });
      
    } catch (error) {
      console.error('Activity error:', error);
    }
  }

  // Load category distribution
  async function loadCategoryDistribution() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsCategoryDist, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) {
        console.error('Category fetch failed:', response.status);
        throw new Error('Failed to fetch categories');
      }
      
      const data = await response.json();
      
      // Check if we have data
      if (!data || data.length === 0) {
        console.log('No category data available');
        return;
      }
      
      const ctx = document.getElementById('categoryChart').getContext('2d');
      
      if (charts.category) charts.category.destroy();
      
      const colors = [
        '#a855f7',
        '#f97316',
        '#3b82f6',
        '#10b981',
        '#f59e0b',
        '#ef4444'
      ];
      
      charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: data.map(d => d.category),
          datasets: [{
            data: data.map(d => d.count),
            backgroundColor: colors.slice(0, data.length),
            borderColor: '#0a0a0a',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#fff',
                padding: 15,
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(31, 31, 31, 0.9)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: 'rgba(168, 85, 247, 0.5)',
              borderWidth: 1,
              padding: 12
            }
          },
          animation: {
            animateRotate: true,
            animateScale: true,
            duration: 1500
          }
        }
      });
      
    } catch (error) {
      console.error('Category error:', error);
    }
  }

  // Load priority distribution
  async function loadPriorityDistribution() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsPriorityDist, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) {
        console.error('Priority fetch failed:', response.status);
        throw new Error('Failed to fetch priorities');
      }
      
      const data = await response.json();
      
      // Check if we have data
      if (!data || data.length === 0) {
        console.log('No priority data available');
        return;
      }
      
      const ctx = document.getElementById('priorityChart').getContext('2d');
      
      if (charts.priority) charts.priority.destroy();
      
      const priorityColors = {
        'Critical': '#dc2626',
        'High': '#ef4444',
        'Medium': '#f59e0b',
        'Low': '#10b981'
      };
      
      charts.priority = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(d => d.priority),
          datasets: [{
            label: 'Tickets',
            data: data.map(d => d.count),
            backgroundColor: data.map(d => priorityColors[d.priority] || '#6b7280'),
            borderRadius: 8,
            borderSkipped: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(31, 31, 31, 0.9)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: 'rgba(168, 85, 247, 0.5)',
              borderWidth: 1,
              padding: 12
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)',
                stepSize: 1
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
              },
              grid: {
                display: false
              }
            }
          },
          animation: {
            duration: 1500,
            easing: 'easeInOutQuart'
          }
        }
      });
      
    } catch (error) {
      console.error('Priority error:', error);
    }
  }

  // Load AI insights
  async function loadAIInsights() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsAIInsights, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch AI insights');
      
      const data = await response.json();
      
      document.getElementById('aiConfidence').textContent = data.average_confidence.toFixed(1) + '%';
      document.getElementById('lowConfidenceCount').textContent = data.low_confidence_count;
      document.getElementById('commonCategory').textContent = data.most_common_category;
      
      // Animate confidence bar
      setTimeout(() => {
        const bar = document.getElementById('aiConfidenceBar');
        bar.style.width = data.average_confidence + '%';
        
        if (data.average_confidence >= 85) {
          bar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
        } else if (data.average_confidence >= 60) {
          bar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
        } else {
          bar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
      }, 500);
      
      // Trend badge
      const trendBadge = document.getElementById('confidenceTrend');
      trendBadge.textContent = data.confidence_trend.charAt(0).toUpperCase() + data.confidence_trend.slice(1);
      trendBadge.className = 'trend-badge trend-' + data.confidence_trend;
      
    } catch (error) {
      console.error('AI insights error:', error);
    }
  }

  // Load resolution insights
  async function loadResolutionInsights() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsResolution, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch resolution insights');
      
      const data = await response.json();
      
      document.getElementById('avgResolution').textContent = data.average_resolution_hours.toFixed(1) + 'h';
      document.getElementById('fastestResolution').textContent = data.fastest_resolution_hours.toFixed(1) + 'h';
      document.getElementById('longestOpen').textContent = data.longest_open_hours.toFixed(1) + 'h';
      document.getElementById('slaRate').textContent = data.sla_met_rate.toFixed(1) + '%';
      
      // Animate SLA bar
      setTimeout(() => {
        const bar = document.getElementById('slaBar');
        bar.style.width = data.sla_met_rate + '%';
        
        if (data.sla_met_rate >= 90) {
          bar.style.background = '#10b981';
        } else if (data.sla_met_rate >= 70) {
          bar.style.background = '#f59e0b';
        } else {
          bar.style.background = '#ef4444';
        }
      }, 500);
      
    } catch (error) {
      console.error('Resolution insights error:', error);
    }
  }

  // Load monthly summary
  async function loadMonthlySummary() {
    try {
      const response = await fetch(API_ENDPOINTS.analyticsMonthlySummary, {
        headers: {
          'Authorization': `Bearer ${authUtils.getToken()}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch monthly summary');
      
      const data = await response.json();
      
      document.getElementById('monthlyCreated').textContent = data.current_month.created;
      document.getElementById('monthlyResolved').textContent = data.current_month.resolved;
      document.getElementById('monthlyCritical').textContent = data.current_month.critical;
      document.getElementById('monthlyConfidence').textContent = data.current_month.avg_confidence.toFixed(1) + '%';
      
      // Set change indicators
      setChangeIndicator('monthlyCreatedChange', data.changes.created);
      setChangeIndicator('monthlyResolvedChange', data.changes.resolved);
      setChangeIndicator('monthlyCriticalChange', data.changes.critical);
      setChangeIndicator('monthlyConfidenceChange', data.changes.confidence);
      
    } catch (error) {
      console.error('Monthly summary error:', error);
    }
  }

  // Set change indicator
  function setChangeIndicator(elementId, change) {
    const element = document.getElementById(elementId);
    const arrow = change > 0 ? '↑' : change < 0 ? '↓' : '→';
    const color = change > 0 ? '#10b981' : change < 0 ? '#ef4444' : '#6b7280';
    
    element.textContent = `${arrow} ${Math.abs(change).toFixed(1)}%`;
    element.style.color = color;
  }

  // Animate counter
  function animateCounter(element, target, duration = 1500) {
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

})();
