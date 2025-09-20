#!/usr/bin/env python3
"""
Configure Database Connection with Provided Credentials
Complete Route 3 implementation
"""

def update_database_configuration():
    """Update app.py with proper database configuration"""
    
    with open('code/app.py', 'r') as f:
        content = f.read()
    
    # Check if we already have the robust database logic
    if 'Robust database connection with error handling' in content:
        print("✓ Database logic already updated")
        return
    
    # Find and replace the database connection
    old_pattern = 'engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///test.db"))'
    
    new_database_logic = '''
# Production database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", 
    "postgresql://audeasy_db_user:gPGHjHhaUKw3cuTVEc9KLHTYuI7UW8P8@dpg-d352di8dl3ps738adjkg-a.oregon-postgres.render.com/audeasy_db")

try:
    engine = create_engine(DATABASE_URL)
    # Test connection on startup
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logging.info("Database connection successful")
except Exception as e:
    logging.error(f"Database connection failed: {e}")
    # Fallback for development
    engine = create_engine("sqlite:///fallback.db")
    logging.warning("Using SQLite fallback")'''
    
    if old_pattern in content:
        updated_content = content.replace(old_pattern, new_database_logic)
        
        # Add required imports
        if 'from sqlalchemy import text' not in updated_content:
            # Find SQLAlchemy import line
            import_line = 'from sqlalchemy import create_engine'
            if import_line in updated_content:
                updated_content = updated_content.replace(import_line, 'from sqlalchemy import create_engine, text')
        
        with open('code/app.py', 'w') as f:
            f.write(updated_content)
        
        print("✓ Database configuration updated with production credentials")
    else:
        print("⚠ Database pattern not found - may need manual update")

if __name__ == "__main__":
    update_database_configuration()
