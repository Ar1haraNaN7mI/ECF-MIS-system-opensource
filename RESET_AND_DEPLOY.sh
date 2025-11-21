#!/bin/bash
# Complete reset and deploy script for ECF MIS System
# This script will completely reset and deploy from scratch

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "ECF MIS System - Complete Reset and Deploy"
echo "=========================================="
echo ""

# Step 1: Stop all processes
echo "[1/8] Stopping all processes..."
pkill -f "gunicorn.*app:app" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true
sleep 2
echo "✓ Processes stopped"
echo ""

# Step 2: Remove old project
echo "[2/8] Removing old project..."
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
    echo "✓ Old project removed"
else
    echo "✓ No old project found"
fi
echo ""

# Step 3: Clone project
echo "[3/8] Cloning project from GitHub..."
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd "$PROJECT_DIR"
echo "✓ Project cloned"
echo ""

# Step 4: Create virtual environment
echo "[4/8] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "✓ Virtual environment created"
echo ""

# Step 5: Upgrade pip
echo "[5/8] Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ Pip upgraded"
echo ""

# Step 6: Install dependencies
echo "[6/8] Installing dependencies (using Aliyun mirror)..."
echo "This may take a few minutes..."

# Try Aliyun mirror first
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com || {
    echo "Aliyun mirror failed, trying default PyPI..."
    pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0
}

# Verify Flask installation
python -c "import flask; print('✓ Flask', flask.__version__, 'installed')" || {
    echo "✗ Flask installation verification failed!"
    echo "Trying to install without version constraints..."
    pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn
}

echo "✓ Dependencies installed"
echo ""

# Step 7: Setup project
echo "[7/8] Setting up project..."
mkdir -p logs instance
cp env.example .env

# Generate SECRET_KEY
if python -c "import secrets" 2>/dev/null; then
    SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
else
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || date +%s | sha256sum | base64 | head -c 64)
fi
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env

chmod -R 755 instance static templates
echo "✓ Project setup complete"
echo ""

# Step 8: Initialize database
echo "[8/8] Initializing database..."
python init_data.py
echo "✓ Database initialized"
echo ""

# Final verification
echo "Verifying installation..."
python -c "from app import app; print('✓ Application can be imported')" || {
    echo "✗ Application import failed!"
    exit 1
}

echo ""
echo "=========================================="
echo "✓ Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Project directory: $PROJECT_DIR"
echo ""
echo "To start the application:"
echo ""
echo "Method 1 - Using Gunicorn (Recommended):"
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo "  gunicorn --config gunicorn_config.py app:app"
echo ""
echo "Method 2 - Using Baota Python Project Manager:"
echo "  1. Open Baota Panel"
echo "  2. Python Project Manager → Add Project"
echo "  3. Fill in:"
echo "     - Project path: $PROJECT_DIR"
echo "     - Framework: Flask"
echo "     - Port: 6657"
echo "     - Execution file: app:app"
echo "  4. Click Start"
echo ""
echo "Method 3 - Direct run (for testing):"
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Configure Nginx reverse proxy in Baota Panel:"
echo "  Website → Your site → Settings → Reverse Proxy"
echo "  Add reverse proxy to: http://127.0.0.1:6657"
echo ""
echo "=========================================="

