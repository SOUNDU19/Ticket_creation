// Google OAuth Demo Implementation
// In production, replace with actual Google Client ID and proper backend integration

class GoogleAuthDemo {
  constructor() {
    this.isDemo = true;
    this.demoUsers = [
      {
        sub: 'demo_user_1',
        email: 'demo@gmail.com',
        name: 'Demo User',
        given_name: 'Demo',
        family_name: 'User',
        picture: 'https://via.placeholder.com/96x96'
      }
    ];
  }

  // Simulate Google Sign-In popup
  simulateGoogleSignIn(callback, context = 'signin') {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
    `;

    // Create popup content
    const popup = document.createElement('div');
    popup.style.cssText = `
      background: white;
      border-radius: 12px;
      padding: 2rem;
      max-width: 400px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    `;

    popup.innerHTML = `
      <div style="margin-bottom: 1.5rem;">
        <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" style="width: 24px; height: 24px; margin-bottom: 1rem;">
        <h3 style="margin: 0; color: #333;">Sign ${context === 'signup' ? 'up' : 'in'} with Google</h3>
        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">Demo Mode - Choose an account</p>
      </div>
      
      <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; cursor: pointer; transition: background 0.2s;" onclick="selectDemoUser()">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 40px; height: 40px; border-radius: 50%; background: #4285f4; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">D</div>
          <div style="text-align: left;">
            <div style="font-weight: 500; color: #333;">Demo User</div>
            <div style="font-size: 0.9rem; color: #666;">demo@gmail.com</div>
          </div>
        </div>
      </div>
      
      <div style="display: flex; gap: 1rem;">
        <button onclick="closeGooglePopup()" style="flex: 1; padding: 0.75rem; border: 1px solid #ddd; background: white; border-radius: 6px; cursor: pointer;">Cancel</button>
        <button onclick="selectDemoUser()" style="flex: 1; padding: 0.75rem; border: none; background: #4285f4; color: white; border-radius: 6px; cursor: pointer;">Continue</button>
      </div>
    `;

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Global functions for popup
    window.selectDemoUser = () => {
      const demoUser = this.demoUsers[0];
      const credential = this.createDemoJWT(demoUser);
      
      document.body.removeChild(overlay);
      
      // Call the callback with demo response
      callback({
        credential: credential
      });
    };

    window.closeGooglePopup = () => {
      document.body.removeChild(overlay);
    };

    // Close on overlay click
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        document.body.removeChild(overlay);
      }
    });
  }

  // Create demo JWT token
  createDemoJWT(user) {
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
      ...user,
      iss: 'https://accounts.google.com',
      aud: 'demo-client-id',
      exp: Math.floor(Date.now() / 1000) + 3600,
      iat: Math.floor(Date.now() / 1000)
    }));
    const signature = btoa('demo-signature');
    
    return `${header}.${payload}.${signature}`;
  }

  // Initialize demo Google buttons
  initializeDemoButtons() {
    // Replace Google Sign-In buttons with demo versions
    const signInButtons = document.querySelectorAll('.g_id_signin');
    signInButtons.forEach(button => {
      const context = button.closest('#g_id_onload') ? 
        button.closest('#g_id_onload').getAttribute('data-context') : 'signin';
      const callbackName = button.closest('#g_id_onload') ? 
        button.closest('#g_id_onload').getAttribute('data-callback') : 'handleGoogleSignIn';
      
      button.innerHTML = `
        <div style="
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.75rem;
          padding: 0.75rem 1rem;
          border: 1px solid #dadce0;
          border-radius: 8px;
          background: white;
          color: #3c4043;
          font-family: 'Google Sans', Roboto, sans-serif;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          width: 100%;
          box-sizing: border-box;
        " onmouseover="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'" onmouseout="this.style.boxShadow='none'">
          <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" style="width: 18px; height: 18px;">
          <span>Sign ${context === 'signup' ? 'up' : 'in'} with Google</span>
        </div>
      `;
      
      button.addEventListener('click', () => {
        const callback = window[callbackName];
        if (callback) {
          this.simulateGoogleSignIn(callback, context);
        }
      });
    });
  }
}

// Initialize demo when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Wait a bit for Google scripts to potentially load
  setTimeout(() => {
    const googleAuth = new GoogleAuthDemo();
    googleAuth.initializeDemoButtons();
  }, 1000);
});

// Export for use in other scripts
window.GoogleAuthDemo = GoogleAuthDemo;