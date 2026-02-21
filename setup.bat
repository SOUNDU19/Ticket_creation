@echo off
echo ==========================================
echo NexoraAI Support Suite - Setup Script
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found

REM Navigate to backend
cd backend

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Download spaCy model
echo.
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm

REM Create .env file if not exists
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created. Please update with your configuration.
)

REM Train ML model
echo.
echo ==========================================
echo Training ML Model
echo ==========================================
cd ml
python train.py
cd ..

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Update backend\.env with your configuration
echo 2. Start backend: cd backend ^&^& python app.py
echo 3. Start frontend: cd frontend ^&^& python -m http.server 8000
echo.
echo Default admin credentials:
echo Email: admin@nexora.ai
echo Password: admin123
echo.
echo WARNING: Change admin password after first login!
echo.
echo ==========================================
pause
