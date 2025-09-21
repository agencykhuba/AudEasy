#!/usr/bin/env python3
"""
Check deployment status and prepare for permanent database linking
"""

import requests
import time

def check_current_deployment():
    """Check if enhanced database discovery is deployed"""
    
    print("=== CHECKING DEPLOYMENT STATUS ===")
    print("Waiting for deployment to complete...")
    time.sleep(60)  # Wait for deployment
    
    try:
        response = requests.get("https://audeasy.onrender.com/health", timeout=15)
        print(f"Health check status: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Service is responding")
            try:
                data = response.json()
                print(f"Database status: {data.get('database', 'unknown')}")
            except:
                print("✓ Service healthy (non-JSON response)")
        else:
            print(f"⚠ Service returning {response.status_code}")
            
    except Exception as e:
        print(f"⚠ Health check failed: {e}")

def show_next_steps():
    """Display the critical next steps for permanent configuration"""
    
    print("\n=== NEXT CRITICAL STEP: RENDER DASHBOARD CONFIGURATION ===")
    print()
    print("You MUST now configure Render dashboard to complete the permanent fix:")
    print()
    print("1. Go to: https://dashboard.render.com")
    print("2. Click on your 'audeasy' WEB SERVICE (not database)")
    print("3. Click 'Environment' in left sidebar")
    print("4. CRITICAL: DELETE the manual DATABASE_URL environment variable")
    print("   (This removes the outdated manual credential)")
    print()
    print("5. Look for database linking option:")
    print("   - 'Add Database' button")
    print("   - 'Connect Database' option") 
    print("   - 'Link Database Service' option")
    print()
    print("6. Select your PostgreSQL database from dropdown")
    print("7. Render will automatically create new DATABASE_URL")
    print("8. Service will auto-redeploy with permanent configuration")
    print()
    print("=== WHY THIS WORKS ===")
    print("- Removes manual credential management")
    print("- Uses Render's automatic database service linking")
    print("- DATABASE_URL auto-updates during credential rotation")
    print("- Eliminates repetitive manual work forever")
    print()
    print("=== EXPECTED RESULT ===")
    print("After linking: No more database authentication errors")
    print("Future credential rotations: Handled automatically")

if __name__ == "__main__":
    check_current_deployment()
    show_next_steps()
