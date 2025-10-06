#!/bin/bash

# Automated deployment script for Azure Agentic AI
# This script sets up the complete environment and runs validation

set -e  # Exit on error

echo "======================================================================"
echo "  Azure Agentic AI - Automated Setup & Deployment"
echo "  Author: Rajan Mishra"
echo "======================================================================"

# Check Python version
echo ""
echo "[1/6] Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "[2/6] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/6] Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo ""
echo "[4/6] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
echo ""
echo "[5/6] Checking configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "Please edit .env file with your credentials"
else
    echo ".env file found"
fi

# Run validation
echo ""
echo "[6/6] Running validation..."
python FINAL_VALIDATION.py

echo ""
echo "======================================================================"
echo "  Setup Complete!"
echo "  Run: python src/main.py"
echo "  Metrics: http://localhost:8000"
echo "======================================================================"
