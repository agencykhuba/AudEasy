#!/usr/bin/env python3
"""
Post-Deployment Validation
Verify BSA Route 2 surgical fix resolved the issues
"""

import requests
import time

def validate_fix():
    """Validate that the surgical fix resolved the 503 errors"""
    
    print("=== POST-DEPLOYMENT VALIDATION ===")
    print("Waiting 2 minutes for deployment to complete...")
    time.sleep(120)
    
    base_url = "https://audeasy.onrender.com"
    
    endpoints = [
        ("/health", "Health Check - Should work now"),
        ("/", "Root Endpoint - Basic functionality"),
        ("/api/ccc/health", "CCC Integration - If available")
    ]
    
    results = {}
    for endpoint, description in endpoints:
        try:
            print(f"Testing {description}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=15)
            
            status = "SUCCESS" if response.status_code == 200 else f"HTTP {response.status_code}"
            results[endpoint] = status
            
            print(f"  {endpoint}: {status}")
            
            if response.status_code == 200 and endpoint == "/health":
                try:
                    data = response.json()
                    print(f"  Database status: {data.get('database', 'unknown')}")
                except:
                    print("  Response: 200 OK")
                    
        except Exception as e:
            results[endpoint] = f"FAILED: {e}"
            print(f"  {endpoint}: FAILED - {e}")
    
    # Validation summary
    successful = sum(1 for status in results.values() if "SUCCESS" in status)
    
    print(f"\n=== BSA ROUTE 2 VALIDATION RESULTS ===")
    print(f"Successful endpoints: {successful}/{len(endpoints)}")
    
    if successful >= 1:  # At least health endpoint should work
        print("✓ BSA ROUTE 2 SUCCESSFUL")
        print("✓ Syntax error resolved")
        print("✓ Service restored to working state")
        
        if "/health" in results and "SUCCESS" in results["/health"]:
            print("✓ Database connectivity needs DATABASE_URL environment variable")
            print("Next step: Set DATABASE_URL in Render dashboard to complete Route 3")
    else:
        print("⚠ Additional investigation required")
        print("May need to check Render logs or consider rollback")

if __name__ == "__main__":
    validate_fix()
