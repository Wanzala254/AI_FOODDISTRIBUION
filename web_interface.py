import sys
import os
import site
import subprocess
import json
import logging
from flask import abort
from jinja2.exceptions import TemplateNotFound
import socket

def install_flask():
    print("Attempting to install Flask...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask installed successfully")
        return True
    except Exception as e:
        print(f"Error installing Flask: {e}")
        return False

def install_waitress():
    print("Attempting to install Waitress...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "waitress"])
        print("Waitress installed successfully")
        return True
    except Exception as e:
        print(f"Error installing Waitress: {e}")
        return False

def install_flask_limiter():
    print("Attempting to install Flask-Limiter...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-limiter"])
        print("Flask-Limiter installed successfully")
        return True
    except Exception as e:
        print(f"Error installing Flask-Limiter: {e}")
        return False

try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
    print("Flask imported successfully")
except ImportError:
    if install_flask():
        from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
    else:
        print("Could not import or install Flask. Please install it manually using:")
        print("python -m pip install flask")
        sys.exit(1)

try:
    from waitress import serve
    print("Waitress imported successfully")
except ImportError:
    if install_waitress():
        from waitress import serve
    else:
        print("Could not import or install Waitress. Please install it manually using:")
        print("python -m pip install waitress")
        sys.exit(1)

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    print("Flask-Limiter imported successfully")
except ImportError:
    if install_flask_limiter():
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
    else:
        print("Could not import or install Flask-Limiter. Please install it manually using:")
        print("python -m pip install flask-limiter")
        sys.exit(1)

from datetime import datetime
import json
from food_distribution_system import FoodDistributionSystem
from demand_prediction import DemandPredictor
from route_optimization import RouteOptimizer
from inventory_management import InventoryManager
from resource_allocation import ResourceAllocator
from alert_system import AlertSystem
from data_visualization import DataVisualizer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Initialize system components
fds = FoodDistributionSystem()
demand_predictor = DemandPredictor()
route_optimizer = RouteOptimizer()
inventory_manager = InventoryManager()
alert_system = AlertSystem()

# Store feedback and delivery confirmations
feedback_db = {}
delivery_confirmations = {}

# Initialize some sample data
def initialize_sample_data():
    # Add distribution centers
    fds.add_distribution_center('dc1', (0, 0), 5000)
    fds.add_distribution_center('dc2', (10, 10), 3000)
    
    # Add vulnerable areas
    vulnerable_areas = {
        'area1': {'vulnerability_score': 8.5, 'population': 1000, 'location': (2, 3)},
        'area2': {'vulnerability_score': 6.2, 'population': 1500, 'location': (5, 4)},
        'area3': {'vulnerability_score': 9.1, 'population': 800, 'location': (3, 7)}
    }
    
    for area_id, data in vulnerable_areas.items():
        fds.add_vulnerable_area(
            area_id, 
            data['location'], 
            data['population'], 
            data['vulnerability_score']
        )
    
    # Add initial inventory
    initial_inventory = {
        'rice': 1000,
        'beans': 800,
        'oil': 500,
        'flour': 600,
        'sugar': 400
    }
    
    for item, quantity in initial_inventory.items():
        inventory_manager.update_inventory(item, quantity)

# Add these imports at the top
from datetime import datetime
import json

# Add this to your existing global variables
distribution_updates = []

# Add Turkana-specific constants
TURKANA_LOCATION = (3.1166, 35.5966)
NAIROBI_LOCATION = (-1.2921, 36.8219)

