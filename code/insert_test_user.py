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

session = Session()
try:
    existing_user = session.query(Users).filter_by(email='test@example.com').first()
    if existing_user:
        print("User test@example.com already exists")
    else:
        user = Users(
            email='test@example.com',
            password_hash=bcrypt.generate_password_hash('test123').decode('utf-8'),
            name='Test User',
            role='auditor',
            status='active'
        )
        session.add(user)
        session.commit()
        print("Test user inserted")
except Exception as e:
    print(f"Error: {e}")
finally:
    session.close()
