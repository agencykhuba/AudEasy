from flask import Blueprint, request, jsonify
import psycopg2
import os
import logging
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'audeasy_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '')
        )
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects with filtering options"""
    vertical_id = request.args.get('vertical_id')
    status = request.args.get('status')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        
        query = """
            SELECT p.id, p.name, p.description, p.status, p.budget_min, p.budget_max,
                   p.start_date, p.end_date, v.display_name as vertical_name,
                   u.username as client_name, p.created_at
            FROM projects p
            JOIN verticals v ON p.vertical_id = v.id
            LEFT JOIN users u ON p.client_id = u.id
            WHERE 1=1
        """
        params = []
        
        if vertical_id:
            query += " AND p.vertical_id = %s"
            params.append(vertical_id)
        
        if status:
            query += " AND p.status = %s"
            params.append(status)
        
        query += " ORDER BY p.created_at DESC"
        
        cur.execute(query, params)
        
        projects = []
        for row in cur.fetchall():
            projects.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'status': row[3],
                'budget_min': float(row[4]) if row[4] else None,
                'budget_max': float(row[5]) if row[5] else None,
                'start_date': row[6].isoformat() if row[6] else None,
                'end_date': row[7].isoformat() if row[7] else None,
                'vertical_name': row[8],
                'client_name': row[9],
                'created_at': row[10].isoformat()
            })
        
        return jsonify({'projects': projects})
        
    except Exception as e:
        logging.error(f"Get projects error: {e}")
        return jsonify({'error': 'Failed to fetch projects'}), 500
    finally:
        conn.close()

@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    required_fields = ['name', 'vertical_id', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projects (name, vertical_id, description, client_id, 
                                budget_min, budget_max, start_date, end_date, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data['name'],
            data['vertical_id'],
            data['description'],
            data.get('client_id'),
            data.get('budget_min'),
            data.get('budget_max'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('metadata', '{}')
        ))
        
        project_id = cur.fetchone()[0]
        conn.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project_id': project_id
        }), 201
        
    except Exception as e:
        logging.error(f"Create project error: {e}")
        return jsonify({'error': 'Failed to create project'}), 500
    finally:
        conn.close()
