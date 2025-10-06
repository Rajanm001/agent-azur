@echo off
REM Automated deployment script for Windows
REM Author: Rajan Mishra

echo ======================================================================
echo   Azure Agentic AI - Automated Setup ^& Deployment
echo   Author: Rajan Mishra
echo ======================================================================

echo.
echo [1/6] Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    exit /b 1
)

echo.
echo [2/6] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo [3/6] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/6] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [5/6] Checking configuration...
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo Please edit .env file with your credentials
) else (
    echo .env file found
)

echo.
echo [6/6] Running validation...
python FINAL_VALIDATION.py

echo.
echo ======================================================================
echo   Setup Complete!
echo   Run: python src\main.py
echo   Metrics: http://localhost:8000
echo ======================================================================

pause
