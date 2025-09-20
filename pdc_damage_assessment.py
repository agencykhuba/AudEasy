#!/usr/bin/env python3
"""
Process And Damage Control (PDC) Assessment
Analyze file integrity and identify damage from recent changes
"""

import subprocess
import os
from datetime import datetime

def analyze_git_history():
    """Analyze recent commits for file damage assessment"""
    
    print("=== PDC: GIT HISTORY ANALYSIS ===")
    
    try:
        # Get last 5 commits with file changes
        result = subprocess.run(['git', 'log', '--oneline', '--stat', '-5'], 
                              capture_output=True, text=True)
        
        print("Recent commits and file changes:")
        print(result.stdout)
        
        # Get specific changes to code/app.py
        app_changes = subprocess.run(['git', 'log', '--oneline', '-10', '--', 'code/app.py'], 
                                   capture_output=True, text=True)
        
        print("\ncode/app.py change history:")
        print(app_changes.stdout)
        
    except Exception as e:
        print(f"Git history analysis failed: {e}")

def check_file_integrity():
    """Check integrity of critical files"""
    
    print("\n=== PDC: FILE INTEGRITY CHECK ===")
    
    critical_files = {
        'code/app.py': 'Main application file',
        'requirements.txt': 'Dependencies',
        'database_extensions/ccc_schema.sql': 'Database schema'
    }
    
    integrity_status = {}
    
    for file_path, description in critical_files.items():
        if os.path.exists(file_path):
            try:
                size = os.path.getsize(file_path)
                
                # Check if Python file has syntax errors
                if file_path.endswith('.py'):
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        import ast
                        ast.parse(content)
                        syntax_status = "VALID"
                    except SyntaxError as e:
                        syntax_status = f"SYNTAX ERROR: {e}"
                else:
                    syntax_status = "N/A"
                
                integrity_status[file_path] = {
                    'exists': True,
                    'size': size,
                    'syntax': syntax_status,
                    'status': 'DAMAGED' if 'ERROR' in syntax_status else 'OK'
                }
                
                print(f"{file_path}: {integrity_status[file_path]['status']} ({size} bytes) - {syntax_status}")
                
            except Exception as e:
                integrity_status[file_path] = {'error': str(e), 'status': 'ERROR'}
                print(f"{file_path}: ERROR - {e}")
        else:
            integrity_status[file_path] = {'exists': False, 'status': 'MISSING'}
            print(f"{file_path}: MISSING")
    
    return integrity_status

def identify_last_working_commit():
    """Identify the last commit before syntax errors"""
    
    print("\n=== PDC: LAST WORKING STATE ANALYSIS ===")
    
    # Check commit messages for error-related commits
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                              capture_output=True, text=True)
        
        commits = result.stdout.strip().split('\n')
        
        print("Recent commits (newest first):")
        for i, commit in enumerate(commits):
            commit_hash = commit.split()[0]
            commit_msg = ' '.join(commit.split()[1:])
            
            # Identify potentially problematic commits
            risk_indicators = ['fix', 'emergency', 'syntax', 'error', 'database']
            is_risky = any(indicator in commit_msg.lower() for indicator in risk_indicators)
            
            status = "RISKY" if is_risky else "SAFE"
            print(f"  {i}: {commit_hash} - {commit_msg} [{status}]")
        
        # Suggest rollback target
        safe_commits = [c for c in commits if not any(indicator in c.lower() for indicator in risk_indicators)]
        if safe_commits:
            rollback_target = safe_commits[0].split()[0]
            print(f"\nSuggested rollback target: {rollback_target}")
            return rollback_target
        
    except Exception as e:
        print(f"Commit analysis failed: {e}")
    
    return None

def main():
    """Execute PDC damage assessment"""
    
    print("=== PROCESS AND DAMAGE CONTROL (PDC) ASSESSMENT ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    analyze_git_history()
    integrity_status = check_file_integrity()
    rollback_target = identify_last_working_commit()
    
    # Summary
    damaged_files = [f for f, status in integrity_status.items() if status.get('status') == 'DAMAGED']
    
    print(f"\n=== PDC SUMMARY ===")
    print(f"Damaged files: {len(damaged_files)}")
    if damaged_files:
        print(f"Files requiring attention: {', '.join(damaged_files)}")
    
    if rollback_target:
        print(f"Safe rollback target available: {rollback_target}")

if __name__ == "__main__":
    main()
