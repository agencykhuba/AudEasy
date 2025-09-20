#!/usr/bin/env python3
"""
Fix remaining issues: datetime import and complete Route 3
"""

def fix_datetime_import():
    """Add missing datetime import"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Check if datetime import exists
    if 'from datetime import datetime' not in content and 'import datetime' not in content:
        # Add datetime import after other imports
        lines = content.split('\n')
        
        # Find a good place to insert the import (after other imports)
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_index = i + 1
        
        lines.insert(insert_index, 'from datetime import datetime')
        
        fixed_content = '\n'.join(lines)
        
        with open('code/app.py', 'w') as f:
            f.write(fixed_content)
        
        print("✓ Added missing datetime import")
        return True
    else:
        print("✓ Datetime import already present")
        return False

def main():
    print("=== FIXING REMAINING ISSUES ===")
    fix_datetime_import()
    
    print("\n=== ROUTE 3 COMPLETION INSTRUCTIONS ===")
    print("1. Fix applied for datetime import")
    print("2. Set DATABASE_URL in Render dashboard:")
    print("   Key: DATABASE_URL")
    print("   Value: postgresql://audeasy_db_user:gPGHjHhaUKw3cuTVEc9KLHTYuI7UW8P8@dpg-d352di8dl3ps738adjkg-a.oregon-postgres.render.com/audeasy_db")
    print("3. This should resolve the database authentication issue")

if __name__ == "__main__":
    main()
