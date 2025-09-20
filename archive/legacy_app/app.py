from flask import Flask, jsonify
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import platform

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
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
            conn.execute(text("SELECT 1"))
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