#!/usr/bin/env python3
"""
Post-Deployment Validation Script
Validates clean deployment and CCC integration
"""

import requests
import time

def validate_deployment():
    """Validate deployment is working correctly"""
    
    base_url = "https://audeasy.onrender.com"
    
    print("=== Post-Deployment Validation ===")
    
    # Wait for deployment to complete
    print("Waiting 2 minutes for deployment...")
    time.sleep(120)
    
    endpoints_to_test = [
        ("/health", "AudEasy Main Health"),
        ("/api/ccc/health", "CCC Integration Health"),
        ("/api/monitoring/health-check", "CCC Monitoring Health")
    ]
    
    results = {}
    
    for endpoint, description in endpoints_to_test:
        try:
            print(f"Testing {description}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            
            results[endpoint] = {
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "content": response.json() if response.status_code == 200 else response.text[:200]
            }
            
            if response.status_code == 200:
                print(f"✓ {description}: OK")
            else:
                print(f"⚠ {description}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"✗ {description}: {str(e)}")
            results[endpoint] = {"error": str(e)}
    
    # Summary
    successful = sum(1 for r in results.values() if r.get("status_code") == 200)
    total = len(endpoints_to_test)
    
    print(f"\n=== Validation Summary ===")
    print(f"Successful: {successful}/{total}")
    print(f"Overall Status: {'HEALTHY' if successful == total else 'DEGRADED'}")
    
    return successful == total

if __name__ == "__main__":
    validate_deployment()
