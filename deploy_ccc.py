#!/usr/bin/env python3
"""
CCC Deployment Script
Extends existing AudEasy infrastructure with Central Command Center
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {description} failed: {e.stderr}")
        return None

def deploy_ccc():
    """Deploy Central Command Center"""
    
    print("=== Deploying Central Command Center ===")
    
    # Step 1: Install CCC requirements
    run_command("pip install -r ccc_requirements.txt", "Installing CCC dependencies")
    
    # Step 2: Create unified requirements for deployment
    run_command("cat requirements.txt ccc_requirements.txt | sort | uniq > unified_requirements.txt", 
                "Creating unified requirements")
    
    # Step 3: Git operations with proper escaping
    commands = [
        ("git add .", "Stage CCC files"),
        ('git commit -m "Deploy: Central Command Center backend with multi-vertical support"', "Commit CCC changes"),
        ("git push origin main", "Deploy to production")
    ]
    
    for command, description in commands:
        result = run_command(command, description)
        if result is None and "commit" in command:
            print("Warning: Commit may have failed due to no changes or existing commit")
    
    print("\nCentral Command Center deployment initiated!")
    print("Monitor at: https://audeasy.onrender.com/api/health")
    print("CCC API will be available at: https://audeasy.onrender.com/api/")

if __name__ == "__main__":
    deploy_ccc()
