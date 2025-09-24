# code/routes/quick_audit.py
"""Quick Audit routes for daily pre-shift validation"""

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from datetime import datetime
from code.services.quick_audit import QuickAuditEngine

quick_audit_bp = Blueprint('quick_audit', __name__, url_prefix='/audit')

audit_engine = QuickAuditEngine()

@quick_audit_bp.route('/quick', methods=['GET', 'POST'])
def quick_audit():
    """5-minute daily pre-shift audit"""
    if request.method == 'POST':
        responses = request.get_json() if request.is_json else request.form.to_dict()
        
        # Validate responses
        results = audit_engine.validate_quick_audit(responses)
        
        if results['status'] == 'FAIL':
            # Create emergency CAR
            car_id = audit_engine.create_emergency_car(results['failures'])
            
            return jsonify({
                'status': 'blocked',
                'message': 'OPERATIONS BLOCKED - Critical failures detected',
                'car_id': car_id,
                'failures': results['failures'],
                'action_required': 'Resolve all critical issues before operations'
            }), 403
        
        # PASS - approve operations
        return jsonify({
            'status': 'approved',
            'message': 'All critical checks passed - Cleared for operations',
            'timestamp': results['timestamp'],
            'next_quick_audit': 'Tomorrow 6:00 AM',
            'next_standard_audit': audit_engine.get_next_audit_schedule(1)['standard'].isoformat()
        })
    
    # GET - show quick audit form
    return render_template('audits/quick_audit.html',
        critical_checks=audit_engine.CRITICAL_CHECKS,
        audit_time='5 minutes',
        required_frequency='Daily before shift'
    )

@quick_audit_bp.route('/standard', methods=['GET', 'POST'])
def standard_audit():
    """20-minute weekly comprehensive audit"""
    if request.method == 'POST':
        # Process standard audit (80-120 checks)
        responses = request.get_json() if request.is_json else request.form.to_dict()
        
        # Calculate score
        total_checks = 80
        passed = sum(1 for v in responses.values() if v == 'yes')
        score = int((passed / total_checks) * 100)
        
        return jsonify({
            'status': 'complete',
            'score': score,
            'passed': passed,
            'total': total_checks,
            'grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'F'
        })
    
    # GET - show standard audit form
    return render_template('standard_audit.html',
        categories=['Temperature Control', 'Pest Control', 'Personal Hygiene', 
                   'Cross Contamination', 'Cleaning & Sanitation', 'Equipment Maintenance'],
        audit_time='20 minutes',
        required_frequency='Weekly'
    )

@quick_audit_bp.route('/deep', methods=['GET', 'POST'])
def deep_audit():
    """45-minute monthly deep audit with CAR capability"""
    if request.method == 'POST':
        # Process deep audit with photos and corrective actions
        # This integrates with existing CAR system
        return redirect(url_for('cars.create_car'))
    
    # GET - show deep audit form
    return render_template('deep_audit.html',
        audit_time='45 minutes',
        required_frequency='Monthly',
        includes=['Photos', 'Corrective Actions', 'Root Cause Analysis']
    )

@quick_audit_bp.route('/dashboard')
def audit_dashboard():
    """Dashboard showing all audit tiers and compliance"""
    # TODO: Get real data from database
    
    audit_stats = {
        'today_quick_audit': {'status': 'pending', 'time': '6:00 AM'},
        'this_week_standard': {'status': 'complete', 'score': 92},
        'this_month_deep': {'status': 'scheduled', 'date': '2025-09-30'},
        'compliance_rate': 95,
        'audit_streak': 23  # days without failure
    }
    
    return render_template('audit_dashboard.html',
        stats=audit_stats,
        audit_tiers=audit_engine.audit_tiers
    )

# Add to imports at top of file
from code.services.smart_defaults import SmartDefaultsEngine

# Initialize smart defaults engine
smart_defaults = SmartDefaultsEngine()

# Add before the existing route, new route for smart defaults API
@quick_audit_bp.route('/smart-defaults', methods=['POST'])
def get_smart_defaults():
    """API endpoint for getting smart defaults based on context"""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')  # TODO: Get from session
    location_context = data.get('location_context', {})
    
    defaults = smart_defaults.get_smart_defaults(user_id, location_context)
    
    return jsonify({
        'defaults': defaults,
        'status': 'success',
        'message': f"Found {len(defaults)} smart defaults"
    })

@quick_audit_bp.route('/learn-pattern', methods=['POST'])  
def learn_audit_pattern():
    """Learn from completed audit for future predictions"""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')
    location_context = data.get('location_context', {})
    audit_data = data.get('audit_data', {})
    
    smart_defaults.learn_pattern(user_id, location_context, audit_data)
    
    return jsonify({
        'status': 'success',
        'message': 'Pattern learned successfully'
    })