# Add this new function for automatic delivery recording
def record_automatic_delivery(area_id: str, location: tuple):
    """Record delivery automatically when convoy reaches destination"""
    # Calculate estimated quantity based on area's population and vulnerability
    area_data = fds.vulnerable_areas.get(area_id)
    if area_data:
        base_quantity = area_data['population'] * 0.5  # 0.5 kg per person
        vulnerability_factor = area_data['vulnerability_score'] / 10
        adjusted_quantity = base_quantity * (1 + vulnerability_factor)

        # Record the delivery
        delivery_confirmation = {
            'area_id': area_id,
            'received_quantity': adjusted_quantity,
            'condition': 'good',
            'timestamp': datetime.now().isoformat(),
            'automatic_record': True
        }
        
        delivery_confirmations[len(delivery_confirmations)] = delivery_confirmation
        
        # Record in the food distribution system
        fds.record_delivery(area_id, adjusted_quantity, datetime.now())
        
        # Add Swahili notification
        swahili_message = (
            f"Habari! Msafara umefika {area_id}. "
            f"Chakula kiasi cha kilo {adjusted_quantity:.0f} kimewasili. "
            "Tafadhali kuja kuchukua mgao wako katika kituo cha usambazaji. "
            "Vitambulisho vinahitajika."
        )
        
        distribution_updates.append({
            'timestamp': datetime.now().isoformat(),
            'location': area_id,
            'status': 'arrived',
            'message': swahili_message,
            'message_type': 'delivery_notification'
        })
        
        # Generate alert
        alert_system.generate_alert(swahili_message, "delivery")
        
        return True
    return False

# Add this after your other routes
FORMULAS_FILE = 'data/formulas.json'

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def load_formulas():
    if os.path.exists(FORMULAS_FILE):
        with open(FORMULAS_FILE, 'r') as f:
            return json.load(f)
    return {
        'demand_formula': 'Base Demand × (Population ÷ 1000) × (1 + Vulnerability Score ÷ 10)',
        'allocation_formula': 'Required Quantity × (1 + Vulnerability Score ÷ 10)',
        'distribution_formula': '(Delivery Success × 0.4) + (Coverage Rate × 0.2) + (Response Time × 0.2)'
    }

def save_formulas(formulas):
    with open(FORMULAS_FILE, 'w') as f:
        json.dump(formulas, f, indent=4)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        logger.error("Template 'index.html' not found. Check if templates directory exists and contains the file.")
        abort(500, description="Template not found. Please ensure the application is properly set up.")

@app.route('/dashboard')
def dashboard():
    try:
        inventory = {
            'rice': 1000,
            'beans': 800,
            'oil': 500,
            'flour': 600,
            'sugar': 400
        }
        alerts = []
        formulas = load_formulas()
        return render_template('dashboard.html', 
                             inventory=inventory,
                             alerts=alerts,
                             formulas=formulas)
    except TemplateNotFound:
        logger.error("Template 'dashboard.html' not found. Check if templates directory exists and contains the file.")
        abort(500, description="Template not found. Please ensure the application is properly set up.")

@app.route('/inventory')
def inventory():
    current_inventory = inventory_manager.get_inventory_levels()
    inventory_history = inventory_manager.generate_inventory_report()
    return render_template('inventory.html', 
                         current_inventory=current_inventory,
                         inventory_history=inventory_history)

@app.route('/distribution-routes')
def distribution_routes():
    delivery_points = [(area['location'], area_id) 
                      for area_id, area in fds.vulnerable_areas.items()]
    routes = route_optimizer.optimize_route((0,0), [loc for loc, _ in delivery_points])
    return render_template('routes.html', routes=routes, areas=fds.vulnerable_areas)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_data = {
            'area_id': request.form['area_id'],
            'rating': int(request.form['rating']),
            'comments': request.form['comments'],
            'timestamp': datetime.now().isoformat()
        }
        feedback_db[len(feedback_db)] = feedback_data
        flash('Thank you for your feedback!')
        return redirect(url_for('feedback'))
    
    return render_template('feedback.html', 
                         areas=fds.vulnerable_areas,
                         feedback_history=feedback_db)

@app.route('/delivery-confirmation', methods=['GET', 'POST'])
def delivery_confirmation():
    if request.method == 'POST':
        confirmation = {
            'area_id': request.form['area_id'],
            'received_quantity': float(request.form['quantity']),
            'condition': request.form['condition'],
            'timestamp': datetime.now().isoformat()
        }
        delivery_confirmations[len(delivery_confirmations)] = confirmation
        
        # Record the delivery in the system
        fds.record_delivery(
            confirmation['area_id'],
            confirmation['received_quantity'],
            datetime.now()
        )
        
        flash('Delivery confirmation recorded!')
        return redirect(url_for('delivery_confirmation'))
    
    return render_template('delivery_confirmation.html',
                         areas=fds.vulnerable_areas,
                         confirmations=delivery_confirmations)

