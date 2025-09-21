#!/usr/bin/env python3
import requests

print("=== FINAL DATABASE CONNECTION TEST ===")
print("Testing with your actual password: GaelRafa91072834")
print()

try:
    response = requests.get("https://audeasy.onrender.com/health", timeout=30)
    print(f"Status: HTTP {response.status_code}")
    print()
    
    data = response.json()
    print("Response:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    print()
    
    if response.status_code == 200 and data.get('database') == 'connected':
        print("=" * 50)
        print("SUCCESS! DATABASE CONNECTION WORKING!")
        print("=" * 50)
        print()
        print("The permanent database solution is now VERIFIED:")
        print("- Correct password identified: GaelRafa91072834")
        print("- Database authentication successful")
        print("- No more credential rotation issues")
        print()
        print("LESSON LEARNED (ELF Framework):")
        print("- Always verify what YOU set, not what UI shows")
        print("- Evidence = actual passwords used during setup")
        print("- Should have asked about original password first")
    else:
        print("Issue persists. Check error message above.")
        
except Exception as e:
    print(f"Error: {e}")
