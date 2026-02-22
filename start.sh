#!/bin/bash
cd backend

# Ensure database directory exists
mkdir -p /opt/render/project/src

# Seed database with sample data
python seed_data.py || echo "Database seeding skipped"

# Start gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --access-logfile - --error-logfile -
