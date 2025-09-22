from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from code.services.industry_recognizer import IndustryRecognizer

wizard_bp = Blueprint('wizard', __name__, url_prefix='/wizard')
recognizer = IndustryRecognizer()
wizard_sessions = {}

@wizard_bp.route('/start', methods=['GET', 'POST'])
def start_wizard():
    if request.method == 'POST':
        data = request.json
        business_description = data.get('business_description', '')
        
        industry_data = recognizer.detect_industry(business_description)
        location_data = recognizer.extract_location(business_description)
        size_data = recognizer.extract_business_size(business_description)
        
        wizard_id = len(wizard_sessions) + 1
        wizard_sessions[wizard_id] = {
            'step': 1,
            'business_info': {
                'description': business_description,
                'industry': industry_data['industry'],
                'confidence': industry_data['confidence'],
                'location': location_data,
                'size': size_data
            },
            'industry_config': {
                'templates': industry_data['templates'],
                'regulations': industry_data['regulations']
            }
        }
        
        return jsonify({
            'success': True,
            'wizard_id': wizard_id,
            'industry_detected': industry_data,
            'location': location_data,
            'size': size_data,
            'templates_available': len(industry_data['templates'])
        })
    
    return render_template('wizard/step1_business.html')
