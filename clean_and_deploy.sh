#!/bin/bash
# Quick clean and deploy script
# This script removes everything and redeploys from scratch

set -e

PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"

echo "=========================================="
echo "Cleaning and Redeploying ECF MIS System"
echo "=========================================="

# Stop any running services
echo "[1/6] Stopping existing services..."
systemctl stop ecf-mis 2>/dev/null || true
pkill -f "gunicorn.*app:app" 2>/dev/null || true
echo "Services stopped."

# Remove old project
echo "[2/6] Removing old project..."
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
    echo "Old project removed."
else
    echo "No existing project found."
fi

# Run deployment script
echo "[3/6] Running deployment script..."
cd /www/wwwroot
bash <(curl -s https://raw.githubusercontent.com/Ar1haraNaN7mI/ECF-MIS-system-opensource/main/deploy_server.sh) || {
    echo "Downloading deployment script failed, using local version..."
    if [ -f deploy_server.sh ]; then
        bash deploy_server.sh
    else
        echo "Please run deploy_server.sh manually"
        exit 1
    fi
}

echo ""
echo "=========================================="
echo "Deployment completed!"
echo "=========================================="

