import re
from typing import Dict

class IndustryRecognizer:
    """AI-powered industry detection from natural language input"""
    
    INDUSTRY_PATTERNS = {
        'food_service': {
            'keywords': ['restaurant', 'cafe', 'coffee', 'food', 'kitchen', 'dining',
                        'fast-casual', 'qsr', 'catering', 'bakery', 'bistro', 'grill'],
            'templates': ['fda_food_code_basic', 'haccp_critical_points', 'allergen_control',
                         'food_temperature_log', 'kitchen_cleanliness', 'employee_hygiene'],
            'regulations': ['FDA Food Code', 'Local Health Department', 'HACCP'],
            'risk_categories': ['Food Safety', 'Equipment', 'Cleanliness', 'Customer Service']
        },
        'retail': {
            'keywords': ['store', 'retail', 'shop', 'boutique', 'outlet', 'mall'],
            'templates': ['retail_safety_checklist', 'customer_service_standards', 'inventory_control'],
            'regulations': ['OSHA', 'ADA', 'Consumer Protection'],
            'risk_categories': ['Safety', 'Customer Service', 'Inventory', 'Compliance']
        }
    }
    
    # EXPANDED: International locations
    LOCATIONS = {
        # United States
        'oregon': {'country': 'US', 'code': 'OR', 'name': 'Oregon'},
        'california': {'country': 'US', 'code': 'CA', 'name': 'California'},
        'new york': {'country': 'US', 'code': 'NY', 'name': 'New York'},
        'texas': {'country': 'US', 'code': 'TX', 'name': 'Texas'},
        'florida': {'country': 'US', 'code': 'FL', 'name': 'Florida'},
        'portland': {'country': 'US', 'code': 'OR', 'name': 'Portland, Oregon'},
        
        # Canada
        'nova scotia': {'country': 'CA', 'code': 'NS', 'name': 'Nova Scotia'},
        'halifax': {'country': 'CA', 'code': 'NS', 'name': 'Halifax, Nova Scotia'},
        'ontario': {'country': 'CA', 'code': 'ON', 'name': 'Ontario'},
        'toronto': {'country': 'CA', 'code': 'ON', 'name': 'Toronto, Ontario'},
        'quebec': {'country': 'CA', 'code': 'QC', 'name': 'Quebec'},
        'british columbia': {'country': 'CA', 'code': 'BC', 'name': 'British Columbia'},
        'vancouver': {'country': 'CA', 'code': 'BC', 'name': 'Vancouver, BC'},
        
        # Middle East
        'qatar': {'country': 'QA', 'code': 'QA', 'name': 'Qatar'},
        'doha': {'country': 'QA', 'code': 'QA', 'name': 'Doha, Qatar'},
        'saudi arabia': {'country': 'SA', 'code': 'SA', 'name': 'Saudi Arabia'},
        'riyadh': {'country': 'SA', 'code': 'SA', 'name': 'Riyadh, Saudi Arabia'},
        'dubai': {'country': 'AE', 'code': 'DU', 'name': 'Dubai, UAE'},
        'uae': {'country': 'AE', 'code': 'AE', 'name': 'United Arab Emirates'},
        
        # Philippines
        'philippines': {'country': 'PH', 'code': 'PH', 'name': 'Philippines'},
        'manila': {'country': 'PH', 'code': 'MM', 'name': 'Manila, Philippines'},
        'cebu': {'country': 'PH', 'code': 'CE', 'name': 'Cebu, Philippines'},
        'davao': {'country': 'PH', 'code': 'DA', 'name': 'Davao, Philippines'},
        
        # Other major markets
        'singapore': {'country': 'SG', 'code': 'SG', 'name': 'Singapore'},
        'hong kong': {'country': 'HK', 'code': 'HK', 'name': 'Hong Kong'},
        'london': {'country': 'GB', 'code': 'LN', 'name': 'London, UK'},
        'sydney': {'country': 'AU', 'code': 'NSW', 'name': 'Sydney, Australia'},
    }
    
    # Country-specific regulations
    COUNTRY_REGULATIONS = {
        'US': ['FDA Food Code', 'OSHA', 'Local Health Department'],
        'CA': ['Canadian Food Inspection Agency (CFIA)', 'Health Canada', 'Provincial Health'],
        'QA': ['Qatar Food Safety', 'Ministry of Public Health', 'QNFSP'],
        'PH': ['FDA Philippines', 'DOH Food Safety', 'LGU Health Office'],
        'SG': ['SFA Singapore', 'NEA', 'Food Safety Standards'],
        'AE': ['Dubai Municipality', 'FSSAI', 'Emirates Food Safety'],
        'GB': ['FSA UK', 'Food Hygiene Rating', 'Local Authority'],
        'AU': ['Food Standards Australia', 'State Health Departments'],
    }
    
    def detect_industry(self, business_description: str) -> Dict:
        description_lower = business_description.lower()
        scores = {}
        
        for industry, config in self.INDUSTRY_PATTERNS.items():
            score = 0
            matched_keywords = []
            for keyword in config['keywords']:
                if keyword in description_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            if score > 0:
                scores[industry] = {
                    'score': score,
                    'confidence': min(score / 5, 1.0),
                    'matched_keywords': matched_keywords,
                    'templates': config['templates'],
                    'regulations': config['regulations'],
                    'risk_categories': config['risk_categories']
                }
        
        if not scores:
            return {
                'industry': 'general',
                'confidence': 0.5,
                'templates': ['general_audit_checklist'],
                'regulations': ['General Compliance'],
                'risk_categories': ['Safety', 'Quality', 'Operations']
            }
        
        best_match = max(scores.items(), key=lambda x: x[1]['score'])
        return {
            'industry': best_match[0],
            'confidence': best_match[1]['confidence'],
            'matched_keywords': best_match[1]['matched_keywords'],
            'templates': best_match[1]['templates'],
            'regulations': best_match[1]['regulations'],
            'risk_categories': best_match[1]['risk_categories']
        }
    
    def extract_location(self, business_description: str) -> Dict:
        """Extract location with international support"""
        description_lower = business_description.lower()
        
        # Check for location matches
        for location_key, location_data in self.LOCATIONS.items():
            if location_key in description_lower:
                country = location_data['country']
                regulations = self.COUNTRY_REGULATIONS.get(country, ['General Compliance'])
                
                return {
                    'location': location_data['name'],
                    'code': location_data['code'],
                    'country': country,
                    'country_name': self._get_country_name(country),
                    'regulations': regulations,
                    'detected': True
                }
        
        return {
            'location': None,
            'code': None,
            'country': None,
            'country_name': None,
            'regulations': ['General Compliance'],
            'detected': False
        }
    
    def _get_country_name(self, country_code: str) -> str:
        """Get full country name from code"""
        country_names = {
            'US': 'United States',
            'CA': 'Canada',
            'QA': 'Qatar',
            'PH': 'Philippines',
            'SG': 'Singapore',
            'AE': 'United Arab Emirates',
            'GB': 'United Kingdom',
            'AU': 'Australia',
            'SA': 'Saudi Arabia',
            'HK': 'Hong Kong'
        }
        return country_names.get(country_code, 'International')
    
    def extract_business_size(self, business_description: str) -> Dict:
        patterns = [r'(\d+)\s*(location|restaurant|store|shop|outlet|branch)']
        for pattern in patterns:
            match = re.search(pattern, business_description.lower())
            if match:
                return {'locations': int(match.group(1)), 'detected': True}
        return {'locations': 1, 'detected': False}
