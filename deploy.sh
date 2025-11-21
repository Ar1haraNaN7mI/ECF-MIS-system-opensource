#!/bin/bash
# ECF MIS System Deployment Script for Baota Panel

set -e

echo "=========================================="
echo "ECF MIS System Deployment Script"
echo "=========================================="

# Configuration
PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "Please do not run as root"
   exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR" || exit 1

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Gunicorn if not installed
if ! pip show gunicorn > /dev/null 2>&1; then
    echo "Installing Gunicorn..."
    pip install gunicorn
fi

# Create logs directory
echo "Creating logs directory..."
mkdir -p "$LOG_DIR"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from env.example..."
    cp env.example .env
    echo "Please edit .env file and set SECRET_KEY and other configurations!"
fi

# Initialize database
echo "Initializing database..."
python init_data.py

# Set permissions
echo "Setting permissions..."
chmod -R 755 instance
chmod -R 755 static
chmod -R 755 templates

# Create systemd service if it doesn't exist
if [ ! -f /etc/systemd/system/ecf-mis.service ]; then
    echo "Creating systemd service..."
    sudo cp ecf-mis.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable ecf-mis
    echo "Service created. You can start it with: sudo systemctl start ecf-mis"
else
    echo "Systemd service already exists."
fi

echo "=========================================="
echo "Deployment completed!"
echo "=========================================="
echo "Next steps:"
echo "1. Edit .env file and set SECRET_KEY"
echo "2. Start the service: sudo systemctl start ecf-mis"
echo "3. Check status: sudo systemctl status ecf-mis"
echo "4. Configure Nginx reverse proxy in Baota Panel"
echo "=========================================="

