#!/bin/bash
# Quick deployment script with compatible versions for Aliyun mirror

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "ECF MIS System - Quick Deploy"
echo "=========================================="

# Stop processes
echo "[1/8] Stopping processes..."
pkill -f "gunicorn" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true

# Remove old project
echo "[2/8] Removing old project..."
rm -rf "$PROJECT_DIR"

# Clone project
echo "[3/8] Cloning project..."
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd "$PROJECT_DIR"

# Create virtual environment
echo "[4/8] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "[5/8] Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies (using versions compatible with Aliyun mirror)
echo "[6/8] Installing dependencies..."
echo "Using Aliyun mirror for faster download..."

# Try with Aliyun mirror first
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com || {
    echo "Aliyun mirror failed, trying default PyPI..."
    pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0
}

# Verify Flask
python -c "import flask; print('✓ Flask', flask.__version__, 'installed')" || {
    echo "✗ Flask installation failed!"
    exit 1
}

# Setup project
echo "[7/8] Setting up project..."
mkdir -p logs instance
cp env.example .env

# Generate SECRET_KEY
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env

chmod -R 755 instance static templates

# Initialize database
echo "[8/8] Initializing database..."
python init_data.py

# Verify
python -c "from app import app; print('✓ Application OK')" || {
    echo "✗ Application verification failed!"
    exit 1
}

echo ""
echo "=========================================="
echo "✓ Deployment completed successfully!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo "  gunicorn --config gunicorn_config.py app:app"
echo "=========================================="

