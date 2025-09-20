#!/usr/bin/env python3
"""
Systematic Database Debug Analysis
Identify exact database connectivity issue
"""

import os
import psycopg2

def debug_database_connection():
    """Debug database connection systematically"""
    
    print("=== DATABASE DEBUG ANALYSIS ===")
    
    # Check environment variables that would be available in production
    db_vars = ['DATABASE_URL', 'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    
    print("1. DATABASE CONFIGURATION CHECK:")
    for var in db_vars:
        value = os.environ.get(var, 'NOT_SET')
        # Mask password for security
        if 'PASSWORD' in var and value != 'NOT_SET':
            print(f"{var}: {'*' * len(value)}")
        else:
            print(f"{var}: {value}")
    
    # Check current app.py database connection logic
    print("\n2. APP.PY DATABASE CONNECTION LOGIC:")
    try:
        with open('code/app.py', 'r') as f:
            content = f.read()
        
        # Find database connection patterns
        db_lines = [line.strip() for line in content.split('\n') 
                   if 'psycopg2.connect' in line or 'DATABASE_URL' in line]
        
        print("Database connection code found:")
        for line in db_lines[:3]:  # Show first 3 matches
            print(f"  {line}")
            
    except Exception as e:
        print(f"Failed to analyze app.py: {e}")
    
    print("\n3. SUGGESTED FIXES:")
    print("- Check Render environment variables")
    print("- Verify database connection string format") 
    print("- Test connection with correct credentials")

if __name__ == "__main__":
    debug_database_connection()
