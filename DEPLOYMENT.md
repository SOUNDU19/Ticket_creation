# NexoraAI Deployment Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- Node.js (optional, for serving frontend)

## Local Development Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
```
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///nexora.db
```

6. Train ML model:
```bash
cd ml
python train.py
cd ..
```

7. Run the backend server:
```bash
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Update API configuration in `js/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

3. Serve frontend using Python:
```bash
python -m http.server 8000
```

Or using Node.js:
```bash
npx serve .
```

Frontend will be available at `http://localhost:8000`

## Production Deployment

### Backend Deployment (Heroku)

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create new Heroku app:
```bash
heroku create nexora-api
```

3. Add buildpack:
```bash
heroku buildpacks:set heroku/python
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set JWT_SECRET_KEY=your-production-jwt-key
heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL=your-production-database-url
```

5. Create Procfile in backend directory:
```
web: gunicorn app:app
```

6. Add gunicorn to requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

7. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Backend Deployment (AWS/DigitalOcean)

1. Set up Ubuntu server

2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

3. Clone repository:
```bash
git clone your-repo-url
cd nexora-ai/backend
```

4. Set up virtual environment and install:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

5. Configure environment variables:
```bash
nano .env
```

6. Train ML model:
```bash
cd ml
python train.py
cd ..
```

7. Set up Gunicorn service:
```bash
sudo nano /etc/systemd/system/nexora.service
```

Add:
```
[Unit]
Description=NexoraAI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/nexora-ai/backend
Environment="PATH=/home/ubuntu/nexora-ai/backend/venv/bin"
ExecStart=/home/ubuntu/nexora-ai/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

8. Start service:
```bash
sudo systemctl start nexora
sudo systemctl enable nexora
```

9. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/nexora
```

Add:
```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

10. Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/nexora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Frontend Deployment (Netlify)

1. Create `netlify.toml` in frontend directory:
```toml
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. Update `js/config.js` with production API URL:
```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

3. Deploy via Netlify CLI:
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

Or connect GitHub repository in Netlify dashboard.

### Frontend Deployment (Vercel)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd frontend
vercel --prod
```

### Database Setup

#### SQLite (Development)
- Automatically created on first run
- File: `backend/nexora.db`

#### PostgreSQL (Production)

1. Create database:
```sql
CREATE DATABASE nexora;
CREATE USER nexora_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE nexora TO nexora_user;
```

2. Update DATABASE_URL:
```
DATABASE_URL=postgresql://nexora_user:your-password@localhost:5432/nexora
```

#### Avian Database

1. Get connection string from Avian dashboard

2. Update .env:
```
AVIAN_CONNECTION_STRING=your-avian-connection-string
```

## Post-Deployment

### Create Admin User

Admin user is automatically created on first run:
- Email: admin@nexora.ai
- Password: admin123

**IMPORTANT:** Change admin password immediately after first login!

### SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Monitoring

Set up monitoring using:
- Sentry for error tracking
- New Relic for performance monitoring
- CloudWatch for AWS deployments

### Backup

Set up automated backups:
```bash
# Database backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump nexora > /backups/nexora_$DATE.sql
```

Add to crontab:
```bash
0 2 * * * /path/to/backup-script.sh
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Flask secret key | Yes |
| JWT_SECRET_KEY | JWT token secret | Yes |
| DATABASE_URL | Database connection string | Yes |
| AVIAN_CONNECTION_STRING | Avian DB connection | No |
| FLASK_ENV | Environment (development/production) | Yes |
| CORS_ORIGINS | Allowed CORS origins | No |

## Troubleshooting

### ML Model Not Found
```bash
cd backend/ml
python train.py
```

### Database Connection Error
- Check DATABASE_URL format
- Verify database credentials
- Ensure database server is running

### CORS Error
- Update CORS_ORIGINS in .env
- Restart backend server

### Port Already in Use
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain only
- [ ] Set up rate limiting
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Review and update dependencies regularly
- [ ] Implement IP whitelisting for admin panel
- [ ] Enable two-factor authentication

## Performance Optimization

1. Enable caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

2. Use CDN for static assets

3. Enable gzip compression in Nginx

4. Optimize database queries with indexes

5. Use connection pooling for database

## Support

For issues and questions:
- GitHub Issues: [repository-url]
- Email: support@nexora.ai
- Documentation: https://docs.nexora.ai

---

**Designed & Developed by Soundarya**
