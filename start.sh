#!/bin/bash
cd backend

# Ensure database directory exists
mkdir -p /opt/render/project/src

# Initialize database if it doesn't exist
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')" || echo "Database initialization skipped"

# Start gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --access-logfile - --error-logfile -
