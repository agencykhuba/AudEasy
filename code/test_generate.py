from transformers import pipeline
import os

# Silence symlink warning
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Ensure Code directory exists
os.makedirs('Code', exist_ok=True)

# Initialize Phi-2 or fallback to distilgpt2
try:
    generator = pipeline('text-generation', model='microsoft/phi-2', trust_remote_code=True)
except Exception as e:
    print(f"Error loading Phi-2 model: {e}, falling back to distilgpt2")
    generator = pipeline('text-generation', model='distilgpt2')

# Prompt for unit tests
prompt = """
Generate pytest unit tests for Flask endpoints in app.py:
1. A login endpoint (/login, POST) using flask-bcrypt and PostgreSQL users table (columns: id UUID, email VARCHAR, password_hash VARCHAR, role ENUM('admin', 'area_manager', 'auditor')).
2. An audit submission endpoint (/audit, POST) using audit_visits table (columns: id UUID, store_id UUID, auditor_id UUID, template_id UUID, visit_datetime TIMESTAMPTZ, status ENUM('in_progress', 'completed')).
Test success and failure cases for both endpoints. Use pytest fixtures for the Flask test client. Include imports for pytest, app from app.py, and any necessary modules. Ensure tests are modular, use UUIDs for IDs, and cover error handling.
"""

# Generate tests with explicit truncation
try:
    generated_code = generator(prompt, max_new_tokens=800, truncation=True, num_return_sequences=1)[0]['generated_text']
    if len(generated_code) > 200:  # Confidence check
        with open('Code/tests.py', 'w') as f:
            f.write(generated_code)
        print("Generated tests written to Code/tests.py:\n", generated_code)
    else:
        print("SLM output too short, retry with adjusted prompt.")
except Exception as e:
    print(f"Error generating tests: {e}")