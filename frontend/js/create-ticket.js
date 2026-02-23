// Create Ticket Page Logic
(function() {
  'use strict';

  // Protect page
  if (!authUtils.protectPage()) {
    throw new Error('Unauthorized');
  }

  let aiPrediction = null;
  let currentStep = 1;

  // Update step indicator
  function updateStep(step) {
    currentStep = step;
    document.querySelectorAll('.step').forEach(s => {
      const stepNum = parseInt(s.dataset.step);
      s.classList.toggle('active', stepNum === step);
      s.classList.toggle('completed', stepNum < step);
    });
  }

  // Character counter with validation
  const descriptionInput = document.getElementById('description');
  descriptionInput.addEventListener('input', (e) => {
    const length = e.target.value.length;
    document.getElementById('charCount').textContent = length;
    
    const minIndicator = document.getElementById('minLengthIndicator');
    if (length >= 20) {
      minIndicator.style.display = 'none';
    } else {
      minIndicator.style.display = 'inline';
    }
    
    // Limit to 1000 characters
    if (length > 1000) {
      e.target.value = e.target.value.substring(0, 1000);
      document.getElementById('charCount').textContent = '1000';
    }
  });

  // Advanced options toggle
  document.getElementById('advancedToggle').addEventListener('click', function() {
    const content = document.getElementById('advancedContent');
    const isOpen = content.style.maxHeight && content.style.maxHeight !== '0px';
    
    if (isOpen) {
      content.style.maxHeight = '0';
      this.classList.remove('open');
    } else {
      content.style.maxHeight = content.scrollHeight + 'px';
      this.classList.add('open');
    }
  });

  // Analyze with AI
  document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const description = document.getElementById('description').value.trim();
    
    if (!description) {
      showToast('Please enter a description first', 'warning');
      return;
    }

    if (description.length < 20) {
      showToast('Description must be at least 20 characters', 'warning');
      return;
    }

    updateStep(2);

    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;

    // Show loading sequence
    document.getElementById('aiPlaceholder').style.display = 'none';
    document.getElementById('aiPreview').style.display = 'none';
    document.getElementById('aiLoading').style.display = 'block';

    // Animate loading steps
    await animateLoadingSteps();

    try {
      aiPrediction = await api.predict(description);

      // Hide loading, show results
      document.getElementById('aiLoading').style.display = 'none';
      document.getElementById('aiPreview').style.display = 'block';
      document.getElementById('aiPreview').style.animation = 'fadeInUp 0.5s ease';

      // Update category
      const categoryBadge = document.getElementById('categoryPreview');
      categoryBadge.textContent = aiPrediction.category;
      categoryBadge.className = 'category-badge';

      // Update priority
      const priorityBadge = document.getElementById('priorityPreview');
      priorityBadge.textContent = aiPrediction.priority.toUpperCase();
      priorityBadge.className = `priority-badge priority-${aiPrediction.priority}`;

      // Update confidence
      const confidencePercent = Math.round(aiPrediction.confidence * 100);
      const confidenceBar = document.getElementById('confidenceBar');
      const confidenceText = document.getElementById('confidenceText');
      
      setTimeout(() => {
        confidenceBar.style.width = confidencePercent + '%';
        confidenceText.textContent = confidencePercent + '%';
        
        // Color based on confidence
        if (confidencePercent >= 85) {
          confidenceBar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
        } else if (confidencePercent >= 60) {
          confidenceBar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
        } else {
          confidenceBar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
      }, 100);

      // Display entities as chips
      const entities = aiPrediction.entities;
      const entitiesContainer = document.getElementById('entitiesPreview');
      entitiesContainer.innerHTML = '';
      
      let hasEntities = false;
      
      // Check all possible entity types
      const entityTypes = ['emails', 'phone_numbers', 'error_codes', 'urls', 'amounts', 'dates'];
      
      entityTypes.forEach(type => {
        if (entities[type] && entities[type].length > 0) {
          hasEntities = true;
          entities[type].forEach(item => {
            const icon = getEntityIcon(type);
            entitiesContainer.innerHTML += `<span class="entity-chip entity-${type}">${icon} ${item}</span>`;
          });
        }
      });
      
      if (!hasEntities) {
        entitiesContainer.innerHTML = '<span class="entity-placeholder">No entities extracted</span>';
      }

      // Check for duplicates (simulated)
      if (Math.random() > 0.8) {
        document.getElementById('duplicateWarning').style.display = 'block';
      }

      // Enable submit button
      document.getElementById('submitBtn').disabled = false;

      showToast('AI analysis complete!', 'success');
    } catch (error) {
      document.getElementById('aiLoading').style.display = 'none';
      document.getElementById('aiPlaceholder').style.display = 'block';
      showToast('AI analysis failed: ' + error.message, 'error');
      updateStep(1);
    } finally {
      analyzeBtn.disabled = false;
    }
  });

  // Get entity icon
  function getEntityIcon(type) {
    const icons = {
      'emails': '📧',
      'phone_numbers': '📞',
      'error_codes': '⚠️',
      'urls': '🔗',
      'amounts': '💰',
      'dates': '📅'
    };
    return icons[type] || '🏷️';
  }

  // Animate loading steps
  async function animateLoadingSteps() {
    const steps = document.querySelectorAll('.loading-step');
    
    for (let i = 0; i < steps.length; i++) {
      steps[i].classList.add('active');
      await new Promise(resolve => setTimeout(resolve, 800));
      steps[i].classList.remove('active');
      steps[i].classList.add('completed');
    }
    
    // Reset for next use
    setTimeout(() => {
      steps.forEach(s => {
        s.classList.remove('active', 'completed');
      });
    }, 500);
  }

  // Category override
  document.getElementById('categoryOverride').addEventListener('change', (e) => {
    if (e.target.value && aiPrediction) {
      aiPrediction.category = e.target.value;
      document.getElementById('categoryPreview').textContent = e.target.value;
      showToast('Category updated', 'success');
    }
  });

  // Submit form - show review modal
  document.getElementById('ticketForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!aiPrediction) {
      showToast('Please analyze with AI first', 'warning');
      return;
    }

    updateStep(3);

    // Populate review modal
    document.getElementById('reviewTitle').textContent = document.getElementById('title').value.trim();
    document.getElementById('reviewCategory').innerHTML = `<span class="category-badge">${aiPrediction.category}</span>`;
    document.getElementById('reviewPriority').innerHTML = `<span class="priority-badge priority-${aiPrediction.priority}">${aiPrediction.priority.toUpperCase()}</span>`;
    document.getElementById('reviewDescription').textContent = document.getElementById('description').value.trim();
    
    // Copy entities
    const entitiesHTML = document.getElementById('entitiesPreview').innerHTML;
    document.getElementById('reviewEntities').innerHTML = entitiesHTML;

    // Show modal
    document.getElementById('reviewModal').classList.add('active');
  });

  // Close review modal
  window.closeReviewModal = function() {
    document.getElementById('reviewModal').classList.remove('active');
    updateStep(2);
  };

  // Confirm and create ticket - using event listener
  const confirmBtn = document.getElementById('confirmCreateBtn');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', async function() {
      const title = document.getElementById('title').value.trim();
      const description = document.getElementById('description').value.trim();
      const manualPriority = document.getElementById('manualPriority').value;

      this.disabled = true;
      const originalHTML = this.innerHTML;
      this.innerHTML = '<span class="btn-spinner"></span><span>Creating...</span>';

      try {
        const ticketData = {
          title,
          description,
          category: aiPrediction.category,
          priority: manualPriority || aiPrediction.priority,
          confidence: aiPrediction.confidence,
          tags: document.getElementById('customTags').value
        };

        console.log('Creating ticket with data:', ticketData);

        const response = await api.createTicket(ticketData);

        console.log('Ticket created successfully:', response);

        showToast('Ticket created successfully!', 'success');

        // Close modal
        document.getElementById('reviewModal').classList.remove('active');

        setTimeout(() => {
          window.location.href = 'history.html';
        }, 1000);
      } catch (error) {
        console.error('Failed to create ticket:', error);
        showToast('Failed to create ticket: ' + error.message, 'error');
        this.disabled = false;
        this.innerHTML = originalHTML;
      }
    });
  }
})();
