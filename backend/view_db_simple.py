"""
Simple Database Viewer - View NexoraAI database without extra dependencies
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = 'instance/nexora.db'

def view_users():
    """View all users"""
    print("\n" + "="*80)
    print("👥 USERS TABLE")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, email, mobile, role, company, department, 
               is_active, created_at, last_login
        FROM user
        ORDER BY created_at DESC
    """)
    
    users = cursor.fetchall()
    
    print(f"\nTotal Users: {len(users)}\n")
    
    for user in users:
        user_id, name, email, mobile, role, company, dept, active, created, last_login = user
        print(f"ID: {user_id}")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        print(f"  Mobile: {mobile}")
        print(f"  Role: {role.upper()}")
        print(f"  Company: {company or 'N/A'}")
        print(f"  Department: {dept or 'N/A'}")
        print(f"  Active: {'Yes' if active else 'No'}")
        print(f"  Created: {created}")
        print(f"  Last Login: {last_login or 'Never'}")
        print("-" * 80)
    
    conn.close()

def view_tickets():
    """View all tickets"""
    print("\n" + "="*80)
    print("🎫 TICKETS TABLE")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.id, t.title, t.category, t.priority, t.status,
               t.confidence, u.name as user_name, t.created_at
        FROM ticket t
        LEFT JOIN user u ON t.user_id = u.id
        ORDER BY t.created_at DESC
        LIMIT 20
    """)
    
    tickets = cursor.fetchall()
    
    print(f"\nTotal Tickets (showing last 20): {len(tickets)}\n")
    
    for ticket in tickets:
        tid, title, category, priority, status, confidence, user_name, created = ticket
        print(f"ID: {tid}")
        print(f"  Title: {title}")
        print(f"  Category: {category}")
        print(f"  Priority: {priority.upper()}")
        print(f"  Status: {status}")
        print(f"  AI Confidence: {confidence*100:.1f}%")
        print(f"  Created By: {user_name}")
        print(f"  Created: {created}")
        print("-" * 80)
    
    conn.close()

def view_stats():
    """View database statistics"""
    print("\n" + "="*80)
    print("📊 DATABASE STATISTICS")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User stats
    cursor.execute("SELECT COUNT(*) FROM user")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
    admin_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM user WHERE role='user'")
    regular_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM user WHERE is_active=1")
    active_users = cursor.fetchone()[0]
    
    # Ticket stats
    cursor.execute("SELECT COUNT(*) FROM ticket")
    total_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE status='open'")
    open_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE status='in_progress'")
    in_progress = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE status='closed'")
    closed_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE priority='critical'")
    critical_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ticket WHERE priority='high'")
    high_tickets = cursor.fetchone()[0]
    
    # Category distribution
    cursor.execute("SELECT category, COUNT(*) as count FROM ticket GROUP BY category ORDER BY count DESC")
    categories = cursor.fetchall()
    
    # Average confidence
    cursor.execute("SELECT AVG(confidence) FROM ticket WHERE confidence IS NOT NULL")
    avg_confidence = cursor.fetchone()[0]
    
    print(f"\n👥 USERS:")
    print(f"   Total Users: {total_users}")
    print(f"   ├─ Admin: {admin_users}")
    print(f"   ├─ Regular: {regular_users}")
    print(f"   └─ Active: {active_users}")
    
    print(f"\n🎫 TICKETS:")
    print(f"   Total Tickets: {total_tickets}")
    print(f"   ├─ Open: {open_tickets}")
    print(f"   ├─ In Progress: {in_progress}")
    print(f"   └─ Closed: {closed_tickets}")
    
    print(f"\n⚠️  PRIORITY:")
    print(f"   ├─ Critical: {critical_tickets}")
    print(f"   └─ High: {high_tickets}")
    
    if categories:
        print(f"\n📂 CATEGORIES:")
        for cat, count in categories:
            percentage = (count / total_tickets * 100) if total_tickets > 0 else 0
            print(f"   ├─ {cat}: {count} ({percentage:.1f}%)")
    
    if avg_confidence:
        print(f"\n🤖 AI PERFORMANCE:")
        print(f"   Average Confidence: {avg_confidence*100:.1f}%")
    
    conn.close()
    
    print("\n" + "="*80)

def view_all_tables():
    """View all tables structure"""
    print("\n" + "="*80)
    print("📋 DATABASE STRUCTURE")
    print("="*80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nDatabase: {DB_PATH}")
    print(f"Total Tables: {len(tables)}\n")
    
    for table in tables:
        table_name = table[0]
        print(f"\n📊 TABLE: {table_name}")
        print("-" * 80)
        
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"Columns ({len(columns)}):")
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            markers = []
            if pk:
                markers.append("PRIMARY KEY")
            if not_null:
                markers.append("NOT NULL")
            marker_str = f" [{', '.join(markers)}]" if markers else ""
            print(f"  • {col_name}: {col_type}{marker_str}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\nRows: {count}")
    
    conn.close()
    print("\n" + "="*80)

if __name__ == '__main__':
    import sys
    
    print("\n" + "="*80)
    print("NEXORAAI DATABASE VIEWER")
    print("="*80)
    print(f"Database Location: backend/{DB_PATH}")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'users':
            view_users()
        elif command == 'tickets':
            view_tickets()
        elif command == 'stats':
            view_stats()
        elif command == 'structure':
            view_all_tables()
        else:
            print("\n❌ Unknown command!")
            print("\nUsage:")
            print("  python view_db_simple.py users      - View all users")
            print("  python view_db_simple.py tickets    - View all tickets")
            print("  python view_db_simple.py stats      - View statistics")
            print("  python view_db_simple.py structure  - View database structure")
    else:
        # Default: show stats
        view_stats()
        print("\n💡 Tip: Run with 'users', 'tickets', 'stats', or 'structure' for more details")
        print("\nExamples:")
        print("  python view_db_simple.py users")
        print("  python view_db_simple.py tickets")
