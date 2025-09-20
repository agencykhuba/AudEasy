from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text

bcrypt = Bcrypt()
engine = create_engine('postgresql+psycopg2://postgres:gaelRafa%4091072834@localhost:5432/audeasy')

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT password_hash FROM users WHERE email = 'test@audeasy.com';")
    ).fetchone()
    stored_hash = result[0]
    print(f"Stored hash: {stored_hash}")
    try:
        is_valid = bcrypt.check_password_hash(stored_hash, 'pass123')
        print(f"Hash validation: {'Successful' if is_valid else 'Failed'}")
    except Exception as e:
        print(f"Hash validation error: {str(e)}")