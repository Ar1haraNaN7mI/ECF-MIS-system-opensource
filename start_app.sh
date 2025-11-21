#!/bin/bash
# Script to start ECF MIS application with proper error handling

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "Starting ECF MIS Application"
echo "=========================================="

# Check if in project directory
if [ ! -f "$PROJECT_DIR/app.py" ]; then
    echo "Error: app.py not found in $PROJECT_DIR"
    echo "Please run this script from the project directory or set PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run deployment script first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create logs directory if it doesn't exist
mkdir -p logs

# Test if app can be imported
echo "Testing application import..."
python -c "from app import app; print('✓ Application can be imported')" || {
    echo "✗ Failed to import application!"
    echo "Please check:"
    echo "  1. All dependencies are installed: pip install -r requirements.txt"
    echo "  2. Database is initialized: python init_data.py"
    exit 1
}

# Check if port is already in use
if netstat -tlnp 2>/dev/null | grep -q ":6657 "; then
    echo "Warning: Port 6657 is already in use!"
    echo "Checking what's using it..."
    netstat -tlnp | grep ":6657 "
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PID=$(netstat -tlnp | grep ":6657 " | awk '{print $7}' | cut -d'/' -f1)
        kill -9 $PID 2>/dev/null || true
        sleep 2
    else
        echo "Please stop the existing process first."
        exit 1
    fi
fi

# Start gunicorn
echo ""
echo "Starting Gunicorn..."
echo "=========================================="

# Option 1: Foreground mode (see output directly)
if [ "$1" == "--foreground" ] || [ "$1" == "-f" ]; then
    echo "Starting in foreground mode (Ctrl+C to stop)..."
    gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
else
    # Option 2: Background mode with nohup
    echo "Starting in background mode..."
    nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &
    
    sleep 2
    
    # Check if started successfully
    if ps aux | grep -q "[g]unicorn.*app:app"; then
        echo "✓ Gunicorn started successfully!"
        echo ""
        echo "Process info:"
        ps aux | grep "[g]unicorn.*app:app" | head -1
        echo ""
        echo "To view logs:"
        echo "  tail -f $PROJECT_DIR/logs/error.log"
        echo "  tail -f $PROJECT_DIR/logs/access.log"
        echo "  tail -f $PROJECT_DIR/logs/gunicorn.log"
        echo ""
        echo "To stop:"
        echo "  pkill -f 'gunicorn.*app:app'"
        echo ""
        echo "To test:"
        echo "  curl http://127.0.0.1:6657"
    else
        echo "✗ Failed to start Gunicorn!"
        echo "Check logs:"
        echo "  tail -f $PROJECT_DIR/logs/gunicorn.log"
        echo "  tail -f $PROJECT_DIR/logs/error.log"
        exit 1
    fi
fi

