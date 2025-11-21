#!/bin/bash
# Complete clean and deploy script for ECF MIS System
# This script will completely remove old installation and deploy fresh

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "ECF MIS System - Clean and Deploy"
echo "=========================================="

# Step 1: Stop all running processes
echo "[1/7] Stopping all running processes..."
pkill -f "gunicorn.*app:app" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true
sleep 2
echo "✓ Processes stopped"

# Step 2: Remove old project
echo "[2/7] Removing old project..."
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
    echo "✓ Old project removed"
else
    echo "✓ No old project found"
fi

# Step 3: Clone fresh project
echo "[3/7] Cloning project from GitHub..."
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd "$PROJECT_DIR"
echo "✓ Project cloned"

# Step 4: Create virtual environment
echo "[4/7] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "✓ Virtual environment created"

# Step 5: Upgrade pip and configure
echo "[5/7] Configuring pip and installing dependencies..."
pip install --upgrade pip --quiet

# Use faster mirror for China
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple 2>/dev/null || true
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn 2>/dev/null || true

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt || {
    echo "Warning: Installation with mirror failed, trying default source..."
    pip config unset global.index-url 2>/dev/null || true
    pip install -r requirements.txt
}
echo "✓ Dependencies installed"

# Verify Flask
python -c "import flask; print('Flask', flask.__version__, 'installed')" || {
    echo "Installing Flask manually..."
    pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn
}
echo "✓ Flask verified"

# Step 6: Setup project
echo "[6/7] Setting up project..."
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

# Step 7: Initialize database
echo "[7/7] Initializing database..."
python init_data.py
echo "✓ Database initialized"

# Final verification
echo ""
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
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo "  gunicorn --config gunicorn_config.py app:app"
echo ""
echo "Or use Baota Python Project Manager:"
echo "  - Path: $PROJECT_DIR"
echo "  - Port: 6657"
echo "  - Execution: app:app"
echo "=========================================="

