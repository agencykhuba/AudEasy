from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
engine = create_engine('postgresql+psycopg2://user:pass@localhost/audeasy')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(ENUM('admin', 'area_manager', 'auditor', name='user_role'), nullable=False)

class AuditVisits(Base):
    __tablename__ = 'audit_visits'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), nullable=False)
    auditor_id = Column(UUID(as_uuid=True), nullable=False)
    template_id = Column(UUID(as_uuid=True), nullable=False)
    visit_datetime = Column(DateTime, nullable=False)
    status = Column(ENUM('in_progress', 'completed', name='visit_status'), nullable=False, default='in_progress')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        session = Session()
        user = session.query(Users).filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            return jsonify({'status': 'success', 'user_id': str(user.id), 'role': user.role}), 200
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

@app.route('/audit', methods=['POST'])
def submit_audit():
    try:
        data = request.json
        session = Session()
        visit = AuditVisits(
            store_id=data['store_id'],
            auditor_id=data['auditor_id'],
            template_id=data['template_id'],
            visit_datetime=datetime.fromisoformat(data['visit_datetime']),
            status='in_progress'
        )
        session.add(visit)
        session.commit()
        return jsonify({'status': 'success', 'visit_id': str(visit.id)}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)