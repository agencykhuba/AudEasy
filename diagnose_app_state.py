#!/usr/bin/env python3
"""
Comprehensive Application State Diagnosis
Gathers critical data for BSA analysis
"""

import requests
import subprocess
import os
import time

def diagnose_current_state():
    """Gather comprehensive diagnostic data"""
    
    print("=== DIAGNOSTIC ANALYSIS FOR BSA ===")
    
    # 1. Check what's actually deployed
    print("\n1. CURRENT DEPLOYMENT STATUS:")
    try:
        response = requests.get("https://audeasy.onrender.com/health", timeout=10)
        print(f"Main App Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text[:200]}")
    except Exception as e:
        print(f"Main App: FAILED - {e}")
    
    # 2. Check CCC endpoints
    print("\n2. CCC INTEGRATION STATUS:")
    ccc_endpoints = ["/api/ccc/health", "/api/monitoring/dashboard", "/api/monitoring/health-check"]
    for endpoint in ccc_endpoints:
        try:
            response = requests.get(f"https://audeasy.onrender.com{endpoint}", timeout=10)
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: FAILED - {e}")
    
    # 3. Check local code state
    print("\n3. LOCAL CODE ANALYSIS:")
    try:
        with open('code/app.py', 'r') as f:
            content = f.read()
        
        print(f"Main app.py size: {len(content)} characters")
        print(f"Has CCC integration: {'CCC Monitoring Integration' in content}")
        print(f"Import statements: {content.count('import ')}")
        
        # Check for potential syntax errors
        import ast
        try:
            ast.parse(content)
            print("Syntax: VALID")
        except SyntaxError as e:
            print(f"Syntax: ERROR - {e}")
    except Exception as e:
        print(f"Code analysis failed: {e}")
    
    # 4. Check file structure
    print("\n4. FILE STRUCTURE VALIDATION:")
    
    critical_files = [
        'code/app.py',
        'requirements.txt',
        'ccc_backend/api/monitoring.py',
        'database_extensions/ccc_schema.sql'
    ]
    
    for file in critical_files:
        exists = os.path.exists(file)
        size = os.path.getsize(file) if exists else 0
        print(f"{file}: {'EXISTS' if exists else 'MISSING'} ({size} bytes)")
    
    # 5. Git status
    print("\n5. VERSION CONTROL STATUS:")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print(f"Uncommitted changes: {uncommitted}")
        
        log_result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                                  capture_output=True, text=True)
        print("Recent commits:")
        for line in log_result.stdout.strip().split('\n')[:3]:
            print(f"  {line}")
    except Exception as e:
        print(f"Git analysis failed: {e}")

if __name__ == "__main__":
    diagnose_current_state()
