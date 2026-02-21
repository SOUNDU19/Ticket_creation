import uuid
from datetime import datetime
from . import db

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed, escalated
    ai_confidence = db.Column(db.Float, default=0.0)
    
    # AI Override Tracking
    original_ai_category = db.Column(db.String(50), nullable=True)
    overridden_by_admin = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Ticket Merging
    merged_into_ticket_id = db.Column(db.String(36), db.ForeignKey('tickets.id'), nullable=True)
    is_merged = db.Column(db.Boolean, default=False)
    
    # Assignment
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    internal_notes = db.relationship('InternalNote', backref='ticket', lazy=True, cascade='all, delete-orphan')
    merged_tickets = db.relationship('Ticket', backref=db.backref('parent_ticket', remote_side=[id]), lazy=True)
    
    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else 'Unknown',
            'user_email': self.user.email if self.user else 'Unknown',
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'ai_confidence': self.ai_confidence,
            'original_ai_category': self.original_ai_category,
            'overridden_by_admin': self.overridden_by_admin,
            'merged_into_ticket_id': self.merged_into_ticket_id,
            'is_merged': self.is_merged,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


class InternalNote(db.Model):
    __tablename__ = 'internal_notes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = db.Column(db.String(36), db.ForeignKey('tickets.id'), nullable=False)
    admin_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    admin = db.relationship('User', foreign_keys=[admin_id])
    
    def to_dict(self):
        """Convert internal note to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'admin_id': self.admin_id,
            'admin_name': self.admin.name if self.admin else 'Unknown',
            'admin_email': self.admin.email if self.admin else 'Unknown',
            'note': self.note,
            'created_at': self.created_at.isoformat()
        }
