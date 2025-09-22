from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WizardSession(Base):
    __tablename__ = 'wizard_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    step_number = Column(Integer, default=1)
    business_info = Column(JSON)
    templates_selected = Column(JSON)
    team_setup = Column(JSON)
    compliance_config = Column(JSON)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IndustryTemplate(Base):
    __tablename__ = 'industry_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    industry = Column(String(100))
    category = Column(String(100))
    description = Column(String(500))
    template_data = Column(JSON)
    keywords = Column(JSON)
    regulatory_requirements = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
