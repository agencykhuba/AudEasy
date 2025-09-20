#!/usr/bin/env python3
"""
Emergency Fix: Syntax Error in app.py
Fix indentation error causing deployment failure
"""

def fix_app_syntax():
    """Fix the syntax error in code/app.py"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Find and fix the broken try block around line 27-30
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'try:' in line and i < len(lines) - 3:
            # Check if next lines have proper indentation
            if 'DATABASE_URL = os.environ.get("DATABASE_URL"' in lines[i+1]:
                # Fix the indentation - ensure proper try block
                lines[i+1] = '    DATABASE_URL = os.environ.get("DATABASE_URL")'
                lines[i+2] = '    if not DATABASE_URL:'
                lines[i+3] = '        DATABASE_URL = "sqlite:///fallback.db"'
                lines[i+4] = '        logging.warning("DATABASE_URL not set - using SQLite fallback")'
                # Add proper except block if missing
                if i+5 < len(lines) and 'except' not in lines[i+5]:
                    lines.insert(i+5, 'except Exception as e:')
                    lines.insert(i+6, '    logging.error(f"Database configuration error: {e}")')
                    lines.insert(i+7, '    DATABASE_URL = "sqlite:///emergency.db"')
                break
    
    # Write fixed content
    fixed_content = '\n'.join(lines)
    
    with open('code/app.py', 'w') as f:
        f.write(fixed_content)
    
    print("✓ Syntax error fixed in app.py")

def validate_syntax():
    """Validate Python syntax"""
    try:
        with open('code/app.py', 'r') as f:
            content = f.read()
        
        import ast
        ast.parse(content)
        print("✓ Python syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error still present: {e}")
        return False

def main():
    """Fix syntax error and deploy"""
    print("=== EMERGENCY SYNTAX FIX ===")
    
    fix_app_syntax()
    
    if validate_syntax():
        print("Ready for deployment")
    else:
        print("Manual syntax fix required")

if __name__ == "__main__":
    main()
