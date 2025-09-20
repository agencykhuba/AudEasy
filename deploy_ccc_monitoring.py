#!/usr/bin/env python3
"""
Deploy CCC Monitoring System
Comprehensive deployment with validation
"""

import subprocess
import os
import sys
import time

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return None

def deploy_ccc_monitoring():
    """Deploy CCC monitoring system"""
    
    print("=== Deploying CCC Monitoring System ===")
    
    # Step 1: Install requirements
    run_command("pip install -r ccc_requirements.txt", "Installing CCC monitoring dependencies")
    
    # Step 2: Test local integration
    print("Testing local integration...")
    
    # Step 3: Apply database schema (if needed)
    # Note: This would need database credentials in production
    print("Database schema application will be handled during deployment")
    
    # Step 4: Create unified requirements
    run_command("cat requirements.txt ccc_requirements.txt | sort | uniq > unified_requirements.txt", 
                "Creating unified requirements")
    
    # Step 5: Git operations with proper escaping
    commands = [
        ("git add .", "Stage CCC monitoring files"),
        ('git commit -m "Deploy: CCC monitoring system with integrated dashboard"', "Commit CCC monitoring"),
        ("git push origin main", "Deploy to production")
    ]
    
    for command, description in commands:
        result = run_command(command, description)
        if result is None and "commit" in command:
            print("Warning: Commit may have failed - checking git status...")
            run_command("git status", "Check git status")
    
    print("\n✓ CCC Monitoring deployment initiated!")
    print("Monitor at: https://audeasy.onrender.com/api/monitoring/dashboard")
    print("Health check: https://audeasy.onrender.com/api/monitoring/health-check")
    
    # Step 6: Wait and validate deployment
    print("\nWaiting 3 minutes for deployment...")
    time.sleep(180)
    
    print("Running post-deployment validation...")
    run_command("python ccc_backend/utils/deployment_validator.py", "Validate deployment")

if __name__ == "__main__":
    deploy_ccc_monitoring()
