import uuid
from datetime import datetime
from . import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g., "ticket_updated", "user_deactivated"
    target_type = db.Column(db.String(50), nullable=False)  # ticket, user, system
    target_id = db.Column(db.String(36), nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON string with additional details
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    admin = db.relationship('User', backref='audit_logs', foreign_keys=[admin_id])
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'admin_name': self.admin.name if self.admin else 'Unknown',
            'admin_email': self.admin.email if self.admin else 'Unknown',
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat()
        }


class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # AI Settings
    ai_confidence_threshold = db.Column(db.Float, default=0.7)
    duplicate_detection_enabled = db.Column(db.Boolean, default=True)
    auto_categorization_enabled = db.Column(db.Boolean, default=True)
    
    # SLA Settings (in hours)
    sla_critical_hours = db.Column(db.Integer, default=2)
    sla_high_hours = db.Column(db.Integer, default=8)
    sla_medium_hours = db.Column(db.Integer, default=24)
    sla_low_hours = db.Column(db.Integer, default=72)
    
    # Ticket Settings
    default_ticket_status = db.Column(db.String(20), default='open')
    allow_user_close_ticket = db.Column(db.Boolean, default=False)
    require_ticket_rating = db.Column(db.Boolean, default=True)
    
    # Notification Settings
    admin_email_notifications = db.Column(db.Boolean, default=True)
    critical_ticket_alerts = db.Column(db.Boolean, default=True)
    sla_breach_alerts = db.Column(db.Boolean, default=True)
    
    # System Info
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    def to_dict(self):
        """Convert system settings to dictionary"""
        return {
            'id': self.id,
            'ai_confidence_threshold': self.ai_confidence_threshold,
            'duplicate_detection_enabled': self.duplicate_detection_enabled,
            'auto_categorization_enabled': self.auto_categorization_enabled,
            'sla_critical_hours': self.sla_critical_hours,
            'sla_high_hours': self.sla_high_hours,
            'sla_medium_hours': self.sla_medium_hours,
            'sla_low_hours': self.sla_low_hours,
            'default_ticket_status': self.default_ticket_status,
            'allow_user_close_ticket': self.allow_user_close_ticket,
            'require_ticket_rating': self.require_ticket_rating,
            'admin_email_notifications': self.admin_email_notifications,
            'critical_ticket_alerts': self.critical_ticket_alerts,
            'sla_breach_alerts': self.sla_breach_alerts,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AdminNotification(db.Model):
    __tablename__ = 'admin_notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # new_ticket, critical_ticket, sla_breach
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'link': self.link,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
