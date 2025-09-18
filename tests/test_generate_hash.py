import pytest
from app.generate_hash import bcrypt

def test_generate_hash():
    hash_value = bcrypt.generate_password_hash("test_password").decode("utf-8")
    assert isinstance(hash_value, str)
    assert len(hash_value) > 0
    assert hash_value != "test_password"
