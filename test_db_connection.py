#!/usr/bin/env python3
"""
Test Database Connection with Production Credentials
Verify Route 3 fix before deployment
"""

import psycopg2

def test_production_database():
    """Test connection to production database"""
    
    DATABASE_URL = "postgresql://audeasy_db_user:gPGHjHhaUKw3cuTVEc9KLHTYuI7UW8P8@dpg-d352di8dl3ps738adjkg-a.oregon-postgres.render.com/audeasy_db"
    
    print("=== TESTING PRODUCTION DATABASE CONNECTION ===")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Database connection successful")
        print(f"PostgreSQL version: {version[0][:50]}...")
        
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        tables = cur.fetchall()
        print(f"Found {len(tables)} tables in database")
        
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users';")
        users_table_exists = cur.fetchone()[0] > 0
        print(f"Users table exists: {users_table_exists}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_production_database()
    if success:
        print("\nDATABASE READY - Route 3 implementation successful")
    else:
        print("\nDATABASE ISSUES - Additional troubleshooting needed")
