from transformers import pipeline
import os

# Silence symlink warning
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Ensure Code directory exists
os.makedirs('Code', exist_ok=True)

# Initialize Phi-2 for code generation (fallback to distilgpt2 if needed)
try:
    generator = pipeline('text-generation', model='microsoft/phi-2', trust_remote_code=True)
except Exception as e:
    print(f"Error loading Phi-2 model: {e}, falling back to distilgpt2")
    generator = pipeline('text-generation', model='distilgpt2')

# Refined prompt for schema-specific Flask routes
prompt = """
Generate Flask routes for:
1. A login endpoint using flask-bcrypt and PostgreSQL users table (columns: id UUID PRIMARY KEY, email VARCHAR UNIQUE, password_hash VARCHAR, role ENUM('admin', 'area_manager', 'auditor')).
2. An audit submission endpoint using audit_visits table (columns: id UUID PRIMARY KEY, store_id UUID, auditor_id UUID, template_id UUID, visit_datetime TIMESTAMPTZ, status ENUM('in_progress', 'completed')).
Use SQLAlchemy for database access (not Flask-SQLAlchemy), UUID for IDs, and return JSON responses with error handling. Include imports for flask, flask_bcrypt, sqlalchemy, sqlalchemy.orm, uuid, and datetime. Define database models for Users and AuditVisits with correct column types (String for UUID, Enum for role/status). Ensure modular imports for scalability.
"""

# Generate code with explicit truncation
try:
    generated_code = generator(prompt, max_new_tokens=800, truncation=True, num_return_sequences=1)[0]['generated_text']
    if len(generated_code) > 200:  # Confidence check
        with open('Code/app.py', 'w') as f:
            f.write(generated_code)
        print("Generated code written to Code/app.py:\n", generated_code)
    else:
        print("SLM output too short, retry with adjusted prompt.")
except Exception as e:
    print(f"Error generating code: {e}")