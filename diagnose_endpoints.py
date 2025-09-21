#!/usr/bin/env python3
import re

print("=== ENDPOINT DIAGNOSTIC ===")
print()

# Read the Flask app code
with open('code/app.py', 'r') as f:
    content = f.read()

# Find all @app.route definitions
routes = re.findall(r'@app\.route\(["\']([^"\']+)["\'].*?\)', content)

print("ACTUAL ENDPOINTS DEFINED IN code/app.py:")
for route in routes:
    print(f"  - {route}")

print()
print("ENDPOINT COUNT:", len(routes))
print()

# Check if /health exists
if '/health' in routes:
    print("RESULT: /health endpoint EXISTS")
else:
    print("RESULT: /health endpoint DOES NOT EXIST")
    print("This explains the HTTP 500 error!")
print()

# Show which endpoints would test database connectivity
db_endpoints = [r for r in routes if r in ['/login', '/audit', '/health']]
print("ENDPOINTS THAT USE DATABASE:")
for ep in db_endpoints:
    print(f"  - {ep}")
