from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from database import Database
import json
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db = Database()

# Simple authentication (in production, use proper authentication)
USERNAME = 'admin'
PASSWORD = 'locapp2024'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

def get_property_id():
    """Get property_id from query parameter, default to 1 (Mazet BSA)"""
    return request.args.get('property_id', 1, type=int)

# Routes for pages
@app.route('/')
def index():
    properties = db.get_all_properties()
    return render_template('index.html', properties=properties)

@app.route('/general')
def general_page():
    properties = db.get_all_properties()
    return render_template('general.html', properties=properties)

@app.route('/wifi')
def wifi_page():
    properties = db.get_all_properties()
    return render_template('wifi.html', properties=properties)

@app.route('/address')
def address_page():
    properties = db.get_all_properties()
    return render_template('address.html', properties=properties)

@app.route('/parking')
def parking_page():
    properties = db.get_all_properties()
    return render_template('parking.html', properties=properties)

@app.route('/access')
def access_page():
    properties = db.get_all_properties()
    return render_template('access.html', properties=properties)

@app.route('/contact')
def contact_page():
    properties = db.get_all_properties()
    return render_template('contact.html', properties=properties)

@app.route('/activities')
def activities_page():
    properties = db.get_all_properties()
    return render_template('activities.html', properties=properties)

@app.route('/services')
def services_page():
    properties = db.get_all_properties()
    return render_template('services.html', properties=properties)

@app.route('/emergency')
def emergency_page():
    properties = db.get_all_properties()
    return render_template('emergency.html', properties=properties)

# API Routes - Properties
@app.route('/api/properties', methods=['GET'])
def get_properties():
    data = db.get_all_properties()
    return jsonify(data)

@app.route('/api/properties/<slug>', methods=['GET'])
def get_property_by_slug(slug):
    data = db.get_property_by_slug(slug)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Property not found'}), 404

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    data = db.get_property(property_id)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Property not found'}), 404

# API Routes - General Info
@app.route('/api/general', methods=['GET'])
def get_general_info():
    property_id = get_property_id()
    data = db.get_general_info(property_id)
    return jsonify(data)

@app.route('/api/general', methods=['PUT'])
@requires_auth
def update_general_info():
    property_id = get_property_id()
    data = request.json
    db.update_general_info(property_id, data)
    return jsonify({'success': True, 'message': 'Informations générales mises à jour'})

# API Routes - WiFi
@app.route('/api/wifi', methods=['GET'])
def get_wifi():
    property_id = get_property_id()
    data = db.get_wifi_config(property_id)
    return jsonify(data)

@app.route('/api/wifi', methods=['PUT'])
@requires_auth
def update_wifi():
    property_id = get_property_id()
    data = request.json
    db.update_wifi_config(property_id, data)
    return jsonify({'success': True, 'message': 'Configuration WiFi mise à jour'})

# API Routes - Address
@app.route('/api/address', methods=['GET'])
def get_address():
    property_id = get_property_id()
    data = db.get_address(property_id)
    return jsonify(data)

@app.route('/api/address', methods=['PUT'])
@requires_auth
def update_address():
    property_id = get_property_id()
    data = request.json
    db.update_address(property_id, data)
    return jsonify({'success': True, 'message': 'Adresse mise à jour'})

# API Routes - Parking
@app.route('/api/parking', methods=['GET'])
def get_parking():
    property_id = get_property_id()
    data = db.get_parking_info(property_id)
    return jsonify(data)

@app.route('/api/parking', methods=['PUT'])
@requires_auth
def update_parking():
    property_id = get_property_id()
    data = request.json
    db.update_parking_info(property_id, data)
    return jsonify({'success': True, 'message': 'Informations parking mises à jour'})

# API Routes - Access
@app.route('/api/access', methods=['GET'])
def get_access():
    property_id = get_property_id()
    data = db.get_access_info(property_id)
    return jsonify(data)

@app.route('/api/access', methods=['PUT'])
@requires_auth
def update_access():
    property_id = get_property_id()
    data = request.json
    db.update_access_info(property_id, data)
    return jsonify({'success': True, 'message': 'Informations d\'accès mises à jour'})

# API Routes - Contact
@app.route('/api/contact', methods=['GET'])
def get_contact():
    property_id = get_property_id()
    data = db.get_contact_info(property_id)
    return jsonify(data)

@app.route('/api/contact', methods=['PUT'])
@requires_auth
def update_contact():
    property_id = get_property_id()
    data = request.json
    db.update_contact_info(property_id, data)
    return jsonify({'success': True, 'message': 'Informations de contact mises à jour'})

# API Routes - Activities
@app.route('/api/activities', methods=['GET'])
def get_activities():
    property_id = get_property_id()
    data = db.get_all_activities(property_id)
    return jsonify(data)

@app.route('/api/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    data = db.get_activity(activity_id)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Activity not found'}), 404

@app.route('/api/activities', methods=['POST'])
@requires_auth
def create_activity():
    property_id = get_property_id()
    data = request.json
    activity_id = db.create_activity(data, property_id)
    return jsonify({'success': True, 'id': activity_id, 'message': 'Activité créée'})

@app.route('/api/activities/<int:activity_id>', methods=['PUT'])
@requires_auth
def update_activity(activity_id):
    data = request.json
    db.update_activity(activity_id, data)
    return jsonify({'success': True, 'message': 'Activité mise à jour'})

@app.route('/api/activities/<int:activity_id>', methods=['DELETE'])
@requires_auth
def delete_activity(activity_id):
    db.delete_activity(activity_id)
    return jsonify({'success': True, 'message': 'Activité supprimée'})

# API Routes - Activity Categories
@app.route('/api/activity-categories', methods=['GET'])
def get_activity_categories():
    data = db.get_all_activity_categories()
    return jsonify(data)

# API Routes - Nearby Services
@app.route('/api/services', methods=['GET'])
def get_services():
    property_id = get_property_id()
    data = db.get_all_nearby_services(property_id)
    return jsonify(data)

@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    data = db.get_nearby_service(service_id)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Service not found'}), 404

@app.route('/api/services', methods=['POST'])
@requires_auth
def create_service():
    property_id = get_property_id()
    data = request.json
    service_id = db.create_nearby_service(data, property_id)
    return jsonify({'success': True, 'id': service_id, 'message': 'Service créé'})

@app.route('/api/services/<int:service_id>', methods=['PUT'])
@requires_auth
def update_service(service_id):
    data = request.json
    db.update_nearby_service(service_id, data)
    return jsonify({'success': True, 'message': 'Service mis à jour'})

@app.route('/api/services/<int:service_id>', methods=['DELETE'])
@requires_auth
def delete_service(service_id):
    db.delete_nearby_service(service_id)
    return jsonify({'success': True, 'message': 'Service supprimé'})

# API Routes - Emergency Numbers
@app.route('/api/emergency', methods=['GET'])
def get_emergency():
    property_id = get_property_id()
    data = db.get_all_emergency_numbers(property_id)
    return jsonify(data)

# Export endpoint
@app.route('/api/export', methods=['GET'])
def export_data():
    property_id = get_property_id()
    data = db.export_all_data(property_id)
    return jsonify(data)

@app.route('/api/export/download', methods=['GET'])
@requires_auth
def download_export():
    property_id = get_property_id()
    data = db.export_all_data(property_id)

    # Get property info for filename
    property_info = db.get_property(property_id)
    filename = f'locapp_{property_info["slug"] if property_info else "export"}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return send_file(filename, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
