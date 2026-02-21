import sys
import os
from pathlib import Path

# Get the backend directory path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(str(backend_dir))

# Import and create the Flask app
from app import create_app

app = create_app('production')

# Export for Vercel
def handler(event, context):
    """Vercel serverless handler"""
    return app
