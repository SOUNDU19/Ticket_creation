#!/bin/bash
cd backend

# Ensure database directory exists
mkdir -p /opt/render/project/src

# Initialize database with only admin user (no sample data)
python -c "
from app import create_app, db
from models.user import User, NotificationSettings
from models.admin import SystemSettings

app = create_app('production')
with app.app_context():
    db.create_all()
    print('✓ Database tables created')
    
    # Create admin if not exists
    admin = User.query.filter_by(email='admin@nexora.ai').first()
    if not admin:
        admin = User(name='Admin', email='admin@nexora.ai', mobile='+1234567890', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        
        admin_settings = NotificationSettings(user_id=admin.id)
        db.session.add(admin_settings)
        print('✓ Admin user created: admin@nexora.ai / admin123')
    
    # Create system settings if not exists
    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        print('✓ System settings created')
    
    db.session.commit()
    print('✅ Database initialized - Ready for real users!')
" || echo "Database initialization skipped"

# Start gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --access-logfile - --error-logfile -
