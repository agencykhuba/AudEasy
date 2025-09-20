from flask import Flask, jsonify
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import platform

# Configure logging (per implementation_roadmap.md Phase 4)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

@app.route("/")
def index():
    logging.info("Root route accessed")
    return jsonify({"status": "AudEasy MVP running - Audit & CAPA Workflow"}), 200

@app.route("/health")
def health():
    logging.info("Health check initiated")
    try:
        engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///test.db"))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Fix: Use text() for SQLAlchemy 2.0+
        return jsonify({"ok": True, "db": "connected"}), 200
    except OperationalError as e:
        logging.error(f"DB connection failed: {str(e)}")
        return jsonify({"ok": False, "db": "failed", "error": str(e)}), 503

@app.route("/audit", methods=["GET"])
def audit():
    logging.info("Audit route accessed")
    return jsonify({
        "categories": [
            "Customer Delight & Ops Excellence",
            "Admin, Financial Control & Maintenance",
            "People Development & QA Compliance"
        ],
        "total_items": 119
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if platform.system() == "Windows":
        from waitress import serve
        logging.info(f"Starting Waitress on port {port}")
        serve(app, host="0.0.0.0", port=port)
    else:
        app.run(debug=False, host="0.0.0.0", port=port)
# CCC Monitoring Integration
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ccc_backend'))
    
    from api.monitoring import monitoring_bp
    app.register_blueprint(monitoring_bp)
    
    # Add CCC health endpoint to existing app
    @app.route('/api/ccc/health', methods=['GET'])
    def ccc_health():
        return jsonify({
            'status': 'healthy',
            'service': 'Central Command Center',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'integration': 'AudEasy-CCC',
            'monitoring_endpoints': {
                'dashboard': '/api/monitoring/dashboard',
                'health_check': '/api/monitoring/health-check',
                'trigger_deploy': '/api/monitoring/trigger-deploy'
            }
        })
    
    logging.info("CCC monitoring integrated successfully into AudEasy")
    
except Exception as e:
    logging.error(f"Failed to integrate CCC monitoring: {e}")
