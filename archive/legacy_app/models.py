from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    role = Column(String)
    status = Column(String)
