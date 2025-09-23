#!/usr/bin/env python3
"""
AudEasy Local Development Server
==================================
Workaround for Python stdlib 'code' module conflict on Windows.

Production uses: gunicorn code.app:app (Linux/Render)
Local dev uses: python run_local.py (Windows)

This script bypasses the module name conflict by directly importing
and serving the Flask app without relying on string-based module resolution.
"""

import sys
import os

# Add project root to Python path before any imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import - the path manipulation allows 'code' package to work
from waitress import serve
from code.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("AudEasy Local Development Server")
    print("=" * 60)
    print(f"Environment: Development (Windows)")
    print(f"Server: Waitress (Windows-compatible WSGI)")
    print(f"URL: http://127.0.0.1:5000")
    print(f"Quick Audit: http://127.0.0.1:5000/audit/quick")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    serve(app, host='127.0.0.1', port=5000, threads=4)
