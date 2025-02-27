# Business Intelligence System

Automated system for collecting, analyzing, and acting on business data from multiple sources.

## Features
- Email monitoring and parsing
- Google Sheets integration for centralized data storage
- Analytics processing
- LLM-powered decision making
- Interactive dashboard

## Setup
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: 
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up API credentials (see below)
6. Run the main script: `python src/main.py`

## API Setup
1. Create a Google Cloud project
2. Enable Google APIs (Gmail, Sheets, Drive, Analytics)
3. Create a service account with appropriate permissions
4. Download the service account key to `credentials/service-account.json`
5. Copy `.env.example` to `.env` and fill in your API keys

## Project Structure
- `src/`: Source code
- `tests/`: Test cases
- `notebooks/`: Jupyter notebooks for experimentation
- `credentials/`: API credentials (not included in git)
