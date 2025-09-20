#!/usr/bin/env python3
"""
Test with the exact external database URL provided
"""

import psycopg2

def test_external_database():
    """Test with exact external URL"""
    
    # Use the exact external URL you provided
    EXTERNAL_URL = "postgresql://audeasy_db_user:gPGHjHhaUKw3cuTVEc9KLHTYuI7UW8P8@dpg-d352di8dl3ps738adjkg-a.oregon-postgres.render.com/audeasy_db"
    
    print("=== TESTING WITH EXTERNAL DATABASE URL ===")
    
    try:
        conn = psycopg2.connect(EXTERNAL_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print("✓ External database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ External database failed: {e}")
        return False

if __name__ == "__main__":
    test_external_database()