@app.route('/analytics')
def analytics():
    # Generate analytics data
    inventory_data = inventory_manager.generate_inventory_report()
    
    # Create visualization data
    inventory_viz = DataVisualizer.plot_inventory_levels(inventory_data)
    
    return render_template('analytics.html',
                         inventory_plot=inventory_viz,
                         feedback_data=feedback_db,
                         delivery_data=delivery_confirmations)

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory_manager.get_inventory_levels())

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alert_system.get_active_alerts())

@app.route('/distribution-updates')
def get_distribution_updates():
    return jsonify(distribution_updates)

@app.route('/add-update', methods=['POST'])
def add_update():
    update = {
        'timestamp': datetime.now().isoformat(),
        'location': request.form['location'],
        'status': request.form['status'],
        'message': request.form['message']
    }
    
    # Check if this is an arrival in Turkana
    if (update['location'].lower() == 'turkana' and 
        update['status'] == 'arrived'):
        record_automatic_delivery('turkana', TURKANA_LOCATION)
        
        # Add SMS notification (you would integrate with an SMS service here)
        sms_message = "Chakula kimefika Turkana. Tafadhali kuja na kitambulisho kuchukua mgao wako."
        print(f"SMS would be sent: {sms_message}")  # For demonstration
        
    distribution_updates.append(update)
    return jsonify({'success': True})

@app.route('/update_formulas', methods=['POST'])
def update_formulas():
    formulas = {
        'demand_formula': request.form['demand_formula'],
        'allocation_formula': request.form['allocation_formula'],
        'distribution_formula': request.form['distribution_formula']
    }
    save_formulas(formulas)
    flash('Formulas updated successfully!')
    return redirect(url_for('dashboard'))

@app.route('/formulas')
def show_formulas():
    formulas_data = {
        'nutritional_density': {
            'name': 'Nutritional Density Index (NDI)',
            'formula': 'NDI = Σ(Ni × Wi) / (V × M)',
            'variables': {
                'Ni': 'Nutrient content of item i',
                'Wi': 'Weight of item i',
                'V': 'Total volume',
                'M': 'Mass factor'
            },
            'example': '(120 × 0.8 + 85 × 0.6) / (100 × 0.9) = 1.73'
        },
        'transport_efficiency': {
            'name': 'Transportation Efficiency Coefficient (TEC)',
            'formula': 'TEC = (M × D) / (F × t × √T)',
            'variables': {
                'M': 'Mass transported (kg)',
                'D': 'Distance (km)',
                'F': 'Fuel consumption',
                't': 'Time taken',
                'T': 'Temperature factor'
            },
            'example': '(1000 × 150) / (45 × 8 × √30) = 71.82'
        },
        'storage_optimization': {
            'name': 'Storage Optimization Factor (SOF)',
            'formula': 'SOF = (Cs × Ts × Es) / (Vt × Lt)',
            'variables': {
                'Cs': 'Storage capacity',
                'Ts': 'Temperature stability',
                'Es': 'Energy efficiency',
                'Vt': 'Total volume',
                'Lt': 'Loss tolerance'
            },
            'example': '(1000 × 0.95 × 0.88) / (800 × 0.05) = 20.9'
        },
        'perishability_index': {
            'name': 'Food Perishability Index (FPI)',
            'formula': 'FPI = e^(-kt) × (1 - H/100) × (T/Tref)',
            'variables': {
                'k': 'Decay constant',
                't': 'Time in storage',
                'H': 'Humidity percentage',
                'T': 'Temperature',
                'Tref': 'Reference temperature'
            },
            'example': '2.718^(-0.02 × 24) × (1 - 65/100) × (20/25) = 0.245'
        },
        'quality_preservation': {
            'name': 'Quality Preservation Factor (QPF)',
            'formula': 'QPF = Q0 × e^(-kt) × (1 - ΔT/Tc)',
            'variables': {
                'Q0': 'Initial quality',
                'k': 'Degradation rate',
                't': 'Time',
                'ΔT': 'Temperature difference',
                'Tc': 'Critical temperature'
            },
            'example': '1.0 × 2.718^(-0.01 × 48) × (1 - 5/30) = 0.614'
        },
        'logistics_efficiency': {
            'name': 'Logistics Efficiency Index (LEI)',
            'formula': 'LEI = (TD × DR × 100) / (TT × TC)',
            'variables': {
                'TD': 'Total Deliveries',
                'DR': 'Delivery Rate',
                'TT': 'Total Time',
                'TC': 'Total Cost'
            },
            'example': '(50 × 0.95 × 100) / (24 × 1000) = 0.198'
        },
        'distribution_density': {
            'name': 'Distribution Density Factor (DDF)',
            'formula': 'DDF = (P × VA) / (A × √D)',
            'variables': {
                'P': 'Population',
                'VA': 'Vulnerability Assessment',
                'A': 'Area in km²',
                'D': 'Distance to nearest center'
            },
            'example': '(1000 × 0.8) / (100 × √50) = 1.13'
        }
    }
    
    return render_template('formulas.html', formulas=formulas_data)

