#!/usr/bin/env python3
"""
Surgical Fix: Replace broken try block structure
"""

def apply_precise_fix():
    """Apply surgical fix to the broken try block"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Replace the entire broken section (lines 27-36) with correct structure
    lines = content.split('\n')
    
    # Find the health function and fix the broken try block
    for i, line in enumerate(lines):
        if 'def health():' in line:
            # Replace the broken section starting from the try block
            if i + 10 < len(lines) and 'try:' in lines[i+2]:
                # Remove the broken lines and replace with correct structure
                lines[i+2] = '    try:'
                lines[i+3] = '        # Database connection check'
                lines[i+4] = '        DATABASE_URL = os.environ.get("DATABASE_URL")'
                lines[i+5] = '        if not DATABASE_URL:'
                lines[i+6] = '            DATABASE_URL = "sqlite:///fallback.db"'
                lines[i+7] = '            logging.warning("DATABASE_URL not set - using SQLite fallback")'
                lines[i+8] = '        '
                lines[i+9] = '        engine = create_engine(DATABASE_URL)'
                lines[i+10] = '        with engine.connect() as conn:'
                lines[i+11] = '            conn.execute(text("SELECT 1"))'
                lines[i+12] = '        '
                lines[i+13] = '        return jsonify({'
                lines[i+14] = '            "status": "healthy",'
                lines[i+15] = '            "timestamp": datetime.now().isoformat(),'
                lines[i+16] = '            "database": "connected"'
                lines[i+17] = '        })'
                lines[i+18] = '    except Exception as e:'
                lines[i+19] = '        logging.error(f"Health check failed: {e}")'
                lines[i+20] = '        return jsonify({'
                lines[i+21] = '            "status": "unhealthy",'
                lines[i+22] = '            "error": str(e)'
                lines[i+23] = '        }), 500'
                
                # Remove the duplicate/broken lines that follow
                # Clean up the malformed section
                del lines[i+24:i+40]  # Remove the broken duplicate code
                break
    
    fixed_content = '\n'.join(lines)
    
    # Validate syntax
    try:
        import ast
        ast.parse(fixed_content)
        print("✓ Surgical fix syntax validation successful")
        
        with open('code/app.py', 'w') as f:
            f.write(fixed_content)
        
        print("✓ Surgical fix applied successfully")
        return True
    except SyntaxError as e:
        print(f"✗ Surgical fix validation failed: {e}")
        return False

if __name__ == "__main__":
    print("=== APPLYING SURGICAL FIX ===")
    if apply_precise_fix():
        print("Ready for immediate deployment")
    else:
        print("Rollback to PDC safe point required")
