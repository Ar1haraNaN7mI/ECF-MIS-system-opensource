#!/bin/bash

echo "===================================="
echo "MIS System Environment Setup"
echo "===================================="
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "Virtual environment created successfully!"
echo ""

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "Virtual environment activated!"
echo ""

echo "[3/4] Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""
echo "===================================="
echo "Environment setup completed!"
echo "===================================="
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the application, run:"
echo "  python app.py"
echo ""



