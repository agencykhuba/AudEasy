# AudEasy Project

AudEasy is a mobile-first, AI-powered auditing platform with CAPA/CAR functionality, serving as the pilot project for Agency Khuba's SLM-centered workflow. It aims to transform Excel-based auditing into a scalable, automated solution.

## Setup
- Clone the repository: `git clone https://github.com/agencykhuba/AudEasy.git`
- Create virtual environment: `python -m venv .venv`
- Activate: `.venv\Scripts\activate.bat` (Windows) or `source .venv/Scripts/activate` (Git Bash)
- Install dependencies: `pip install -r requirements.txt`

## Structure
- `Code/`: Application code (e.g., Flask backend, frontend).
- `Documents/`: Project documentation (e.g., notes.txt, spec.json).
## Local Development Setup

### Running Locally (Windows)
```bash
# Install dependencies
pip install -r requirements.txt

# Start local development server
python run_local.py

# Access application at:
# http://127.0.0.1:5000
