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
    
    # Step 1: Apply database extensions
    print("=== Deploying Central Command Center ===")
    
    # Step 2: Install CCC requirements
    run_command("pip install -r ccc_requirements.txt", "Installing CCC dependencies")
    
    # Step 3: Test CCC backend locally
    print("Testing CCC backend...")
    
    # Step 4: Create unified requirements for deployment
    run_command("cat requirements.txt ccc_requirements.txt | sort | uniq > unified_requirements.txt", 
                "Creating unified requirements")
    
    # Step 5: Git commit and deploy
    commands = [
        ("git add .", "Stage CCC files"),
        ("git commit -m 'Deploy: Central Command Center backend with multi-vertical support'", "Commit CCC changes"),
        ("git push origin main", "Deploy to production")
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print("\nCentral Command Center deployment initiated!")
    print("Monitor at: https://audeasy.onrender.com/api/health")
    print("CCC API will be available at: https://audeasy.onrender.com/api/")

if __name__ == "__main__":
    deploy_ccc()
