from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone
import psycopg2
import os
from werkzeug.security import check_password_hash
import jwt
import logging

# Configure logging for cloud compatibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ccc-dev-key-2024')

# Import and register monitoring blueprint
try:
    from api.monitoring import monitoring_bp
    app.register_blueprint(monitoring_bp)
    logging.info("Monitoring blueprint registered successfully")
except Exception as e:
    logging.error(f"Failed to register monitoring blueprint: {e}")

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'audeasy_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '')
        )
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None

# Authentication middleware
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'error': 'Token invalid'}), 401
        return f(current_user_id, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/health', methods=['GET'])
def health_check():
    """CCC Health Check with Monitoring Integration"""
    return jsonify({
        'status': 'healthy',
        'service': 'Central Command Center',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '1.0.0',
        'monitoring': 'integrated',
        'endpoints': {
            'monitoring_dashboard': '/api/monitoring/dashboard',
            'health_check': '/api/monitoring/health-check',
            'trigger_deploy': '/api/monitoring/trigger-deploy'
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Unified authentication for all verticals"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user[2], password):
            token = jwt.encode({
                'user_id': user[0],
                'username': user[1],
                'exp': datetime.now(timezone.utc).timestamp() + 3600  # 1 hour
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'token': token,
                'user': {'id': user[0], 'username': user[1]},
                'message': 'Login successful'
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500
    finally:
        conn.close()

@app.route('/api/verticals', methods=['GET'])
@token_required  
def get_verticals(current_user_id):
    """Get all verticals with their status"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT v.id, v.name, v.display_name, v.status, v.description, 
                   v.revenue_model, COUNT(p.id) as project_count,
                   COALESCE(SUM(r.amount), 0) as total_revenue
            FROM verticals v
            LEFT JOIN projects p ON v.id = p.vertical_id
            LEFT JOIN revenue_records r ON v.id = r.vertical_id AND r.status = 'completed'
            GROUP BY v.id, v.name, v.display_name, v.status, v.description, v.revenue_model
            ORDER BY v.id
        """)
        
        verticals = []
        for row in cur.fetchall():
            verticals.append({
                'id': row[0],
                'name': row[1],
                'display_name': row[2],
                'status': row[3],
                'description': row[4],
                'revenue_model': row[5],
                'project_count': row[6],
                'total_revenue': float(row[7])
            })
        
        return jsonify({'verticals': verticals})
        
    except Exception as e:
        logging.error(f"Get verticals error: {e}")
        return jsonify({'error': 'Failed to fetch verticals'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
