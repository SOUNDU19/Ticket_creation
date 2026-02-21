// Floating Gradient Orbs System
class FloatingOrbs {
  constructor() {
    this.orbs = [];
    this.init();
  }

  init() {
    // Create orb elements
    this.createOrbs();
    // Start animation loop
    this.animate();
  }

  createOrbs() {
    const orbCount = 5;
    const colors = [
      'rgba(168, 85, 247, 0.3)', // Purple
      'rgba(249, 115, 22, 0.25)', // Orange
      'rgba(236, 72, 153, 0.2)',  // Pink
      'rgba(168, 85, 247, 0.25)', // Purple variant
      'rgba(249, 115, 22, 0.3)'   // Orange variant
    ];

    for (let i = 0; i < orbCount; i++) {
      const orb = document.createElement('div');
      orb.className = 'floating-orb';
      
      const size = Math.random() * 300 + 200; // 200-500px
      const x = Math.random() * window.innerWidth;
      const y = Math.random() * window.innerHeight;
      const duration = Math.random() * 20 + 20; // 20-40s
      const delay = Math.random() * 5;
      
      orb.style.cssText = `
        position: fixed;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: radial-gradient(circle, ${colors[i]} 0%, transparent 70%);
        filter: blur(${80 + Math.random() * 40}px);
        pointer-events: none;
        z-index: 0;
        left: ${x}px;
        top: ${y}px;
        animation: floatOrb ${duration}s ease-in-out infinite;
        animation-delay: ${delay}s;
        opacity: 0.6;
      `;
      
      document.body.appendChild(orb);
      this.orbs.push({
        element: orb,
        x: x,
        y: y,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: size
      });
    }

    // Add CSS animation
    if (!document.getElementById('orb-animations')) {
      const style = document.createElement('style');
      style.id = 'orb-animations';
      style.textContent = `
        @keyframes floatOrb {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          25% {
            transform: translate(50px, -50px) scale(1.1);
          }
          50% {
            transform: translate(-30px, 50px) scale(0.9);
          }
          75% {
            transform: translate(40px, 30px) scale(1.05);
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  animate() {
    // Optional: Add mouse interaction
    document.addEventListener('mousemove', (e) => {
      this.orbs.forEach((orb, index) => {
        const dx = e.clientX - orb.x;
        const dy = e.clientY - orb.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 300) {
          const angle = Math.atan2(dy, dx);
          const force = (300 - distance) / 300;
          orb.vx -= Math.cos(angle) * force * 0.1;
          orb.vy -= Math.sin(angle) * force * 0.1;
        }
      });
    });
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new FloatingOrbs();
  });
} else {
  new FloatingOrbs();
}

// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});

// Add ripple effect to buttons
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        left: ${x}px;
        top: ${y}px;
        pointer-events: none;
        animation: ripple 0.6s ease-out;
      `;
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
  
  // Add ripple animation
  if (!document.getElementById('ripple-animation')) {
    const style = document.createElement('style');
    style.id = 'ripple-animation';
    style.textContent = `
      @keyframes ripple {
        to {
          transform: scale(2);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }
});
