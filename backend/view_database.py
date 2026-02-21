"""
Database Viewer - View all tables and data in NexoraAI database
"""

import sqlite3
import pandas as pd
from tabulate import tabulate

# Database path
DB_PATH = 'instance/nexora.db'

def view_database():
    """View all tables and their data"""
    print("\n" + "="*80)
    print("NEXORAAI DATABASE VIEWER")
    print("="*80)
    print(f"Database: {DB_PATH}\n")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables:\n")
        
        for table in tables:
            table_name = table[0]
            print("="*80)
            print(f"TABLE: {table_name}")
            print("="*80)
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"\n📋 Columns ({len(columns)}):")
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                pk_marker = " [PRIMARY KEY]" if pk else ""
                null_marker = " NOT NULL" if not_null else ""
                print(f"  - {col_name}: {col_type}{pk_marker}{null_marker}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n📈 Total Rows: {count}")
            
            # Show data
            if count > 0:
                print(f"\n📄 Data (showing first 10 rows):\n")
                df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 10", conn)
                print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
            else:
                print("\n⚠️  No data in this table")
            
            print("\n")
        
        conn.close()
        
        print("="*80)
        print("✅ Database view complete!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def view_users():
    """View only users table"""
    print("\n" + "="*80)
    print("USERS TABLE")
    print("="*80)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Get all users
        df = pd.read_sql_query("""
            SELECT 
                id, name, email, mobile, role, 
                company, department, timezone,
                is_active, created_at, last_login
            FROM user
            ORDER BY created_at DESC
        """, conn)
        
        print(f"\n📊 Total Users: {len(df)}\n")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def view_tickets():
    """View only tickets table"""
    print("\n" + "="*80)
    print("TICKETS TABLE")
    print("="*80)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Get all tickets
        df = pd.read_sql_query("""
            SELECT 
                id, title, category, priority, status,
                confidence, user_id, created_at
            FROM ticket
            ORDER BY created_at DESC
            LIMIT 20
        """, conn)
        
        print(f"\n📊 Total Tickets (showing last 20):\n")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def view_stats():
    """View database statistics"""
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # User stats
        cursor.execute("SELECT COUNT(*) FROM user")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
        admin_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user WHERE role='user'")
        regular_users = cursor.fetchone()[0]
        
        # Ticket stats
        cursor.execute("SELECT COUNT(*) FROM ticket")
        total_tickets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE status='open'")
        open_tickets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE status='closed'")
        closed_tickets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE priority='critical'")
        critical_tickets = cursor.fetchone()[0]
        
        # Category distribution
        cursor.execute("SELECT category, COUNT(*) as count FROM ticket GROUP BY category ORDER BY count DESC")
        categories = cursor.fetchall()
        
        print(f"\n👥 USERS:")
        print(f"   Total Users: {total_users}")
        print(f"   Admin Users: {admin_users}")
        print(f"   Regular Users: {regular_users}")
        
        print(f"\n🎫 TICKETS:")
        print(f"   Total Tickets: {total_tickets}")
        print(f"   Open: {open_tickets}")
        print(f"   Closed: {closed_tickets}")
        print(f"   Critical: {critical_tickets}")
        
        if categories:
            print(f"\n📊 CATEGORIES:")
            for cat, count in categories:
                print(f"   {cat}: {count}")
        
        conn.close()
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'users':
            view_users()
        elif command == 'tickets':
            view_tickets()
        elif command == 'stats':
            view_stats()
        elif command == 'all':
            view_database()
        else:
            print("Usage:")
            print("  python view_database.py users    - View users table")
            print("  python view_database.py tickets  - View tickets table")
            print("  python view_database.py stats    - View statistics")
            print("  python view_database.py all      - View all tables")
    else:
        # Default: show stats
        view_stats()
        print("\n💡 Tip: Run with 'users', 'tickets', 'stats', or 'all' for more details")
