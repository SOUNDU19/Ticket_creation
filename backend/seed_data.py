"""
Seed database with sample data for testing
"""
from app import create_app, db
from models.user import User, NotificationSettings
from models.ticket import Ticket
from models.admin import SystemSettings
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with sample data"""
    app = create_app('production')
    
    with app.app_context():
        print("Starting database seeding...")
        
        # Create tables
        db.create_all()
        print("✓ Tables created")
        
        # Create admin if not exists
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
            
            admin_settings = NotificationSettings(user_id=admin.id)
            db.session.add(admin_settings)
            print("✓ Admin user created")
        else:
            print("✓ Admin user already exists")
        
        # Create system settings if not exists
        settings = SystemSettings.query.first()
        if not settings:
            settings = SystemSettings()
            db.session.add(settings)
            print("✓ System settings created")
        
        # Create sample users
        sample_users = [
            {'name': 'John Doe', 'email': 'john.doe@example.com', 'mobile': '+1234567891'},
            {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'mobile': '+1234567892'},
            {'name': 'Bob Johnson', 'email': 'bob.johnson@example.com', 'mobile': '+1234567893'},
            {'name': 'Alice Williams', 'email': 'alice.williams@example.com', 'mobile': '+1234567894'},
            {'name': 'Charlie Brown', 'email': 'charlie.brown@example.com', 'mobile': '+1234567895'},
        ]
        
        users = []
        for user_data in sample_users:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    mobile=user_data['mobile'],
                    role='user'
                )
                user.set_password('password123')
                db.session.add(user)
                db.session.flush()
                
                user_settings = NotificationSettings(user_id=user.id)
                db.session.add(user_settings)
                users.append(user)
            else:
                users.append(existing_user)
        
        print(f"✓ Created {len(users)} sample users")
        
        # Create sample tickets
        categories = ['Technical', 'Billing', 'General', 'Account']
        priorities = ['Low', 'Medium', 'High', 'Critical']
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        
        sample_tickets = [
            {
                'title': 'Cannot login to my account',
                'description': 'I am unable to login to my account. Getting error message "Invalid credentials" even though I am using the correct password.',
                'category': 'Technical',
                'priority': 'High'
            },
            {
                'title': 'Billing issue - double charged',
                'description': 'I was charged twice for my subscription this month. Please refund the duplicate charge.',
                'category': 'Billing',
                'priority': 'Critical'
            },
            {
                'title': 'How to reset password?',
                'description': 'I forgot my password and need help resetting it. The reset link is not working.',
                'category': 'General',
                'priority': 'Medium'
            },
            {
                'title': 'Account verification pending',
                'description': 'My account verification has been pending for 3 days. When will it be completed?',
                'category': 'Account',
                'priority': 'Medium'
            },
            {
                'title': 'Feature request - Dark mode',
                'description': 'Please add dark mode to the application. It would be great for night time usage.',
                'category': 'General',
                'priority': 'Low'
            },
            {
                'title': 'API integration not working',
                'description': 'The API integration is returning 500 errors. Need urgent help to fix this.',
                'category': 'Technical',
                'priority': 'Critical'
            },
            {
                'title': 'Update payment method',
                'description': 'I need to update my payment method but cannot find the option in settings.',
                'category': 'Billing',
                'priority': 'Medium'
            },
            {
                'title': 'Email notifications not received',
                'description': 'I am not receiving any email notifications from the system.',
                'category': 'Technical',
                'priority': 'High'
            },
            {
                'title': 'Delete my account',
                'description': 'I want to delete my account and all associated data.',
                'category': 'Account',
                'priority': 'Low'
            },
            {
                'title': 'Dashboard loading very slow',
                'description': 'The dashboard takes more than 30 seconds to load. This is affecting my productivity.',
                'category': 'Technical',
                'priority': 'High'
            },
        ]
        
        tickets_created = 0
        for i, ticket_data in enumerate(sample_tickets):
            user = users[i % len(users)]
            
            # Create ticket with varying creation dates
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            # Determine status based on age
            if days_ago > 20:
                status = random.choice(['Resolved', 'Closed'])
            elif days_ago > 10:
                status = random.choice(['In Progress', 'Resolved'])
            else:
                status = random.choice(['Open', 'In Progress'])
            
            ticket = Ticket(
                user_id=user.id,
                title=ticket_data['title'],
                description=ticket_data['description'],
                category=ticket_data['category'],
                priority=ticket_data['priority'],
                status=status,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(1, 48))
            )
            db.session.add(ticket)
            tickets_created += 1
        
        print(f"✓ Created {tickets_created} sample tickets")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database seeding completed successfully!")
        print(f"\nSample credentials:")
        print(f"Admin: admin@nexora.ai / admin123")
        print(f"User: john.doe@example.com / password123")
        
        return True

if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
