# Routes package
from .financial import financial_bp
from .donation import donation_bp
from .inventory import inventory_bp
from .staff import staff_bp
from .dashboard import dashboard_bp

__all__ = ['financial_bp', 'donation_bp', 'inventory_bp', 'staff_bp', 'dashboard_bp']

