@echo off
echo ========================================
echo Azure Diagnostic AI Agent - Setup
echo ========================================
echo.
echo [1/4] Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo      Done!
echo.

echo [2/4] Activating environment...
call .venv\Scripts\activate.bat
echo      Done!
echo.

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo      Done!
echo.

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo      Done!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Login to Azure: az login
echo 2. Run agent: run_app.bat
echo.
pause
