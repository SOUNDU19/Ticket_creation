"""
Initialize Enterprise Database Schema
Run this to update the database with new enterprise features
"""

from app import create_app
from models import db
from models.user import User, NotificationSettings
from models.ticket import Ticket, InternalNote
from models.admin import AuditLog, SystemSettings, AdminNotification

def init_enterprise_db():
    """Initialize database with enterprise schema"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Initializing Enterprise Database Schema...")
        
        # Create all tables
        db.create_all()
        print("✓ Database tables created/updated")
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@nexora.ai').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@nexora.ai',
                mobile='+1234567890',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()
            
            # Create notification settings for admin
            admin_settings = NotificationSettings(user_id=admin.id)
            db.session.add(admin_settings)
            
            db.session.commit()
            print("✓ Default admin created: admin@nexora.ai / admin123")
        else:
            print("✓ Admin user already exists")
        
        # Check/create system settings
        settings = SystemSettings.query.first()
        if not settings:
            settings = SystemSettings(
                ai_confidence_threshold=0.7,
                duplicate_detection_enabled=True,
                auto_categorization_enabled=True,
                sla_critical_hours=4,
                sla_high_hours=24,
                sla_medium_hours=48,
                sla_low_hours=72,
                default_ticket_status='open',
                allow_user_close_ticket=False,
                require_ticket_rating=True,
                admin_email_notifications=True,
                critical_ticket_alerts=True,
                sla_breach_alerts=True
            )
            db.session.add(settings)
            db.session.commit()
            print("✓ System settings initialized")
        else:
            # Update existing settings with new SLA fields if needed
            if not hasattr(settings, 'sla_critical_hours') or settings.sla_critical_hours is None:
                settings.sla_critical_hours = 4
                settings.sla_high_hours = 24
                settings.sla_medium_hours = 48
                settings.sla_low_hours = 72
                db.session.commit()
            print("✓ System settings already exist")
        
        # Count existing data
        user_count = User.query.filter_by(role='user').count()
        ticket_count = Ticket.query.count()
        note_count = InternalNote.query.count()
        audit_count = AuditLog.query.count()
        
        print("\n📊 Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Tickets: {ticket_count}")
        print(f"   Internal Notes: {note_count}")
        print(f"   Audit Logs: {audit_count}")
        
        print("\n✅ Enterprise Database Initialization Complete!")
        print("\n🔐 Admin Credentials:")
        print("   Email: admin@nexora.ai")
        print("   Password: admin123")
        print("\n🌐 Access Enterprise Admin Dashboard:")
        print("   http://localhost:8000/admin-dashboard-enhanced.html")
        print("\n" + "="*60)

if __name__ == '__main__':
    init_enterprise_db()
