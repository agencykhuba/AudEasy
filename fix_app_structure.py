#!/usr/bin/env python3
"""
Fix Application Structure and Remove Duplicates
Consolidate into single production-ready application
"""

import os
import shutil

def fix_app_structure():
    """Consolidate application structure"""
    
    print("=== Fixing Application Structure ===")
    
    # 1. Archive legacy app directory (it's not being used in production)
    if os.path.exists('app'):
        if os.path.exists('archive'):
            shutil.rmtree('archive')
        shutil.move('app', 'archive/legacy_app')
        print("✓ Archived legacy app directory")
    
    # 2. Create proper Python module structure for CCC
    os.makedirs('ccc_backend', exist_ok=True)
    
    # Create __init__.py files for proper Python modules
    init_files = [
        'ccc_backend/__init__.py',
        'ccc_backend/api/__init__.py',
        'ccc_backend/services/__init__.py',
        'ccc_backend/utils/__init__.py'
    ]
    
    for init_file in init_files:
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        with open(init_file, 'w') as f:
            f.write('# CCC Module\n')
    
    print("✓ Created proper Python module structure")
    
    # 3. Consolidate requirements files
    core_requirements = [
        'Flask==3.0.3',
        'Flask-CORS==4.0.0', 
        'Flask-Bcrypt==1.0.1',
        'psycopg2-binary==2.9.10',
        'PyJWT==2.8.0',
        'requests==2.32.5',
        'python-dotenv==1.0.1',
        'gunicorn==22.0.0',
        'Werkzeug==3.1.3',
        'Jinja2==3.1.6',
        'bcrypt==4.3.0',
        'SQLAlchemy==2.0.43',
        'psutil==5.9.8'
    ]
    
    with open('requirements.txt', 'w') as f:
        for req in core_requirements:
            f.write(f"{req}\n")
    
    # Remove duplicate requirements files
    duplicate_files = [
        'requirements-cpu.txt',
        'unified_requirements.txt',
        'ccc_requirements.txt'
    ]
    
    for file in duplicate_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ Removed duplicate: {file}")
    
    print("✓ Consolidated requirements files")
    
    # 4. Remove duplicate CCC app files, keep only integrated version
    if os.path.exists('ccc_backend/app.py'):
        os.remove('ccc_backend/app.py')
        print("✓ Removed standalone CCC app (using integration instead)")

if __name__ == "__main__":
    fix_app_structure()
