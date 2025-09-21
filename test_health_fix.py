#!/usr/bin/env python3
import requests

print("=== TESTING FIXED HEALTH ENDPOINT ===")
print()

try:
    response = requests.get("https://audeasy.onrender.com/health", timeout=30)
    print(f"Status: HTTP {response.status_code}")
    print()
    
    try:
        data = response.json()
        print("Response JSON:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except:
        print(f"Response text: {response.text}")
    
    print()
    if response.status_code == 200:
        print("SUCCESS: Database connection is working!")
    elif response.status_code == 503:
        print("Database connection failed, but now we can see WHY:")
        print("Check the 'error' field above for the actual problem")
    else:
        print(f"Unexpected status: {response.status_code}")
        
except Exception as e:
    print(f"Request failed: {e}")
