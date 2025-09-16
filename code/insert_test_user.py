from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
import uuid

bcrypt = Bcrypt()
engine = create_engine('postgresql+psycopg2://postgres:gaelRafa%4091072834@localhost:5432/audeasy')

# Generate valid hash
password_hash = bcrypt.generate_password_hash('pass123').decode('utf-8')
print(f"Generated hash: {password_hash}")

# Test bcrypt
try:
    is_valid = bcrypt.check_password_hash(password_hash, 'pass123')
    print(f"Bcrypt validation test: {'Successful' if is_valid else 'Failed'}")
except Exception as e:
    print(f"Bcrypt validation error: {str(e)}")

# Insert test user
with engine.connect() as conn:
    conn.execute(
        text("DELETE FROM users WHERE email = 'test@audeasy.com';")
    )
    conn.execute(
        text("""
        INSERT INTO users (id, email, password_hash, name, role, status)
        VALUES (:id, :email, :password_hash, :name, :role, :status);
        """),
        {
            'id': str(uuid.uuid4()),
            'email': 'test@audeasy.com',
            'password_hash': password_hash,
            'name': 'Test User',
            'role': 'auditor',
            'status': 'active'
        }
    )
    conn.commit()
    print("Test user inserted")

    # Validate hash
    result = conn.execute(
        text("SELECT password_hash FROM users WHERE email = 'test@audeasy.com';")
    ).fetchone()
    stored_hash = result[0]
    print(f"Stored hash: {stored_hash}")
    if stored_hash == password_hash:
        print("Hash validation successful")
    else:
        print("Hash validation failed")