# code/services/smart_defaults.py
"""Enhanced AI-powered smart defaults system"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter

class SmartDefaultsEngine:
    """Generate intelligent form defaults based on user patterns and context"""
    
    def __init__(self):
        # In-memory cache (replace with database in production)
        self.user_patterns = {}
    
    def get_defaults(self, user_id: int, form_type: str, context: Dict = None) -> Dict:
        """Get smart defaults for a form"""
        defaults = {}
        context = context or {}
        
        if form_type == 'car_creation':
            defaults = self._get_car_defaults(user_id, context)
        elif form_type == 'action':
            defaults = self._get_action_defaults(user_id, context)
        
        return defaults
    
    def _get_car_defaults(self, user_id: int, context: Dict) -> Dict:
        """Generate defaults for CAR creation"""
        defaults = {}
        
        # Get user's historical patterns
        user_history = self.user_patterns.get(user_id, {})
        
        # Most common location
        if 'locations' in user_history and user_history['locations']:
            location_counts = Counter(user_history['locations'])
            defaults['location'] = location_counts.most_common(1)[0][0]
        else:
            defaults['location'] = 'Walk-in Cooler'
        
        # Most common category
        if 'categories' in user_history and user_history['categories']:
            category_counts = Counter(user_history['categories'])
            defaults['category'] = category_counts.most_common(1)[0][0]
        
        # Time-based defaults
        current_hour = datetime.now().hour
        if current_hour < 12:
            defaults['when'] = 'This morning'
        elif current_hour < 17:
            defaults['when'] = 'This afternoon'
        else:
            defaults['when'] = 'This evening'
        
        # Common products for user's industry
        if 'industry' in context:
            defaults['suggested_products'] = self._get_industry_products(context['industry'])
        
        # Responsible party
        if 'assignees' in user_history and user_history['assignees']:
            assignee_counts = Counter(user_history['assignees'])
            defaults['responsible_person'] = assignee_counts.most_common(1)[0][0]
        
        # Due date (default 3 days)
        avg_days = user_history.get('avg_completion_days', 3)
        defaults['due_date'] = (datetime.now() + timedelta(days=avg_days)).strftime('%Y-%m-%d')
        
        return defaults
    
    def _get_action_defaults(self, user_id: int, context: Dict) -> Dict:
        """Generate defaults for corrective action"""
        defaults = {}
        
        severity = context.get('severity', 'major')
        if severity == 'critical':
            defaults['priority'] = 'high'
            defaults['due_days'] = 1
        elif severity == 'major':
            defaults['priority'] = 'medium'
            defaults['due_days'] = 3
        else:
            defaults['priority'] = 'low'
            defaults['due_days'] = 7
        
        return defaults
    
    def _get_industry_products(self, industry: str) -> List[str]:
        """Get common products for an industry"""
        products = {
            'food_service': ['Chicken', 'Beef', 'Dairy', 'Vegetables', 'Seafood'],
            'retail': ['Perishables', 'Refrigerated items', 'Frozen goods'],
            'healthcare': ['Medical supplies', 'Pharmaceuticals', 'Equipment']
        }
        return products.get(industry.lower().replace(' ', '_'), [])
    
    def learn_from_submission(self, user_id: int, form_type: str, submitted_data: Dict):
        """Learn from user's submissions to improve defaults"""
        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = {
                'locations': [],
                'categories': [],
                'assignees': [],
                'completion_times': []
            }
        
        patterns = self.user_patterns[user_id]
        
        if form_type == 'car_creation':
            if 'location' in submitted_data:
                patterns['locations'].append(submitted_data['location'])
            if 'category' in submitted_data:
                patterns['categories'].append(submitted_data['category'])
            if 'responsible_person' in submitted_data:
                patterns['assignees'].append(submitted_data['responsible_person'])
        
        # Limit history to last 50 entries
        for key in patterns:
            if isinstance(patterns[key], list) and len(patterns[key]) > 50:
                patterns[key] = patterns[key][-50:]
