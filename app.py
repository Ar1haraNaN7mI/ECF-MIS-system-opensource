from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from models import db
from routes import financial_bp, donation_bp, inventory_bp, staff_bp, dashboard_bp
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Ensure instance directory exists
instance_path = Path('instance')
instance_path.mkdir(exist_ok=True)

# Configure database URI
database_url = os.getenv('DATABASE_URL', 'sqlite:///instance/mis_database.db')
# Convert relative path to absolute path for SQLite
if database_url.startswith('sqlite:///'):
    db_path = database_url.replace('sqlite:///', '')
    if not os.path.isabs(db_path):
        # Make it absolute path
        db_path = os.path.abspath(db_path)
        database_url = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

CORS(app)
db.init_app(app)

# Register blueprints
app.register_blueprint(financial_bp, url_prefix='/api/financial')
app.register_blueprint(donation_bp, url_prefix='/api/donation')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(staff_bp, url_prefix='/api/staff')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', 6657))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Starting server on {host}:{port}")
    print(f"Access the application at http://{host}:{port}")
    app.run(debug=debug, host=host, port=port, threaded=True)

