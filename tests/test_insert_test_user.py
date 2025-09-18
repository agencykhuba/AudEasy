import pytest
from app.insert_test_user import insert_test_user, bcrypt
from app.models import Users

def test_insert_test_user(db_session):
    password_hash = bcrypt.generate_password_hash("test123").decode("utf-8")
    insert_test_user(db_session, "test@example.com", password_hash)
    user = db_session.query(Users).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.email == "test@example.com"
    assert bcrypt.check_password_hash(user.password_hash, "test123")
