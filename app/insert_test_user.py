from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app import Users, bcrypt
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:GaelRafa91072834@localhost:5433/audeasy')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def insert_test_user(session, email, password_hash):
    try:
        existing_user = session.query(Users).filter_by(email=email).first()
        if existing_user:
            print(f"User {email} already exists")
            return
        user = Users(
            id="1",  # Simplified; use uuid_generate_v4() in production
            email=email,
            password_hash=password_hash,
            name="Test User",
            role="auditor",
            status="active"
        )
        session.add(user)
        session.commit()
        print("Test user inserted")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
