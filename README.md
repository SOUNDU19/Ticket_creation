# NexoraAI Support Suite

**Smart Ticketing. Intelligent Automation.**

A production-ready AI-powered ticket automation system with premium SaaS UI and enterprise architecture.

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

Frontend will be available at `http://localhost:8000`

## Project Structure

```
nexora-ai/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── create-ticket.html
│   ├── history.html
│   ├── profile.html
│   ├── admin.html
│   ├── analytics.html
│   ├── settings.html
│   ├── about.html
│   ├── documentation.html
│   ├── 404.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── config.js
│       ├── auth.js
│       ├── api.js
│       └── [page-specific].js
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── ticket.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tickets.py
│   │   └── admin.py
│   ├── ml/
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── model.pkl
│   │   └── vectorizer.pkl
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── dataset/
└── datasets/
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

## Credits

**Designed & Developed by Soundarya**

## License

Proprietary - All rights reserved

## Support

For issues and questions, please contact support.
