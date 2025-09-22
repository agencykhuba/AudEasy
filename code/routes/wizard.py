# code/routes/wizard.py
"""Smart Setup Wizard Routes with Natural Language CAR Processing"""

from flask import Blueprint, render_template, request, jsonify, session
from code.services.industry_recognizer import IndustryRecognizer
from code.services.car_text_parser import CARTextParser
from code.models.wizard import WizardSession, IndustryTemplate
from datetime import datetime
import uuid

wizard_bp = Blueprint('wizard', __name__, url_prefix='/wizard')
industry_recognizer = IndustryRecognizer()
car_parser = CARTextParser()

wizard_sessions = {}

@wizard_bp.route('/start', methods=['GET'])
def start_wizard():
    session_id = str(uuid.uuid4())
    wizard_sessions[session_id] = WizardSession(session_id=session_id, created_at=datetime.now())
    session['wizard_session_id'] = session_id
    return render_template('wizard/step1.html', session_id=session_id)

@wizard_bp.route('/process-step1', methods=['POST'])
def process_step1():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    description = request.form.get('description', '')
    analysis = industry_recognizer.analyze_business(description)
    
    wizard_sessions[session_id].business_info = {
        'description': description,
        'industry': analysis['industry'],
        'location': analysis['location'],
        'size': analysis['business_size'],
        'standards': analysis['applicable_standards'],
        'confidence': analysis['confidence']
    }
    
    return jsonify({'success': True, 'analysis': analysis, 'next_step': '/wizard/step2'})

@wizard_bp.route('/step2', methods=['GET'])
def show_step2():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return render_template('wizard/step1.html')
    
    wizard_session = wizard_sessions[session_id]
    industry = wizard_session.business_info.get('industry', {}).get('name', 'general')
    templates = IndustryTemplate.get_templates_for_industry(industry)
    
    return render_template('wizard/step2.html', templates=templates, industry=industry)

@wizard_bp.route('/process-step2', methods=['POST'])
def process_step2():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    selected_templates = request.form.getlist('templates')
    wizard_sessions[session_id].selected_templates = selected_templates
    
    return jsonify({'success': True, 'next_step': '/wizard/step3'})

@wizard_bp.route('/step3', methods=['GET'])
def show_step3():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return render_template('wizard/step1.html')
    return render_template('wizard/step3.html')

@wizard_bp.route('/process-step3', methods=['POST'])
def process_step3():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    description = request.form.get('description', '')
    parsed_car = car_parser.parse(description)
    
    wizard_sessions[session_id].car_data = {
        'raw_description': description,
        'parsed_data': parsed_car,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'parsed_car': parsed_car, 'next_step': '/wizard/step4'})

@wizard_bp.route('/api/analyze-car', methods=['POST'])
def analyze_car_text():
    data = request.get_json()
    description = data.get('description', '')
    
    if len(description) < 10:
        return jsonify({'success': False, 'message': 'Description too short for analysis'})
    
    parsed_car = car_parser.parse(description)
    
    return jsonify({
        'success': True,
        'analysis': {
            'category': parsed_car['category'][0],
            'category_confidence': parsed_car['category'][1],
            'severity': parsed_car['severity'][0],
            'severity_reason': parsed_car['severity'][1],
            'location': parsed_car['location'],
            'when': parsed_car['when'],
            'affected_products': parsed_car['affected_products'],
            'immediate_risks': parsed_car['immediate_risks'],
            'suggested_actions': parsed_car['suggested_actions'],
            'related_standards': parsed_car['related_standards'],
            'confidence_score': parsed_car['confidence_score']
        }
    })

@wizard_bp.route('/step4', methods=['GET'])
def show_step4():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return render_template('wizard/step1.html')
    
    wizard_session = wizard_sessions[session_id]
    return render_template('wizard/step4.html',
                         business_info=wizard_session.business_info,
                         templates=wizard_session.selected_templates,
                         car_data=wizard_session.car_data)

@wizard_bp.route('/complete', methods=['POST'])
def complete_wizard():
    session_id = session.get('wizard_session_id')
    if not session_id or session_id not in wizard_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    wizard_sessions[session_id].completed = True
    wizard_sessions[session_id].completed_at = datetime.now()
    
    return jsonify({'success': True, 'message': 'Setup wizard completed successfully!', 'redirect': '/dashboard'})
