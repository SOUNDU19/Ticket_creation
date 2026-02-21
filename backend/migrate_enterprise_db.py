"""
Migrate existing database to enterprise schema
This script safely adds new columns to existing tables
"""

import sqlite3
import os

def migrate_database():
    """Migrate database to enterprise schema"""
    db_path = 'instance/nexora.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found. Please run the application first to create the database.")
        return
    
    print("🚀 Starting Enterprise Database Migration...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(tickets)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add new columns to tickets table if they don't exist
        new_columns = {
            'original_ai_category': 'VARCHAR(50)',
            'overridden_by_admin': 'VARCHAR(36)',
            'merged_into_ticket_id': 'VARCHAR(36)',
            'is_merged': 'BOOLEAN DEFAULT 0',
            'assigned_to': 'VARCHAR(36)',
            'resolved_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE tickets ADD COLUMN {col_name} {col_type}")
                    print(f"✓ Added column: tickets.{col_name}")
                except sqlite3.OperationalError as e:
                    print(f"⚠ Column tickets.{col_name} might already exist: {e}")
        
        # Create internal_notes table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internal_notes (
                id VARCHAR(36) PRIMARY KEY,
                ticket_id VARCHAR(36) NOT NULL,
                admin_id VARCHAR(36) NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id),
                FOREIGN KEY (admin_id) REFERENCES users(id)
            )
        """)
        print("✓ Created/verified internal_notes table")
        
        # Check system_settings table
        cursor.execute("PRAGMA table_info(system_settings)")
        settings_columns = [col[1] for col in cursor.fetchall()]
        
        # Add SLA columns to system_settings if they don't exist
        sla_columns = {
            'sla_critical_hours': 'INTEGER DEFAULT 4',
            'sla_high_hours': 'INTEGER DEFAULT 24',
            'sla_medium_hours': 'INTEGER DEFAULT 48',
            'sla_low_hours': 'INTEGER DEFAULT 72'
        }
        
        for col_name, col_type in sla_columns.items():
            if col_name not in settings_columns:
                try:
                    cursor.execute(f"ALTER TABLE system_settings ADD COLUMN {col_name} {col_type}")
                    print(f"✓ Added column: system_settings.{col_name}")
                except sqlite3.OperationalError as e:
                    print(f"⚠ Column system_settings.{col_name} might already exist: {e}")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Show statistics
        cursor.execute("SELECT COUNT(*) FROM tickets")
        ticket_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM internal_notes")
        note_count = cursor.fetchone()[0]
        
        print("\n📊 Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Tickets: {ticket_count}")
        print(f"   Internal Notes: {note_count}")
        
        print("\n🌐 Access Enterprise Admin Dashboard:")
        print("   http://localhost:8000/admin-dashboard-enhanced.html")
        print("\n" + "="*60)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
