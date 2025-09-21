#!/usr/bin/env python3
"""
Get the current correct database URL for manual environment variable setup
"""

def show_database_url_instructions():
    """Show how to get and set the correct database URL"""
    
    print("=== GET CURRENT DATABASE URL ===")
    print()
    print("Since automatic linking isn't available, you need to:")
    print()
    print("1. Go to your PostgreSQL DATABASE service (separate from web service)")
    print("2. Look for 'Connection Details' or 'Info' tab")
    print("3. Copy the 'Internal Database URL' (not External)")
    print("4. The URL should look like:")
    print("   postgresql://username:password@internal-host:port/database")
    print()
    print("5. Back in your web service Environment section:")
    print("   - Click 'Add' under Environment Variables")
    print("   - Key: DATABASE_URL")
    print("   - Value: [paste the Internal Database URL]")
    print("   - Click Add Environment Variable")
    print()
    print("=== IMPORTANT ===")
    print("- Use INTERNAL Database URL (not external)")
    print("- Internal URL provides better performance")
    print("- Internal URL format: postgresql://user:pass@internal-host:port/db")
    print()
    print("=== EXPECTED RESULT ===")
    print("- Service will auto-redeploy")
    print("- 500 errors should resolve to 200 OK")
    print("- Database authentication should work")

if __name__ == "__main__":
    show_database_url_instructions()
