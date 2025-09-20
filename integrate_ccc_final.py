#!/usr/bin/env python3
"""
Final CCC Integration into Main AudEasy Application
Creates single, production-ready application with monitoring
"""

def integrate_ccc():
    """Add CCC routes to main application"""
    
    # Read current app.py
    with open('code/app.py', 'r') as f:
        app_content = f.read()
    
    # Check if CCC integration already exists
    if 'CCC Monitoring Integration' in app_content:
        print("CCC integration already present in main app")
        return
    
    # Add CCC integration at the end
    ccc_integration = '''

# CCC Monitoring Integration
import sys
import os
from datetime import datetime

# Add CCC backend to Python path
ccc_path = os.path.join(os.path.dirname(__file__), '..', 'ccc_backend')
if ccc_path not in sys.path:
    sys.path.insert(0, ccc_path)

try:
    from api.monitoring import monitoring_bp
    app.register_blueprint(monitoring_bp)
    
    @app.route('/api/ccc/health', methods=['GET'])
    def ccc_health():
        return jsonify({
            'status': 'healthy',
            'service': 'Central Command Center',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'integration': 'AudEasy-CCC-Production',
            'monitoring_endpoints': {
                'dashboard': '/api/monitoring/dashboard',
                'health_check': '/api/monitoring/health-check',
                'trigger_deploy': '/api/monitoring/trigger-deploy'
            }
        })
    
    logging.info("CCC monitoring integrated successfully")
    
except Exception as e:
    logging.error(f"CCC integration failed: {e}")
    
    @app.route('/api/ccc/health', methods=['GET'])
    def ccc_health_fallback():
        return jsonify({
            'status': 'degraded',
            'service': 'Central Command Center',
            'integration': 'fallback_mode',
            'error': 'CCC modules not available'
        })
'''

    # Write updated app.py
    with open('code/app.py', 'w') as f:
        f.write(app_content + ccc_integration)
    
    print("✓ CCC integration added to main application")

if __name__ == "__main__":
    integrate_ccc()
