#!/usr/bin/env python3
"""
Directory Cleanup and Maintenance Script
Removes orphaned files and maintains clean project structure
"""

import os
import glob
import shutil
from datetime import datetime

class DirectoryMaintenance:
    def __init__(self):
        self.project_root = os.getcwd()
        self.cleanup_log = []
        
    def scan_for_orphaned_files(self):
        """Identify orphaned and unnecessary files"""
        orphaned_patterns = [
            "*.backup",
            "*_backup.*",
            "*.old",
            "*.tmp",
            "*.temp",
            "*~",
            "requirements_backup.txt",
            "ccc_requirements_monitoring.txt"  # Duplicate content
        ]
        
        orphaned_files = []
        for pattern in orphaned_patterns:
            orphaned_files.extend(glob.glob(pattern, recursive=True))
            
        return orphaned_files
    
    def scan_for_duplicate_files(self):
        """Identify duplicate files with same content"""
        # Check for duplicate requirements files
        req_files = glob.glob("*requirements*.txt")
        print(f"Requirements files found: {req_files}")
        
        # Check for duplicate app files
        app_files = glob.glob("**/app*.py", recursive=True)
        print(f"App files found: {app_files}")
        
        return {
            "requirements": req_files,
            "applications": app_files
        }
    
    def clean_orphaned_files(self, orphaned_files):
        """Remove orphaned files"""
        for file in orphaned_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    self.cleanup_log.append(f"Removed orphaned file: {file}")
                    print(f"✓ Removed: {file}")
                except Exception as e:
                    print(f"✗ Failed to remove {file}: {e}")
    
    def create_maintenance_log(self):
        """Create maintenance log"""
        log_content = f"""
# Directory Maintenance Log
Date: {datetime.now().isoformat()}

## Files Removed:
{chr(10).join(self.cleanup_log) if self.cleanup_log else "No files removed"}

## Current Structure:
- Core Application: code/app.py
- CCC Backend: ccc_backend/
- Database Extensions: database_extensions/
- Requirements: requirements.txt, ccc_requirements.txt
- Deployment Scripts: deploy_ccc_monitoring.py, apply_ccc_schema.py
"""
        
        with open('.maintenance_log.md', 'w') as f:
            f.write(log_content)
    
    def run_maintenance(self):
        """Run complete directory maintenance"""
        print("=== Directory Maintenance Started ===")
        
        orphaned = self.scan_for_orphaned_files()
        duplicates = self.scan_for_duplicate_files()
        
        if orphaned:
            print(f"Found {len(orphaned)} orphaned files:")
            for file in orphaned:
                print(f"  - {file}")
            
            response = input("Remove these files? (y/n): ")
            if response.lower() == 'y':
                self.clean_orphaned_files(orphaned)
        
        self.create_maintenance_log()
        print("=== Directory Maintenance Completed ===")

if __name__ == "__main__":
    maintenance = DirectoryMaintenance()
    maintenance.run_maintenance()
