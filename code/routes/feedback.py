# code/routes/feedback.py
"""Bug reporting and feedback system"""

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')
bug_reports = []

@feedback_bp.route('/submit', methods=['POST'])
def submit_bug_report():
    data = request.get_json()
    bug_report = {
        'id': len(bug_reports) + 1,
        'screenshot_data': data.get('screenshot'),
        'description': data.get('description', ''),
        'page_url': data.get('page_url', ''),
        'timestamp': datetime.now().isoformat(),
        'status': 'new'
    }
    bug_reports.append(bug_report)
    return jsonify({'success': True, 'bug_id': bug_report['id']})

@feedback_bp.route('/list', methods=['GET'])
def list_bug_reports():
    return jsonify({'reports': bug_reports})
