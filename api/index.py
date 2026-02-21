import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app

# Create Flask app for Vercel
app = create_app('production')

# Vercel serverless function handler
def handler(request, context):
    return app(request, context)