@app.route('/scientific-formulas')
def scientific_formulas():
    formulas_data = {
        'nutritional_density': {
            'name': 'Nutritional Density Index (NDI)',
            'formula': 'NDI = Σ(Ni × Wi) / (V × M)',
            'variables': {
                'Ni': 'Nutrient content of item i',
                'Wi': 'Weight of item i',
                'V': 'Total volume',
                'M': 'Mass factor'
            },
            'example': '(120 × 0.8 + 85 × 0.6) / (100 × 0.9) = 1.73'
        },
        'transport_efficiency': {
            'name': 'Transportation Efficiency Coefficient (TEC)',
            'formula': 'TEC = (M × D) / (F × t × √T)',
            'variables': {
                'M': 'Mass transported (kg)',
                'D': 'Distance (km)',
                'F': 'Fuel consumption',
                't': 'Time taken',
                'T': 'Temperature factor'
            },
            'example': '(1000 × 150) / (45 × 8 × √30) = 71.82'
        },
        'storage_optimization': {
            'name': 'Storage Optimization Factor (SOF)',
            'formula': 'SOF = (Cs × Ts × Es) / (Vt × Lt)',
            'variables': {
                'Cs': 'Storage capacity',
                'Ts': 'Temperature stability',
                'Es': 'Energy efficiency',
                'Vt': 'Total volume',
                'Lt': 'Loss tolerance'
            },
            'example': '(1000 × 0.95 × 0.88) / (800 × 0.05) = 20.9'
        },
        'perishability_index': {
            'name': 'Food Perishability Index (FPI)',
            'formula': 'FPI = e^(-kt) × (1 - H/100) × (T/Tref)',
            'variables': {
                'k': 'Decay constant',
                't': 'Time in storage',
                'H': 'Humidity percentage',
                'T': 'Temperature',
                'Tref': 'Reference temperature'
            },
            'example': '2.718^(-0.02 × 24) × (1 - 65/100) × (20/25) = 0.245'
        },
        'quality_preservation': {
            'name': 'Quality Preservation Factor (QPF)',
            'formula': 'QPF = Q0 × e^(-kt) × (1 - ΔT/Tc)',
            'variables': {
                'Q0': 'Initial quality',
                'k': 'Degradation rate',
                't': 'Time',
                'ΔT': 'Temperature difference',
                'Tc': 'Critical temperature'
            },
            'example': '1.0 × 2.718^(-0.01 × 48) × (1 - 5/30) = 0.614'
        },
        'logistics_efficiency': {
            'name': 'Logistics Efficiency Index (LEI)',
            'formula': 'LEI = (TD × DR × 100) / (TT × TC)',
            'variables': {
                'TD': 'Total Deliveries',
                'DR': 'Delivery Rate',
                'TT': 'Total Time',
                'TC': 'Total Cost'
            },
            'example': '(50 × 0.95 × 100) / (24 × 1000) = 0.198'
        },
        'distribution_density': {
            'name': 'Distribution Density Factor (DDF)',
            'formula': 'DDF = (P × VA) / (A × √D)',
            'variables': {
                'P': 'Population',
                'VA': 'Vulnerability Assessment',
                'A': 'Area in km²',
                'D': 'Distance to nearest center'
            },
            'example': '(1000 × 0.8) / (100 × √50) = 1.13'
        }
    }
    return render_template('scientific_formulas.html', formulas=formulas_data)

