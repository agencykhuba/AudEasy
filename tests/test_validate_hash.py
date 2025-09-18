import pytest
from app.validate_hash import bcrypt
from app.generate_hash import bcrypt as generate_bcrypt

def test_validate_hash():
    password = "test_password"
    hash_value = generate_bcrypt.generate_password_hash(password).decode("utf-8")
    assert bcrypt.check_password_hash(hash_value, password) is True
    assert bcrypt.check_password_hash(hash_value, "wrong_password") is False
