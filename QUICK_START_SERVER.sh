#!/bin/bash
# Quick start script for server

cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# Ensure logs directory exists
mkdir -p logs

# Start gunicorn in foreground (can see output)
echo "Starting Gunicorn on 127.0.0.1:6657..."
echo "Press Ctrl+C to stop"
echo ""
gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app

