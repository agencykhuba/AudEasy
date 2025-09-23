# code/services/quick_audit.py
"""Quick Audit System - 5-10 minute daily pre-shift validation"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import and_

class QuickAuditEngine:
    """Engine for managing three-tier audit system"""
    
    # Critical checks that MUST pass for operations
    CRITICAL_CHECKS = {
        'temperature_control': {
            'walk_in_cooler': {'max': 4, 'unit': '°C', 'critical': True},
            'freezer': {'max': -18, 'unit': '°C', 'critical': True},
            'hot_hold': {'min': 60, 'unit': '°C', 'critical': True}
        },
        'food_safety': {
            'hand_wash_stations': {'status': 'functional', 'critical': True},
            'cross_contamination_control': {'status': 'compliant', 'critical': True},
            'allergen_separation': {'status': 'proper', 'critical': True}
        },
        'sanitation': {
            'sanitizer_concentration': {'min': 200, 'max': 400, 'unit': 'ppm', 'critical': True},
            'equipment_cleanliness': {'status': 'clean', 'critical': True}
        },
        'personnel': {
            'sick_employee_policy': {'status': 'compliant', 'critical': True},
            'proper_uniforms': {'status': 'yes', 'critical': True}
        }
    }
    
    def __init__(self):
        self.audit_tiers = {
            'quick': {'time': 5, 'checks': 10, 'frequency': 'daily'},
            'standard': {'time': 20, 'checks': 80, 'frequency': 'weekly'},
            'deep': {'time': 45, 'checks': 120, 'frequency': 'monthly'}
        }
    
    def validate_quick_audit(self, responses: Dict) -> Dict:
        """Validate quick audit responses - PASS/FAIL only"""
        failures = []
        
        for category, checks in self.CRITICAL_CHECKS.items():
            for check_name, criteria in checks.items():
                response = responses.get(f"{category}_{check_name}")
                
                if not self._check_passes(response, criteria):
                    failures.append({
                        'category': category,
                        'check': check_name,
                        'expected': criteria,
                        'actual': response,
                        'severity': 'critical'
                    })
        
        return {
            'status': 'PASS' if len(failures) == 0 else 'FAIL',
            'failures': failures,
            'passed_checks': 10 - len(failures),
            'total_checks': 10,
            'timestamp': datetime.now().isoformat(),
            'operations_approved': len(failures) == 0
        }
    
    def _check_passes(self, value, criteria: Dict) -> bool:
        """Determine if individual check passes"""
        if 'min' in criteria and 'max' in criteria:
            try:
                val = float(value)
                return criteria['min'] <= val <= criteria['max']
            except (ValueError, TypeError):
                return False
        
        if 'max' in criteria:
            try:
                return float(value) <= criteria['max']
            except (ValueError, TypeError):
                return False
        
        if 'min' in criteria:
            try:
                return float(value) >= criteria['min']
            except (ValueError, TypeError):
                return False
        
        if 'status' in criteria:
            return str(value).lower() == str(criteria['status']).lower()
        
        return False
    
    def get_next_audit_schedule(self, location_id: int) -> Dict:
        """Determine next required audit for location"""
        # TODO: Query database for last audits
        # For now, return template
        return {
            'quick': datetime.now().replace(hour=6, minute=0, second=0),
            'standard': datetime.now() + timedelta(days=7),
            'deep': datetime.now() + timedelta(days=30)
        }
    
    def create_emergency_car(self, failures: List[Dict]) -> int:
        """Auto-create CAR for critical failures"""
        # TODO: Integrate with existing CAR system
        description = "CRITICAL FAILURE - Pre-shift audit blocked operations:\n\n"
        
        for failure in failures:
            description += f"- {failure['category']}: {failure['check']}\n"
            description += f"  Expected: {failure['expected']}\n"
            description += f"  Actual: {failure['actual']}\n\n"
        
        # Return mock CAR ID for now
        return 999
