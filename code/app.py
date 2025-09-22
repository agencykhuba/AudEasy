from flask import Flask, jsonify
import os
import logging
from sqlalchemy import create_engine, text, text
from sqlalchemy.exc import OperationalError
import platform
from datetime import datetime

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
        # Database connection check
        # Render automatic database discovery (handles credential rotation)
        # Priority order: 1) DATABASE_URL (auto-linked), 2) POSTGRES_URL, 3) Fallback
        DATABASE_URL = (
            os.environ.get("DATABASE_URL") or 
            os.environ.get("POSTGRES_URL") or
            os.environ.get("POSTGRESQL_URL")
        )
        
        if not DATABASE_URL:
            logging.warning("No database URL found - using SQLite fallback")
            DATABASE_URL = "sqlite:///emergency.db"
        else:
            logging.info("Database URL automatically discovered from Render environment")
        if not DATABASE_URL:
            DATABASE_URL = "sqlite:///fallback.db"
            logging.warning("DATABASE_URL not set - using SQLite fallback")
        
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        })
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
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

# Import wizard blueprint
from code.routes.wizard import wizard_bp

# Register wizard blueprint
app.register_blueprint(wizard_bp)

print("Wizard routes registered at /wizard")

# Register CAR routes
from code.routes.cars import cars_bp
app.register_blueprint(cars_bp)

# Feedback system
from code.routes.feedback import feedback_bp
app.register_blueprint(feedback_bp)
