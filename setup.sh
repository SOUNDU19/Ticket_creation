#!/bin/bash

echo "=========================================="
echo "NexoraAI Support Suite - Setup Script"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Navigate to backend
cd backend

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Create .env file if not exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please update with your configuration."
fi

# Train ML model
echo ""
echo "=========================================="
echo "Training ML Model"
echo "=========================================="
cd ml
python train.py
cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Start backend: cd backend && python app.py"
echo "3. Start frontend: cd frontend && python -m http.server 8000"
echo ""
echo "Default admin credentials:"
echo "Email: admin@nexora.ai"
echo "Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change admin password after first login!"
echo ""
echo "=========================================="
