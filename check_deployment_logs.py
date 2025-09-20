#!/usr/bin/env python3
"""
Analyze deployment patterns and error indicators
"""

import subprocess
import requests

def analyze_deployment_patterns():
    """Check deployment history and patterns"""
    
    print("=== DEPLOYMENT PATTERN ANALYSIS ===")
    
    # 1. Recent deployment activity
    try:
        result = subprocess.run(['git', 'log', '--oneline', '--since="24 hours ago"'], 
                              capture_output=True, text=True)
        recent_commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        print(f"Commits in last 24h: {len(recent_commits)}")
        for commit in recent_commits[:5]:
            print(f"  {commit}")
    except Exception as e:
        print(f"Deployment history analysis failed: {e}")
    
    # 2. Check for Render deployment indicators
    print("\n2. RENDER DEPLOYMENT ANALYSIS:")
    
    # Check if service responds with any server headers
    try:
        response = requests.head("https://audeasy.onrender.com", timeout=10)
        server_header = response.headers.get('server', 'Unknown')
        print(f"Server header: {server_header}")
        print(f"Response headers count: {len(response.headers)}")
    except Exception as e:
        print(f"Server analysis failed: {e}")
    
    # 3. Test with different endpoints to see deployment state
    print("\n3. ENDPOINT RESPONSE PATTERN:")
    endpoints = ["/", "/health", "/login", "/api/ccc/health"]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"https://audeasy.onrender.com{endpoint}", 
                                  timeout=5, allow_redirects=False)
            print(f"{endpoint}: {response.status_code} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"{endpoint}: FAILED - {type(e).__name__}")

if __name__ == "__main__":
    analyze_deployment_patterns()