# Add error handlers
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', 
                         error_code=500,
                         error_message=str(e.description)), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                         error_code=404,
                         error_message="The requested page was not found."), 404

# Add template directory check at startup
def check_template_directory():
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if not os.path.exists(template_dir):
        logger.error(f"Templates directory not found at {template_dir}")
        os.makedirs(template_dir)
        logger.info(f"Created templates directory at {template_dir}")
        
    # Check for required template files
    required_templates = ['index.html', 'dashboard.html', 'error.html']
    missing_templates = [t for t in required_templates if not os.path.exists(os.path.join(template_dir, t))]
    
    if missing_templates:
        logger.error(f"Missing required templates: {', '.join(missing_templates)}")
        
        # Create a basic error template if it doesn't exist
        if 'error.html' in missing_templates:
            error_template_path = os.path.join(template_dir, 'error.html')
            with open(error_template_path, 'w') as f:
                f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Food Distribution System - Error</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .error-container { text-align: center; }
        .home-link { display: inline-block; margin-top: 20px; color: #0066cc; text-decoration: none; }
        .home-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>Error {{ error_code }}</h1>
        <p>{{ error_message }}</p>
        <a href="/" class="home-link">Return to Food Distribution System</a>
    </div>
</body>
</html>
''')
            logger.info("Created basic error.html template")

        # Create a basic index template if it doesn't exist
        if 'index.html' in missing_templates:
            index_template_path = os.path.join(template_dir, 'index.html')
            with open(index_template_path, 'w') as f:
                f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Food Distribution System</title>
    <style>
        body { 
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            padding: 20px 0;
            background-color: #2c3e50;
            color: white;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 20px -20px;
        }
        h1 { 
            margin: 0;
            font-size: 2.5em;
        }
        .subtitle {
            color: #ecf0f1;
            margin-top: 10px;
        }
        nav {
            margin: 20px 0;
            text-align: center;
        }
        nav a {
            display: inline-block;
            padding: 12px 24px;
            margin: 0 10px;
            color: white;
            background-color: #3498db;
            text-decoration: none;
            border-radius: 4px;
            transition: background-color 0.3s;
            font-weight: bold;
        }
        nav a:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
        }
        .system-info {
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Food Distribution System</h1>
            <div class="subtitle">Efficient Distribution Management Platform</div>
        </div>
        <nav>
            <a href="/dashboard">Dashboard</a>
            <a href="/inventory">Inventory</a>
            <a href="/distribution-routes">Routes</a>
            <a href="/feedback">Feedback</a>
            <a href="/delivery-confirmation">Deliveries</a>
            <a href="/analytics">Analytics</a>
        </nav>
        <div class="system-info">
            <p>Welcome to the Food Distribution System</p>
            <p>A comprehensive platform for managing and optimizing food distribution operations</p>
        </div>
    </div>
</body>
</html>
''')
            logger.info("Created basic index.html template")

# Add this function before the main block
def get_local_ip():
    try:
        # Get the local machine's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# Modify the main block to display access URLs
if __name__ == '__main__':
    check_template_directory()
    initialize_sample_data()
    
    # Use environment variables or configuration file for these settings
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    # Get and display the access URLs
    local_ip = get_local_ip()
    logger.info("=" * 60)
    logger.info("Food Distribution System is starting up!")
    logger.info("=" * 60)
    logger.info(f"Local access URL: http://localhost:{port}")
    logger.info(f"Network access URL: http://{local_ip}:{port}")
    logger.info("=" * 60)
    logger.info("Share the Network access URL with users on the same network")
    logger.info("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    ) 