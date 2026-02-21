"""
NexoraAI Database Viewer
View users, tickets, and statistics
"""

import sqlite3
import sys

DB_PATH = 'instance/nexora.db'

def view_users():
    """View all users"""
    print("\n" + "="*100)
    print("👥 USERS")
    print("="*100)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, email, mobile, company, role, department, 
               is_active, created_at, last_login
        FROM users
        ORDER BY created_at DESC
    """)
    
    users = cursor.fetchall()
    
    print(f"\nTotal Users: {len(users)}\n")
    
    for i, user in enumerate(users, 1):
        user_id, name, email, mobile, company, role, dept, active, created, last_login = user
        print(f"{i}. {name}")
        print(f"   Email: {email}")
        print(f"   Mobile: {mobile}")
        print(f"   Role: {role.upper()}")
        print(f"   Company: {company or 'N/A'}")
        print(f"   Department: {dept or 'N/A'}")
        print(f"   Status: {'✅ Active' if active else '❌ Inactive'}")
        print(f"   Created: {created}")
        print(f"   Last Login: {last_login or 'Never'}")
        print("-" * 100)
    
    conn.close()

def view_tickets():
    """View all tickets"""
    print("\n" + "="*100)
    print("🎫 TICKETS")
    print("="*100)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.id, t.title, t.description, t.category, t.priority, t.status,
               t.ai_confidence, u.name as user_name, t.created_at
        FROM tickets t
        LEFT JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
    """)
    
    tickets = cursor.fetchall()
    
    print(f"\nTotal Tickets: {len(tickets)}\n")
    
    for i, ticket in enumerate(tickets, 1):
        tid, title, desc, category, priority, status, confidence, user_name, created = ticket
        print(f"{i}. {title}")
        print(f"   Description: {desc[:100]}{'...' if len(desc) > 100 else ''}")
        print(f"   Category: {category}")
        print(f"   Priority: {priority.upper()}")
        print(f"   Status: {status.upper()}")
        print(f"   AI Confidence: {confidence*100:.1f}%")
        print(f"   Created By: {user_name}")
        print(f"   Created: {created}")
        print("-" * 100)
    
    conn.close()

def view_stats():
    """View database statistics"""
    print("\n" + "="*100)
    print("📊 DATABASE STATISTICS")
    print("="*100)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User stats
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    admin_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    regular_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_active=1")
    active_users = cursor.fetchone()[0]
    
    # Ticket stats
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='open'")
    open_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='in_progress'")
    in_progress = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='closed'")
    closed_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='critical'")
    critical_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='high'")
    high_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='medium'")
    medium_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='low'")
    low_tickets = cursor.fetchone()[0]
    
    # Category distribution
    cursor.execute("SELECT category, COUNT(*) as count FROM tickets GROUP BY category ORDER BY count DESC")
    categories = cursor.fetchall()
    
    # Average confidence
    cursor.execute("SELECT AVG(ai_confidence) FROM tickets WHERE ai_confidence IS NOT NULL")
    avg_confidence = cursor.fetchone()[0]
    
    print(f"\n👥 USERS:")
    print(f"   Total: {total_users}")
    print(f"   ├─ Admin: {admin_users}")
    print(f"   ├─ Regular: {regular_users}")
    print(f"   └─ Active: {active_users}")
    
    print(f"\n🎫 TICKETS:")
    print(f"   Total: {total_tickets}")
    print(f"   ├─ Open: {open_tickets}")
    print(f"   ├─ In Progress: {in_progress}")
    print(f"   └─ Closed: {closed_tickets}")
    
    print(f"\n⚠️  PRIORITY DISTRIBUTION:")
    print(f"   ├─ Critical: {critical_tickets}")
    print(f"   ├─ High: {high_tickets}")
    print(f"   ├─ Medium: {medium_tickets}")
    print(f"   └─ Low: {low_tickets}")
    
    if categories:
        print(f"\n📂 CATEGORY DISTRIBUTION:")
        for cat, count in categories:
            percentage = (count / total_tickets * 100) if total_tickets > 0 else 0
            print(f"   ├─ {cat}: {count} ({percentage:.1f}%)")
    
    if avg_confidence:
        print(f"\n🤖 AI PERFORMANCE:")
        print(f"   Average Confidence: {avg_confidence*100:.1f}%")
    
    conn.close()
    
    print("\n" + "="*100)

def main():
    print("\n" + "="*100)
    print("NEXORAAI DATABASE VIEWER")
    print("="*100)
    print(f"📁 Database: backend/{DB_PATH}")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'users':
            view_users()
        elif command == 'tickets':
            view_tickets()
        elif command == 'stats':
            view_stats()
        else:
            print("\n❌ Unknown command!")
            print("\n📖 Usage:")
            print("  python view_db.py users    - View all users")
            print("  python view_db.py tickets  - View all tickets")
            print("  python view_db.py stats    - View statistics (default)")
    else:
        # Default: show stats
        view_stats()
        print("\n💡 Tip: Run with 'users' or 'tickets' for detailed views")
        print("\n📖 Examples:")
        print("  python view_db.py users")
        print("  python view_db.py tickets")

if __name__ == '__main__':
    main()
