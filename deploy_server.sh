#!/bin/bash
# Complete deployment script for ECF MIS System on Baota Panel Server
# This script will clean and redeploy the entire project

set -e

echo "=========================================="
echo "ECF MIS System - Complete Deployment"
echo "=========================================="

# Configuration
PROJECT_DIR="/www/wwwroot/ECF-MIS-system-opensource"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_info "Found: $PYTHON_VERSION"
else
    print_error "Python3 not found! Please install Python 3.8+ first."
    exit 1
fi

# Navigate to wwwroot directory
print_info "Navigating to /www/wwwroot..."
cd /www/wwwroot || exit 1

# Remove existing project if it exists
if [ -d "$PROJECT_DIR" ]; then
    print_warn "Existing project found. Removing it..."
    rm -rf "$PROJECT_DIR"
    print_info "Old project removed."
fi

# Clone project from GitHub
print_info "Cloning project from GitHub..."
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
print_info "Project cloned successfully."

# Navigate to project directory
cd "$PROJECT_DIR" || exit 1

# Create virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
print_info "Virtual environment created."

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Configure pip to use faster mirror (optional, for China)
print_info "Configuring pip mirror (for faster download)..."
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple 2>/dev/null || true
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn 2>/dev/null || true

# Install dependencies with retry
print_info "Installing project dependencies..."
MAX_RETRIES=3
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if pip install -r requirements.txt; then
        print_info "Dependencies installed successfully."
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            print_warn "Installation failed, retrying ($RETRY_COUNT/$MAX_RETRIES)..."
            sleep 2
        else
            print_error "Failed to install dependencies after $MAX_RETRIES attempts."
            print_info "Trying with default PyPI source..."
            pip config unset global.index-url 2>/dev/null || true
            pip install -r requirements.txt || {
                print_error "Failed to install dependencies. Please check your network connection."
                exit 1
            }
        fi
    fi
done

# Verify Flask installation
print_info "Verifying Flask installation..."
if python -c "import flask; print('Flask version:', flask.__version__)" 2>/dev/null; then
    print_info "Flask installed successfully."
else
    print_error "Flask installation verification failed!"
    print_info "Trying to install Flask manually..."
    pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn || {
        print_error "Manual Flask installation failed!"
        exit 1
    }
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p "$LOG_DIR"
mkdir -p "$PROJECT_DIR/instance"
print_info "Directories created."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_info "Creating .env file from env.example..."
    cp env.example .env
    
    # Generate a random secret key
    if python3 -c "import secrets" 2>/dev/null; then
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    else
        # Fallback if secrets module not available
        SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || date +%s | sha256sum | base64 | head -c 64)
    fi
    
    # Update SECRET_KEY in .env file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi
    
    print_info ".env file created with generated SECRET_KEY."
    print_warn "Please review and update .env file if needed."
else
    print_info ".env file already exists, skipping creation."
fi

# Set proper permissions
print_info "Setting file permissions..."
chmod -R 755 instance
chmod -R 755 static
chmod -R 755 templates
chmod +x deploy.sh 2>/dev/null || true
print_info "Permissions set."

# Initialize database
print_info "Initializing database..."
python init_data.py
print_info "Database initialized successfully."

# Test if the application can be imported
print_info "Testing application import..."
python -c "from app import app; print('Application imported successfully!')"
print_info "Application test passed."

echo ""
echo "=========================================="
print_info "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review .env file: nano $PROJECT_DIR/.env"
echo "2. Start the application using one of these methods:"
echo ""
echo "   Method 1 - Using Gunicorn (Recommended for production):"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   gunicorn --config gunicorn_config.py app:app"
echo ""
echo "   Method 2 - Using Python directly (for testing):"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "   Method 3 - Using Baota Python Project Manager:"
echo "   - Open Baota Panel"
echo "   - Go to Python Project Manager"
echo "   - Add new project:"
echo "     * Project path: $PROJECT_DIR"
echo "     * Framework: Flask"
echo "     * Port: 6657"
echo "     * Execution file: app:app"
echo ""
echo "3. Configure Nginx reverse proxy in Baota Panel:"
echo "   - Target URL: http://127.0.0.1:6657"
echo ""
echo "=========================================="

