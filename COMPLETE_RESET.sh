#!/bin/bash
# Complete reset and deploy script - from stopping processes to starting application

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "ECF MIS System - Complete Reset and Deploy"
echo "=========================================="
echo ""

# ========== Step 1: Stop all processes ==========
echo "[1/10] Stopping all processes..."
pkill -f "gunicorn.*app:app" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "gunicorn" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true
sleep 3

# Verify processes are stopped
if pgrep -f "gunicorn" > /dev/null; then
    echo "Warning: Some gunicorn processes still running, force killing..."
    pkill -9 -f "gunicorn" 2>/dev/null || true
    sleep 2
fi

echo "✓ All processes stopped"
echo ""

# ========== Step 2: Remove old project ==========
echo "[2/10] Removing old project files..."
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
    echo "✓ Old project removed"
else
    echo "✓ No old project found"
fi
echo ""

# ========== Step 3: Clone project ==========
echo "[3/10] Cloning project from GitHub..."
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd "$PROJECT_DIR"
echo "✓ Project cloned"
echo ""

# ========== Step 4: Create virtual environment ==========
echo "[4/10] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "✓ Virtual environment created"
echo ""

# ========== Step 5: Upgrade pip ==========
echo "[5/10] Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ Pip upgraded"
echo ""

# ========== Step 6: Install dependencies ==========
echo "[6/10] Installing dependencies (using Aliyun mirror)..."
echo "This may take a few minutes..."

# Install with Aliyun mirror
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

# ========== Step 7: Setup project ==========
echo "[7/10] Setting up project..."
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

# ========== Step 8: Initialize database ==========
echo "[8/10] Initializing database..."
python init_data.py
echo "✓ Database initialized"
echo ""

# ========== Step 9: Verify application ==========
echo "[9/10] Verifying application..."
python -c "from app import app; print('✓ Application can be imported')" || {
    echo "✗ Application import failed!"
    exit 1
}
echo "✓ Application verified"
echo ""

# ========== Step 10: Start application ==========
echo "[10/10] Starting application..."
echo ""

# Check if port is in use
if netstat -tlnp 2>/dev/null | grep -q ":6657 "; then
    echo "Warning: Port 6657 is already in use!"
    PID=$(netstat -tlnp 2>/dev/null | grep ":6657 " | awk '{print $7}' | cut -d'/' -f1)
    if [ ! -z "$PID" ]; then
        echo "Killing process on port 6657..."
        kill -9 $PID 2>/dev/null || true
        sleep 2
    fi
fi

# Start gunicorn in background
nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &

sleep 3

# Verify it started
if ps aux | grep -q "[g]unicorn.*app:app"; then
    echo "✓ Application started successfully!"
    echo ""
    echo "Process info:"
    ps aux | grep "[g]unicorn.*app:app" | head -1
    echo ""
    echo "Port status:"
    netstat -tlnp | grep 6657 || ss -tlnp | grep 6657
    echo ""
else
    echo "✗ Failed to start application!"
    echo "Check logs:"
    echo "  tail -f $PROJECT_DIR/logs/gunicorn.log"
    echo "  tail -f $PROJECT_DIR/logs/error.log"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Application is running on: http://127.0.0.1:6657"
echo ""
echo "Next steps:"
echo "1. Configure Nginx reverse proxy in Baota Panel:"
echo "   - Website → Your site → Settings → Reverse Proxy"
echo "   - Target URL: http://127.0.0.1:6657"
echo ""
echo "2. Access the application:"
echo "   - Public IP: http://47.242.126.44"
echo "   - Or your domain (if configured)"
echo ""
echo "3. View logs:"
echo "   tail -f $PROJECT_DIR/logs/error.log"
echo "   tail -f $PROJECT_DIR/logs/access.log"
echo "   tail -f $PROJECT_DIR/logs/gunicorn.log"
echo ""
echo "4. Stop application:"
echo "   pkill -f 'gunicorn.*app:app'"
echo ""
echo "=========================================="

