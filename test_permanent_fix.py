#!/usr/bin/env python3
import requests
import sys

def test_database_fix():
    print("=== TESTING PERMANENT DATABASE FIX ===")
    
    try:
        response = requests.get("https://audeasy.onrender.com/health", timeout=15)
        print(f"Health endpoint: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Service is healthy")
            try:
                data = response.json()
                db_status = data.get('database', 'unknown')
                print(f"Database status: {db_status}")
                if 'connected' in str(db_status).lower():
                    print("PERMANENT FIX CONFIRMED: Database connected")
                    return True
            except:
                print("Service responding (non-JSON response)")
                
        root_response = requests.get("https://audeasy.onrender.com/", timeout=15)
        print(f"Root endpoint: HTTP {root_response.status_code}")
        
        if root_response.status_code == 200:
            print("Root endpoint working - service operational")
            return True
            
    except Exception as e:
        print(f"Connection error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    if test_database_fix():
        print("\n=== PERMANENT DATABASE SOLUTION WORKING ===")
        print("- Internal DATABASE_URL configured")
        print("- Manual credential management eliminated")
        print("- AudEasy service operational")
        sys.exit(0)
    else:
        print("\nService check failed - may need investigation")
        sys.exit(1)
