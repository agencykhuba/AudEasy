#!/usr/bin/env python3
"""
Route 3: Use Render API to retrieve database credentials
Professional approach using official Render API
"""

import requests
import os

def get_render_api_credentials():
    """
    Guide for setting up Render API access
    """
    
    print("=== ROUTE 3: RENDER API SETUP REQUIRED ===")
    print("\nTo use Render API, you need to:")
    print("1. Go to https://dashboard.render.com/account")
    print("2. Navigate to 'API Keys' section")
    print("3. Create a new API key")
    print("4. Copy the API key")
    print("5. Run this script with the API key")
    
    api_key = input("\nEnter your Render API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("Skipping API approach - manual environment variable setup required")
        return None
    
    return api_key

def list_render_services(api_key):
    """List all Render services to find database and web service IDs"""
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get('https://api.render.com/v1/services', headers=headers)
        
        if response.status_code == 200:
            services = response.json()
            print(f"Found {len(services)} services:")
            
            database_services = []
            web_services = []
            
            for service in services:
                service_type = service.get('type', 'unknown')
                service_name = service.get('name', 'unnamed')
                service_id = service.get('id', 'no-id')
                
                print(f"  - {service_name} ({service_type}): {service_id}")
                
                if service_type == 'postgresql':
                    database_services.append(service)
                elif service_type == 'web':
                    web_services.append(service)
            
            return {
                'databases': database_services,
                'web_services': web_services
            }
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"API Request failed: {e}")
        return None

def update_app_with_env_vars():
    """Update app.py to use proper environment variable handling"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Find and replace database configuration section
    if 'DATABASE_URL = os.environ.get("DATABASE_URL"' in content:
        # Already using environment variables
        print("✓ App already configured for environment variables")
        return True
    
    # Find the current database configuration and replace
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'DATABASE_URL =' in line and 'postgresql://' in line:
            # Replace hardcoded credentials with environment variable
            lines[i] = '''# Use DATABASE_URL from Render environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Development fallback
    DATABASE_URL = "sqlite:///fallback.db"
    logging.warning("DATABASE_URL not set - using SQLite fallback")'''
            break
    
    updated_content = '\n'.join(lines)
    
    with open('code/app.py', 'w') as f:
        f.write(updated_content)
    
    print("✓ App updated to use DATABASE_URL environment variable")
    return True

def main():
    """Execute Route 3 with Render API"""
    
    print("=== ROUTE 3: RENDER API APPROACH ===")
    
    # Option 1: Try API approach
    api_key = get_render_api_credentials()
    
    if api_key:
        services = list_render_services(api_key)
        if services:
            print("\nDatabase services found:")
            for db in services['databases']:
                print(f"  Database: {db['name']} (ID: {db['id']})")
            
            print("\nNext step: You'll need to set DATABASE_URL in your web service environment variables")
    
    # Option 2: Configure app for environment variables (always do this)
    print("\n=== CONFIGURING APP FOR ENVIRONMENT VARIABLES ===")
    update_app_with_env_vars()
    
    print("\n=== ROUTE 3 COMPLETION STEPS ===")
    print("1. ✓ App configured for environment variables")
    print("2. Manual: Set DATABASE_URL in Render web service dashboard")
    print("3. Deploy updated application")
    print("4. Verify database connection")

if __name__ == "__main__":
    main()
