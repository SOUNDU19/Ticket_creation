import uuid
from datetime import datetime
from . import db
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user or admin
    
    # Extended profile fields
    avatar_url = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    timezone = db.Column(db.String(50), default='UTC')
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='user', lazy=True, cascade='all, delete-orphan', foreign_keys='Ticket.user_id')
    notification_settings = db.relationship('NotificationSettings', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'company': self.company,
            'role': self.role,
            'avatar_url': self.avatar_url,
            'phone': self.phone,
            'department': self.department,
            'timezone': self.timezone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def to_profile_dict(self):
        """Convert user to profile dictionary with notification settings"""
        profile = self.to_dict()
        if self.notification_settings:
            profile['notification_settings'] = self.notification_settings.to_dict()
        else:
            profile['notification_settings'] = None
        return profile


class NotificationSettings(db.Model):
    __tablename__ = 'notification_settings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    ticket_status_updates = db.Column(db.Boolean, default=True)
    critical_alerts = db.Column(db.Boolean, default=True)
    weekly_summary = db.Column(db.Boolean, default=False)
    ai_insight_updates = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert notification settings to dictionary"""
        return {
            'email_notifications': self.email_notifications,
            'ticket_status_updates': self.ticket_status_updates,
            'critical_alerts': self.critical_alerts,
            'weekly_summary': self.weekly_summary,
            'ai_insight_updates': self.ai_insight_updates
        }
