# MIS Management System - Elder Care Foundation

A comprehensive Management Information System (MIS) for managing financial, donation, inventory, and staff data for an elder care foundation.

## Features

### Financial Management
- Financial record management (income, expenses, donations)
- Financial trend analysis
- Expense categorization and statistics
- Financial report generation

### Donation Management
- Donation record management
- Donor information management
- Donor demographics analysis (age groups, regional distribution)
- Top donors ranking

### Inventory Management
- Inventory item management
- Demand planning management
- Supplier management
- Purchase order management

### Staff Management
- Staff information management
- Attendance records
- Schedule management
- Performance evaluation

### Data Visualization
- Financial trend charts
- Donation trend charts
- Expense category pie charts
- Donor demographics charts
- Top donors bar charts

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (configurable to other databases)
- **Frontend**: HTML5, CSS3, JavaScript
- **Chart Library**: Chart.js

## Installation and Running

### Method 1: One-Click Startup Script (Simplest, Recommended)

**Windows Users:**
```bash
# Double-click quick_start.bat or run in command line:
quick_start.bat
```

**Linux/Mac Users:**
```bash
# Add execute permission and run
chmod +x quick_start.sh
./quick_start.sh
```

The one-click startup script automatically performs the following operations:
- ✅ Check Python environment
- ✅ Create virtual environment (if not exists)
- ✅ Install/update all dependencies
- ✅ Create configuration file (from env.example)
- ✅ Initialize database
- ✅ Start application server

After startup, access at: `http://localhost:6657`

### Method 2: Step-by-Step Installation (For custom configuration)

**Windows Users:**
```bash
# First time setup, configure environment
setup_env.bat

# Start application
run.bat
```

**Linux/Mac Users:**
```bash
# First time setup, configure environment
chmod +x setup_env.sh
./setup_env.sh

# Start application
source venv/bin/activate
python app.py
```

### Method 3: Manual Configuration

#### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Copy `env.example` to `.env` file:
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

Then modify the configuration in `.env` file as needed.

#### 4. Run Application

```bash
python app.py
```

The application will start at `http://localhost:6657`.

### Access the System

Open `http://localhost:6657` in your browser to use the MIS system.

> **Note**: The database file will be automatically created on first run.

## Server Deployment

### Baota Panel Deployment (Recommended)

For detailed Baota panel deployment guide, please refer to:
- [Baota Panel Quick Start Guide](BAOTA_QUICK_START.md) - 5-minute quick deployment
- [Complete Deployment Documentation](DEPLOYMENT.md) - Detailed deployment steps and troubleshooting

### Quick Deployment Steps

1. **Clone project to server**
   ```bash
   cd /www/wwwroot
   git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
   cd ECF-MIS-system-opensource
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==0.20.0 Werkzeug==2.0.3 gunicorn==20.1.0
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env file, set HOST=0.0.0.0 for public access
   ```

4. **Initialize database**
   ```bash
   python init_data.py
   ```

5. **Start application**
   ```bash
   python app.py
   # Or use gunicorn (recommended for production)
   gunicorn --bind 0.0.0.0:6657 --workers 2 app:app
   ```

6. **Configure Nginx reverse proxy** (in Baota panel)
   - Website → Your Site → Settings → Reverse Proxy
   - Target URL: `http://127.0.0.1:6657`

7. **Configure firewall**
   - Open ports 80 (HTTP) and 443 (HTTPS)
   - If accessing application directly, open port 6657

## Project Structure

```
eldercare-fundation/
├── app.py                 # Flask application main file
├── models.py              # Database model definitions
├── requirements.txt       # Python dependencies
├── quick_start.bat        # Windows one-click startup script
├── quick_start.sh         # Linux/Mac one-click startup script
├── setup_env.bat          # Windows environment setup script
├── setup_env.sh           # Linux/Mac environment setup script
├── run.bat                # Windows run script
├── env.example            # Environment variable configuration example
├── routes/               # API routes
│   ├── __init__.py
│   ├── financial.py      # Financial management routes
│   ├── donation.py       # Donation management routes
│   ├── inventory.py      # Inventory management routes
│   ├── staff.py          # Staff management routes
│   ├── dashboard.py      # Dashboard routes
│   └── utils.py          # Utility functions
├── templates/            # HTML templates
│   └── index.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## API Endpoints

### Financial Management
- `GET /api/financial/records` - Get financial records
- `POST /api/financial/records` - Create financial record
- `GET /api/financial/summary` - Get financial summary
- `GET /api/financial/expenses` - Get expense records

### Donation Management
- `GET /api/donation/donations` - Get donation records
- `POST /api/donation/donations` - Create donation
- `GET /api/donation/donors` - Get donor list
- `POST /api/donation/donors` - Create donor
- `GET /api/donation/demographics` - Get donor demographics

### Inventory Management
- `GET /api/inventory/items` - Get inventory items
- `POST /api/inventory/items` - Create inventory item
- `GET /api/inventory/suppliers` - Get suppliers
- `GET /api/inventory/purchase-orders` - Get purchase orders

### Staff Management
- `GET /api/staff/staff` - Get staff list
- `POST /api/staff/staff` - Create staff member
- `GET /api/staff/attendance` - Get attendance records
- `GET /api/staff/schedules` - Get schedules

### Dashboard
- `GET /api/dashboard/overview` - Get dashboard overview
- `GET /api/dashboard/financial-trends` - Get financial trends
- `GET /api/dashboard/donation-trends` - Get donation trends
- `GET /api/dashboard/top-donors` - Get top donors

## Database Models

The system includes the following main data tables:

- **Financial Management**: FinancialRecord, Expense, PayrollRecord
- **Donation Management**: Donation, Donor, Gift
- **Inventory Management**: Inventory, DemandPlan, Supplier, PurchaseOrder
- **Staff Management**: Staff, Attendance, Schedule, PerformanceReview
- **User Management**: User, Role, Permission

All relationships between tables are defined in the ERD diagram and linked through foreign keys.

## Usage Instructions

1. **Dashboard**: View system overview and key statistics
2. **Financial Management**: Manage all financial records and expenses
3. **Donation Management**: Manage donation records and donor information, view demographics
4. **Inventory Management**: Manage inventory items, suppliers, and purchase orders
5. **Staff Management**: Manage staff information, attendance, and schedules

## Configuration File Description

### Environment Variables (.env)

Main configuration items:
- `HOST`: Server binding address (default: `0.0.0.0`, allows public access)
- `PORT`: Server port (default: `6657`)
- `SECRET_KEY`: Flask secret key (must be changed in production)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `FLASK_DEBUG`: Debug mode (set to `0` in production)

### Production Environment Configuration

- `gunicorn_config.py`: Gunicorn production server configuration
- `nginx.conf.example`: Nginx reverse proxy configuration example
- `ecf-mis.service`: Systemd service file (optional)

## Notes

- SQLite database will be automatically created on first run
- Other databases can be configured via `DATABASE_URL` environment variable
- **`SECRET_KEY` must be changed in production environment**
- Production environment should use Gunicorn instead of Flask development server
- It is recommended to configure Nginx reverse proxy and SSL certificate

## Development

The system uses a modular design, making it easy to extend and maintain. New functional modules can be easily added or existing features modified.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
