# code/services/car_text_parser.py
"""
Natural Language CAR Text Parser
Extracts structured data from free-form CAR descriptions
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class CARTextParser:
    """Parse natural language CAR descriptions into structured data"""
    
    CATEGORY_PATTERNS = {
        'Temperature Control': {
            'keywords': ['temperature', 'cooler', 'freezer', 'refrigerat', 'hot', 'cold', 'warm', 'frozen', 'thaw'],
            'weight': 1.0
        },
        'Pest Control': {
            'keywords': ['pest', 'mouse', 'mice', 'rat', 'rodent', 'insect', 'fly', 'cockroach', 'droppings'],
            'weight': 1.0
        },
        'Personal Hygiene': {
            'keywords': ['glove', 'hand', 'wash', 'hygiene', 'uniform', 'hairnet', 'apron', 'jewelry'],
            'weight': 0.9
        },
        'Cross Contamination': {
            'keywords': ['cross', 'contamination', 'raw', 'cooked', 'separate', 'cutting board', 'contact'],
            'weight': 1.0
        },
        'Cleaning & Sanitation': {
            'keywords': ['clean', 'sanit', 'dirty', 'residue', 'chemical', 'detergent', 'sanitizer'],
            'weight': 0.9
        },
        'Equipment Maintenance': {
            'keywords': ['equipment', 'machine', 'broken', 'malfunction', 'repair', 'maintenance', 'leak'],
            'weight': 0.8
        },
        'Documentation': {
            'keywords': ['log', 'record', 'document', 'form', 'checklist', 'missing', 'incomplete'],
            'weight': 0.8
        },
        'Storage & Organization': {
            'keywords': ['storage', 'shelf', 'organize', 'label', 'expired', 'dating', 'fifo'],
            'weight': 0.8
        }
    }
    
    SEVERITY_PATTERNS = {
        'critical': {
            'keywords': ['critical', 'immediate', 'contamination', 'illness', 'outbreak', 'poisoning', 
                        'severe', 'dangerous', 'unsafe', 'health risk', 'life-threatening'],
            'indicators': ['must', 'immediately', 'urgent', 'emergency']
        },
        'major': {
            'keywords': ['major', 'significant', 'serious', 'violation', 'non-compliance', 'regulatory'],
            'indicators': ['should', 'need to', 'requires']
        },
        'minor': {
            'keywords': ['minor', 'small', 'slight', 'cosmetic', 'improvement', 'enhancement'],
            'indicators': ['could', 'might', 'suggest']
        }
    }
    
    TIME_PATTERNS = [
        (r'today', lambda: 'today'),
        (r'yesterday', lambda: 'yesterday'),
        (r'this morning', lambda: 'this morning'),
        (r'lunch rush', lambda: 'during lunch service'),
        (r'dinner service', lambda: 'during dinner service'),
        (r'(\d{1,2}):(\d{2})\s*(am|pm)?', lambda m: f"{m.group(0)}"),
        (r'at\s+(\d{1,2})\s*(am|pm)', lambda m: f"at {m.group(0)}"),
    ]
    
    LOCATION_PATTERNS = [
        r'walk-in\s+(?:cooler|freezer)',
        r'prep\s+(?:area|station|kitchen)',
        r'storage\s+(?:area|room)',
        r'dish\s*(?:washing|washer)?\s+area',
        r'dry\s+storage',
        r'back\s+(?:door|area|room)',
        r'(?:main|front)\s+kitchen',
        r'service\s+area',
    ]
    
    def parse(self, description: str) -> Dict:
        text_lower = description.lower()
        
        return {
            'category': self._extract_category(text_lower),
            'severity': self._extract_severity(text_lower, description),
            'location': self._extract_location(text_lower, description),
            'when': self._extract_time(text_lower, description),
            'affected_products': self._extract_products(text_lower),
            'immediate_risks': self._extract_risks(text_lower),
            'suggested_actions': self._generate_actions(text_lower),
            'related_standards': self._get_related_standards(text_lower),
            'confidence_score': self._calculate_confidence(text_lower)
        }
    
    def _extract_category(self, text: str) -> Tuple[str, float]:
        scores = {}
        for category, config in self.CATEGORY_PATTERNS.items():
            score = 0
            for keyword in config['keywords']:
                if keyword in text:
                    score += config['weight']
            scores[category] = score
        
        if not scores or max(scores.values()) == 0:
            return ('Other', 0.3)
        
        best_category = max(scores.items(), key=lambda x: x[1])
        confidence = min(best_category[1] / 3.0, 1.0)
        return (best_category[0], round(confidence, 2))
    
    def _extract_severity(self, text: str, original: str) -> Tuple[str, str]:
        severity_scores = {'critical': 0, 'major': 0, 'minor': 0}
        
        for severity, config in self.SEVERITY_PATTERNS.items():
            for keyword in config['keywords']:
                if keyword in text:
                    severity_scores[severity] += 2
            for indicator in config['indicators']:
                if indicator in text:
                    severity_scores[severity] += 1
        
        if max(severity_scores.values()) == 0:
            return ('major', 'Unable to determine from description - defaulting to major')
        
        best_severity = max(severity_scores.items(), key=lambda x: x[1])[0]
        
        reasons = []
        if 'contamination' in text or 'illness' in text:
            reasons.append('Food safety risk detected')
        if 'temperature' in text and ('warm' in text or 'hot' in text):
            reasons.append('Temperature abuse indicated')
        if 'immediate' in text or 'urgent' in text:
            reasons.append('Urgency indicated')
        
        reasoning = '; '.join(reasons) if reasons else 'Based on keyword analysis'
        return (best_severity, reasoning)
    
    def _extract_location(self, text: str, original: str) -> Optional[str]:
        for pattern in self.LOCATION_PATTERNS:
            match = re.search(pattern, text)
            if match:
                start, end = match.span()
                return original[start:end].title()
        
        location_match = re.search(r'(?:in|at|near)\s+(?:the\s+)?([a-z\s-]{3,30})', text)
        if location_match:
            return location_match.group(1).strip().title()
        return None
    
    def _extract_time(self, text: str, original: str) -> Optional[str]:
        for pattern, extractor in self.TIME_PATTERNS:
            match = re.search(pattern, text)
            if match:
                if callable(extractor):
                    return extractor(match) if match.groups() else extractor()
        return None
    
    def _extract_products(self, text: str) -> List[str]:
        products = []
        food_items = ['chicken', 'beef', 'pork', 'fish', 'seafood', 'dairy', 'milk', 'cheese',
                     'salad', 'vegetables', 'fruit', 'bread', 'pastries', 'dessert', 'soup',
                     'rice', 'pasta', 'meat', 'eggs', 'produce']
        
        for item in food_items:
            if item in text:
                products.append(item.capitalize())
        return products[:5]
    
    def _extract_risks(self, text: str) -> List[str]:
        risks = []
        risk_indicators = {
            'Food poisoning risk': ['contamination', 'bacteria', 'salmonella', 'e.coli'],
            'Temperature abuse': ['warm', 'hot', 'temperature', 'thaw'],
            'Cross-contamination': ['raw', 'cooked', 'contact', 'cross'],
            'Pest infestation': ['pest', 'rodent', 'droppings', 'insects'],
            'Injury risk': ['sharp', 'broken', 'leak', 'wet floor']
        }
        
        for risk, keywords in risk_indicators.items():
            if any(kw in text for kw in keywords):
                risks.append(risk)
        return risks
    
    def _generate_actions(self, text: str) -> List[Dict[str, str]]:
        actions = []
        
        if 'temperature' in text or 'warm' in text or 'hot' in text:
            actions.append({'action': 'Discard affected products', 'priority': 1})
            actions.append({'action': 'Call refrigeration technician', 'priority': 2})
            actions.append({'action': 'Monitor temperature hourly', 'priority': 3})
        
        if 'pest' in text or 'rodent' in text or 'mouse' in text:
            actions.append({'action': 'Contact pest control service', 'priority': 1})
            actions.append({'action': 'Deep clean affected area', 'priority': 2})
            actions.append({'action': 'Seal entry points', 'priority': 3})
        
        if 'glove' in text or 'hand' in text or 'hygiene' in text:
            actions.append({'action': 'Retrain staff on hygiene protocols', 'priority': 1})
            actions.append({'action': 'Review handwashing procedures', 'priority': 2})
            actions.append({'action': 'Increase supervision', 'priority': 3})
        
        if 'equipment' in text or 'broken' in text or 'malfunction' in text:
            actions.append({'action': 'Tag equipment "Out of Service"', 'priority': 1})
            actions.append({'action': 'Schedule repair/replacement', 'priority': 2})
            actions.append({'action': 'Document equipment failure', 'priority': 3})
        
        return actions[:3]
    
    def _get_related_standards(self, text: str) -> List[str]:
        standards = []
        standard_mapping = {
            'temperature': ['CFIA 4.2 - Cold Storage', 'FDA Food Code 3-501.16'],
            'pest': ['CFIA 5.1 - Pest Prevention', 'FDA Food Code 6-202.15'],
            'hygiene': ['CFIA 3.3 - Food Handler Hygiene', 'FDA Food Code 2-301.11'],
            'cleaning': ['CFIA 6.1 - Cleaning and Sanitizing', 'FDA Food Code 4-601.11'],
            'equipment': ['CFIA 7.2 - Equipment Maintenance', 'FDA Food Code 4-204.11']
        }
        
        for keyword, stds in standard_mapping.items():
            if keyword in text:
                standards.extend(stds)
        return list(set(standards))[:3]
    
    def _calculate_confidence(self, text: str) -> float:
        word_count = len(text.split())
        if word_count < 10:
            return 0.3
        elif word_count < 20:
            return 0.5
        elif word_count < 50:
            return 0.7
        else:
            return 0.9
