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
    """CCC Health Check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Central Command Center',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '1.0.0'
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

@app.route('/api/dashboard/overview', methods=['GET'])
@token_required
def dashboard_overview(current_user_id):
    """Central dashboard overview data"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        
        # Active projects count
        cur.execute("SELECT COUNT(*) FROM projects WHERE status = 'active'")
        active_projects = cur.fetchone()[0]
        
        # Total revenue this month
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM revenue_records 
            WHERE status = 'completed' 
            AND DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)
        """)
        monthly_revenue = float(cur.fetchone()[0])
        
        # Vertical status distribution
        cur.execute("""
            SELECT status, COUNT(*) 
            FROM verticals 
            GROUP BY status
        """)
        vertical_status = dict(cur.fetchall())
        
        # Recent projects
        cur.execute("""
            SELECT p.name, v.display_name, p.status, p.created_at
            FROM projects p
            JOIN verticals v ON p.vertical_id = v.id
            ORDER BY p.created_at DESC
            LIMIT 5
        """)
        recent_projects = []
        for row in cur.fetchall():
            recent_projects.append({
                'name': row[0],
                'vertical': row[1],
                'status': row[2],
                'created_at': row[3].isoformat()
            })
        
        return jsonify({
            'active_projects': active_projects,
            'monthly_revenue': monthly_revenue,
            'vertical_status': vertical_status,
            'recent_projects': recent_projects,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logging.error(f"Dashboard overview error: {e}")
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
