from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bcrypt = Bcrypt(app)
db_url = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:GaelRafa91072834@localhost:5433/audeasy')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
try:
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    raise

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    role = Column(ENUM('admin', 'area_manager', 'auditor', name='user_role'), nullable=False)
    status = Column(ENUM('active', 'inactive', name='user_status'), nullable=False)

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
        data = request.get_json()
        logger.debug(f"Received login request: {data}")
        session = Session()
        user = session.query(Users).filter_by(email=data['email']).first()
        logger.debug(f"Queried user: {user.email if user else None}")
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            logger.debug("Password check passed")
            return jsonify({'status': 'success', 'user_id': str(user.id), 'role': user.role}), 200
        logger.debug("Invalid credentials")
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

@app.route('/audit', methods=['POST'])
def submit_audit():
    try:
        data = request.get_json()
        logger.debug(f"Received audit request: {data}")
        session = Session()
        visit = AuditVisits(
            store_id=uuid.UUID(data['store_id']),
            auditor_id=uuid.UUID(data['auditor_id']),
            template_id=uuid.UUID(data['template_id']),
            visit_datetime=datetime.fromisoformat(data['visit_datetime']),
            status='in_progress'
        )
        session.add(visit)
        session.commit()
        logger.debug(f"Audit visit created: {visit.id}")
        return jsonify({'status': 'success', 'visit_id': str(visit.id)}), 200
    except Exception as e:
        logger.error(f"Audit error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
