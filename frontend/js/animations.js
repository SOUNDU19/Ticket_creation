// Advanced Animation System for Landing Page
class AnimationController {
  constructor() {
    this.observers = [];
    this.init();
  }

  init() {
    // Initialize scroll animations
    this.initScrollAnimations();
    
    // Initialize feature cards stagger animation
    this.initFeatureCardsAnimation();
    
    // Initialize number counters
    this.initCounters();
    
    // Initialize parallax effects
    this.initParallax();
    
    // Initialize typing effect
    this.initTypingEffect();
    
    // Initialize hover effects
    this.initHoverEffects();
  }

  // Special animation for feature cards grid
  initFeatureCardsAnimation() {
    const featuresSection = document.querySelector('#features');
    if (!featuresSection) return;

    const cards = featuresSection.querySelectorAll('.card.scale-in');
    
    const observerOptions = {
      threshold: 0.15,
      rootMargin: '0px 0px -80px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Animate all cards with stagger when section comes into view
          cards.forEach((card, index) => {
            setTimeout(() => {
              card.classList.add('animated');
            }, index * 200); // 200ms delay between each card
          });
          
          // Disconnect after animating once
          observer.disconnect();
        }
      });
    }, observerOptions);

    // Observe the features section
    if (featuresSection) {
      observer.observe(featuresSection);
    }
  }

  // Scroll-triggered animations using Intersection Observer
  initScrollAnimations() {
    const observerOptions = {
      threshold: 0.2, // Increased threshold - element must be 20% visible
      rootMargin: '0px 0px -50px 0px' // Reduced margin for earlier trigger
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Add a small delay before triggering animation
          setTimeout(() => {
            entry.target.classList.add('animated');
          }, 100);
          
          // For staggered animations
          if (entry.target.classList.contains('stagger-parent')) {
            this.animateChildren(entry.target);
          }
        }
      });
    }, observerOptions);

    // Observe all elements with animation classes
    const animatedElements = document.querySelectorAll(
      '.animate-on-scroll, .fade-in, .slide-in-left, .slide-in-right, ' +
      '.scale-in, .rotate-in, .slide-up, .zoom-in, .flip-in, .reveal-animation'
    );

    animatedElements.forEach(el => observer.observe(el));
    this.observers.push(observer);
  }

  // Animate children with stagger effect
  animateChildren(parent) {
    const children = parent.querySelectorAll('.stagger-item');
    children.forEach((child, index) => {
      setTimeout(() => {
        child.classList.add('animated');
      }, index * 200); // Increased from 100ms to 200ms for slower stagger
    });
  }

  // Number counter animation
  initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    const observerOptions = {
      threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
          this.animateCounter(entry.target);
          entry.target.classList.add('counted');
        }
      });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
    this.observers.push(observer);
  }

  animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target') || element.textContent);
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
      current += increment;
      if (current < target) {
        element.textContent = Math.floor(current);
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = target;
      }
    };

    updateCounter();
  }

  // Parallax scroll effect
  initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;

      parallaxElements.forEach(element => {
        const speed = element.getAttribute('data-speed') || 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
      });
    });
  }

  // Typing effect for hero text
  initTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-effect');
    
    typingElements.forEach(element => {
      const text = element.textContent;
      element.textContent = '';
      element.style.opacity = '1';
      
      let index = 0;
      const typeSpeed = 50;

      const type = () => {
        if (index < text.length) {
          element.textContent += text.charAt(index);
          index++;
          setTimeout(type, typeSpeed);
        }
      };

      // Start typing after a delay
      setTimeout(type, 500);
    });
  }

  // Enhanced hover effects
  initHoverEffects() {
    // Magnetic button effect
    const magneticButtons = document.querySelectorAll('.btn-magnetic');
    
    magneticButtons.forEach(button => {
      button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
      });

      button.addEventListener('mouseleave', () => {
        button.style.transform = 'translate(0, 0)';
      });
    });

    // Tilt effect on cards
    const tiltCards = document.querySelectorAll('.tilt-card');
    
    tiltCards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
      });
    });
  }

  // Cleanup observers
  destroy() {
    this.observers.forEach(observer => observer.disconnect());
  }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      
      if (target) {
        const offsetTop = target.offsetTop - 80;
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Navbar scroll effect
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(10, 10, 10, 0.95)';
      navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.7)';
    } else {
      navbar.style.background = 'rgba(10, 10, 10, 0.8)';
      navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.5)';
    }
  });
}

// Cursor trail effect
function initCursorTrail() {
  const trail = [];
  const trailLength = 20;

  document.addEventListener('mousemove', (e) => {
    trail.push({ x: e.clientX, y: e.clientY, time: Date.now() });
    
    if (trail.length > trailLength) {
      trail.shift();
    }
  });

  // Optional: Create visual trail elements
  // This can be enabled for more dramatic effect
}

// Page load animation
function initPageLoadAnimation() {
  document.body.style.opacity = '0';
  
  window.addEventListener('load', () => {
    setTimeout(() => {
      document.body.style.transition = 'opacity 0.5s ease';
      document.body.style.opacity = '1';
    }, 100);
  });
}

// Scroll progress indicator
function initScrollProgress() {
  const progressBar = document.createElement('div');
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #a855f7, #f97316);
    z-index: 9999;
    transition: width 0.1s ease;
    width: 0;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.scrollY / windowHeight) * 100;
    progressBar.style.width = scrolled + '%';
  });
}

// Initialize all animations when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const animationController = new AnimationController();
    initSmoothScroll();
    initNavbarScroll();
    initScrollProgress();
    initPageLoadAnimation();
  });
} else {
  const animationController = new AnimationController();
  initSmoothScroll();
  initNavbarScroll();
  initScrollProgress();
  initPageLoadAnimation();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AnimationController };
}
