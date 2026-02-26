# NexoraAI Support Suite

**Smart Ticketing. Intelligent Automation.**

A production-ready AI-powered ticket automation system with premium SaaS UI and enterprise architecture.

## 🚀 Live Demo

- **Frontend**: https://ticket-creation-rho.vercel.app/landing.html
- **Backend API**: https://ticket-creation-6.onrender.com/api
- **Admin Login**: admin@nexora.ai / admin123

## Features

- 🤖 AI-powered ticket categorization (>95% accuracy)
- 🎯 Intelligent priority assignment
- 🔍 Named entity extraction using spaCy
- 🔐 JWT authentication & role-based access
- 💾 Dual database support (Avian DB + SQLite fallback)
- 📊 Advanced analytics dashboard
- 🎨 Premium glassmorphism UI
- 📱 Fully responsive design
- 🌙 Dark mode support

## Tech Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript (ES6)
- Chart.js for analytics
- jsPDF for PDF export
- Glassmorphism design

### Backend
- Flask REST API
- Flask-JWT-Extended
- SQLAlchemy
- scikit-learn
- spaCy NLP
- Avian DB / SQLite

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Node.js (optional, for serving frontend)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Configure environment variables:
Create `.env` file in backend directory:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
AVIAN_CONNECTION_STRING=your-avian-connection-string
DATABASE_URL=sqlite:///nexora.db
```

5. Train ML model:
```bash
cd ml
python train.py
cd ..
```

6. Run the application:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Open `frontend/js/config.js` and ensure API_BASE_URL points to your backend

2. Serve frontend using any static server:
```bash
# Using Python
cd frontend
python -m http.server 8000

# Or using Node.js
npx serve frontend
```

Frontend will be available at `http://run itlocalhost:8000`

## 📁 Project Structure

```
NexoraAI/
├── 📂 frontend/                    # Frontend application
│   ├── 🏠 landing.html            # Landing page
│   ├── 🔐 login.html              # Login page
│   ├── 📝 signup.html             # Registration page
│   ├── 📊 dashboard.html          # User dashboard
│   ├── ➕ create-ticket.html      # Ticket creation (AI-powered)
│   ├── 📜 history.html            # Ticket history
│   ├── 👤 profile.html            # User profile
│   ├── 🔧 admin-dashboard-enhanced.html  # Admin panel
│   ├── 📈 analytics.html          # Analytics dashboard
│   ├── 🎨 css/                    # Stylesheets
│   │   ├── style.css              # Main styles
│   │   ├── landing-styles.css     # Landing page styles
│   │   ├── landing-animations.css # Animations
│   │   └── responsive.css         # Mobile responsive
│   └── 💻 js/                     # JavaScript files
│       ├── config.js              # API configuration
│       ├── auth.js                # Authentication logic
│       ├── api.js                 # API calls & utilities
│       ├── create-ticket.js       # Ticket creation logic
│       ├── admin-enhanced.js      # Admin functionality
│       └── profile.js             # Profile management
│
├── 📂 backend/                     # Backend API
│   ├── app.py                     # Main Flask application
│   ├── config.py                  # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── 📂 models/                 # Database models
│   │   ├── user.py                # User model
│   │   └── ticket.py              # Ticket model
│   ├── 📂 routes/                 # API endpoints
│   │   ├── auth.py                # Authentication routes
│   │   ├── tickets.py             # Ticket CRUD operations
│   │   ├── profile.py             # User profile routes
│   │   └── admin_enhanced.py      # Admin routes
│   ├── 📂 ml/                     # Machine Learning
│   │   ├── train.py               # Model training script
│   │   ├── predict.py             # Prediction logic
│   │   ├── model.pkl              # Trained model
│   │   └── vectorizer.pkl         # TF-IDF vectorizer
│   └── 📂 utils/                  # Helper functions
│       └── helpers.py             # Utility functions
│
├── 📂 agile_project/               # Agile Project Management
│   ├── 📋 Product_Backlog.csv     # Product backlog
│   ├── 📅 Sprint_Backlog.csv      # Sprint tasks
│   ├── 🔄 Sprint_Planning_Retrospective.csv  # Sprint planning
│   ├── 📝 Daily_Standup_Tracking.csv  # Daily standups
│   ├── 📄 AGILE_PROJECT_TEMPLATE.md  # Agile documentation
│   ├── 📄 EXCEL_AGILE_TEMPLATE.md    # Excel guide
│   └── 📊 Agile_Template_v0.1.xls    # Excel template
│
├── 📂 dataset/                     # Training data
│   └── customer_support_tickets.csv
│
├── 📄 README.md                    # Project documentation
├── 📄 TECHNICAL_INTERVIEW_QUESTIONS.md  # Interview prep
├── ⚙️ vercel.json                 # Vercel deployment config
└── ⚙️ render.yaml                 # Render deployment config
```

## ML Model Training

The system uses multiple ML algorithms:
- Logistic Regression
- Linear SVM
- Random Forest

Training process:
1. Text cleaning and preprocessing
2. Stopword removal
3. Lemmatization using spaCy
4. TF-IDF vectorization
5. GridSearchCV for hyperparameter tuning
6. Model evaluation (Accuracy, Precision, Recall, F1)

Expected accuracy: >95%

## API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login

### Tickets
- `POST /api/predict` - AI prediction
- `POST /api/create-ticket` - Create ticket
- `GET /api/tickets` - Get user tickets
- `GET /api/ticket/<id>` - Get ticket details
- `PUT /api/update-ticket` - Update ticket

### User
- `PUT /api/update-profile` - Update profile
- `DELETE /api/delete-account` - Delete account

### Analytics
- `GET /api/analytics` - Get analytics data

### Admin
- `GET /api/admin/tickets` - Get all tickets

## Security Features

- bcrypt password hashing
- JWT token authentication
- Role-based access control
- Input validation
- CORS protection
- Environment-based secrets

## Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure production database (Avian DB)
- [ ] Enable HTTPS
- [ ] Set up CORS for production domain
- [ ] Configure rate limiting
- [ ] Set up logging and monitoring
- [ ] Enable database backups

### Deployment Options
- **Backend**: Heroku, AWS, Google Cloud, DigitalOcean
- **Frontend**: Netlify, Vercel, GitHub Pages
- **Database**: Avian Cloud, PostgreSQL, MySQL

## 📚 Documentation

- **[Technical Interview Questions](TECHNICAL_INTERVIEW_QUESTIONS.md)** - 70+ interview Q&A covering ML, Backend, Database, Frontend, and more
- **[Agile Project Documentation](agile_project/)** - Complete Agile/Scrum documentation with sprints, backlogs, and retrospectives

## Credits

**Designed & Developed by Soundarya**

## License

Proprietary - All rights reserved

## Support

For issues and questions, please contact support.
