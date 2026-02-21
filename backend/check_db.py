import sqlite3

conn = sqlite3.connect('instance/nexora.db')
cursor = conn.cursor()

print("\n=== TABLES IN DATABASE ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    print(f"\nTable: {table[0]}")
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  Rows: {count}")
    
    if count > 0 and count < 10:
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            print(f"  {row}")

conn.close()
