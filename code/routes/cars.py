# code/routes/cars.py
"""CAR management routes"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from code.services.car_text_parser import CARTextParser
from datetime import datetime

cars_bp = Blueprint('cars', __name__, url_prefix='/cars')
car_parser = CARTextParser()

@cars_bp.route('/create', methods=['GET'])
def create_car_form():
    """Show CAR creation form"""
    return render_template('cars/create.html')

@cars_bp.route('/create', methods=['POST'])
def create_car():
    """Process CAR creation"""
    description = request.form.get('description', '')
    
    # Parse with AI
    parsed_car = car_parser.parse(description)
    
    # TODO: Save to database
    # car = Car(
    #     description=description,
    #     category=parsed_car['category'][0],
    #     severity=parsed_car['severity'][0],
    #     location=parsed_car['location'],
    #     status='open'
    # )
    # db.session.add(car)
    # db.session.commit()
    
    return redirect(url_for('dashboard'))

@cars_bp.route('/list', methods=['GET'])
def list_cars():
    """List all CARs"""
    # TODO: Fetch from database
    return render_template('cars/list.html', cars=[])
