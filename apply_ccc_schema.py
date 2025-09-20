#!/usr/bin/env python3
"""
Apply CCC Database Schema to Production
Extends existing AudEasy database with CCC tables
"""

import psycopg2
import os
import logging

def apply_ccc_schema():
    """Apply CCC database schema"""
    
    # Read schema file
    with open('database_extensions/ccc_schema.sql', 'r') as f:
        schema_sql = f.read()
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'audeasy_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '')
        )
        
        cur = conn.cursor()
        
        # Execute schema
        cur.execute(schema_sql)
        conn.commit()
        
        print("✓ CCC database schema applied successfully")
        
        # Verify tables created
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name IN 
            ('verticals', 'projects', 'service_health', 'revenue_records', 'system_metrics')
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        print(f"✓ CCC tables created: {', '.join(tables)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Schema application failed: {e}")
        return False

if __name__ == "__main__":
    apply_ccc_schema()
