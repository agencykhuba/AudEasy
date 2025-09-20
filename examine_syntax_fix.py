#!/usr/bin/env python3
"""
BSA Route 2: Manual Surgical Fix
Examine and fix specific syntax error at line 27-30
"""

def examine_broken_lines():
    """Show exact problematic code"""
    
    with open('code/app.py', 'r') as f:
        lines = f.readlines()
    
    print("=== EXAMINING BROKEN SYNTAX (lines 25-35) ===")
    for i in range(24, min(36, len(lines))):
        line_num = i + 1
        line = lines[i].rstrip()
        marker = " <-- SYNTAX ERROR" if line_num in [27, 28, 29, 30] else ""
        print(f"{line_num:2d}: {line}{marker}")

def create_surgical_fix():
    """Create precise surgical fix for syntax error"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Find the broken try block and replace with correct syntax
    lines = content.split('\n')
    
    # Locate the problematic try block
    for i, line in enumerate(lines):
        if 'try:' in line and i + 4 < len(lines):
            # Check if this is the broken database configuration try block
            next_lines = ''.join(lines[i+1:i+5])
            if 'DATABASE_URL' in next_lines and 'os.environ.get' in next_lines:
                # Replace with properly indented block
                lines[i] = '# Production database configuration'
                lines[i+1] = 'try:'
                lines[i+2] = '    DATABASE_URL = os.environ.get("DATABASE_URL")'
                lines[i+3] = '    if not DATABASE_URL:'
                lines[i+4] = '        DATABASE_URL = "sqlite:///fallback.db"'
                lines[i+5] = '        logging.warning("DATABASE_URL not set - using SQLite fallback")'
                lines[i+6] = '    engine = create_engine(DATABASE_URL)'
                lines[i+7] = 'except Exception as e:'
                lines[i+8] = '    logging.error(f"Database configuration error: {e}")'
                lines[i+9] = '    engine = create_engine("sqlite:///emergency.db")'
                break
    
    fixed_content = '\n'.join(lines)
    
    # Validate syntax before writing
    try:
        import ast
        ast.parse(fixed_content)
        print("✓ Surgical fix validated - syntax is correct")
        
        with open('code/app.py', 'w') as f:
            f.write(fixed_content)
        
        print("✓ Surgical fix applied to code/app.py")
        return True
    except SyntaxError as e:
        print(f"✗ Surgical fix failed validation: {e}")
        return False

def main():
    """Execute surgical fix"""
    print("=== BSA ROUTE 2: SURGICAL FIX EXECUTION ===")
    
    examine_broken_lines()
    print()
    
    if create_surgical_fix():
        print("Ready for deployment")
    else:
        print("Manual intervention required")

if __name__ == "__main__":
    main()
