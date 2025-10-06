@echo off
call .venv\Scripts\activate.bat
set PYTHONPATH=%cd%
echo ========================================
echo Starting Azure Diagnostic AI Agent...
echo ========================================
echo.
python src\main.py
pause
