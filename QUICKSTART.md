# NexoraAI Support Suite - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd nexora-ai
```

### Step 2: Run Setup Script

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create Python virtual environment
- Install all dependencies
- Download spaCy language model
- Train ML model on your datasets
- Create configuration files

### Step 3: Configure Environment

Edit `backend/.env`:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///nexora.db
```

### Step 4: Start Backend

```bash
cd backend
python app.py
```

Backend runs on: `http://localhost:5000`

### Step 5: Start Frontend

Open new terminal:

```bash
cd frontend
python -m http.server 8000
```

Frontend runs on: `http://localhost:8000`

### Step 6: Login

Open browser and go to: `http://localhost:8000`

**Default Admin Credentials:**
- Email: `admin@nexora.ai`
- Password: `admin123`

⚠️ **Change password immediately after first login!**

## 📊 Using the System

### Create Your First Ticket

1. Click "Create Ticket" in navigation
2. Enter ticket title and description
3. Click "Analyze with AI"
4. Review AI predictions (category, priority, confidence)
5. Click "Create Ticket"

### View Analytics

1. Navigate to "Analytics" page
2. View tickets by category, priority, and monthly trends
3. Export data as needed

### Admin Features

Admin users can:
- View all tickets from all users
- Update ticket status
- Access system-wide analytics
- Manage users

## 🔧 Troubleshooting

### ML Model Not Found

```bash
cd backend/ml
python train.py
```

### Port Already in Use

Change port in `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

And update `frontend/js/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

### Database Error

Delete existing database and restart:
```bash
rm backend/nexora.db
python backend/app.py
```

## 📁 Project Structure

```
nexora-ai/
├── frontend/           # Frontend application
│   ├── index.html     # Landing page
│   ├── login.html     # Login page
│   ├── dashboard.html # User dashboard
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── backend/           # Backend API
│   ├── app.py         # Main application
│   ├── models/        # Database models
│   ├── routes/        # API routes
│   ├── ml/            # Machine learning
│   └── utils/         # Utilities
└── datasets/          # Training datasets
```

## 🎯 Key Features

- ✅ AI-powered ticket categorization (>95% accuracy)
- ✅ Intelligent priority assignment
- ✅ Named entity extraction
- ✅ Real-time analytics
- ✅ Role-based access control
- ✅ Premium glassmorphism UI
- ✅ Fully responsive design
- ✅ PDF export functionality

## 📚 Next Steps

- Read full [README.md](README.md) for detailed information
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore [Documentation](http://localhost:8000/documentation.html)

## 💡 Tips

1. **Training Data**: Place your CSV datasets in `datasets/` folder before training
2. **Backup**: Regularly backup your database file
3. **Security**: Use strong passwords and enable HTTPS in production
4. **Performance**: Consider using PostgreSQL for production instead of SQLite

## 🆘 Support

For issues:
1. Check troubleshooting section above
2. Review error logs in terminal
3. Ensure all dependencies are installed
4. Verify Python version (3.8+)

## 🎨 Customization

### Change Theme Colors

Edit `frontend/css/style.css`:
```css
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  /* Add your colors */
}
```

### Add New Categories

Update ML training data in `datasets/` and retrain:
```bash
cd backend/ml
python train.py
```

---

**Designed & Developed by Soundarya**

Enjoy using NexoraAI Support Suite! 🚀
