"""
Flask API for Attack Pattern Predictor
Provides REST endpoints for attack prediction
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Add backend directory to path BEFORE any imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Get project root
project_root = os.path.dirname(backend_dir)

# Import the model classes to register them for pickle
from utils.preprocessing import AttackPreprocessor
from models.markov_model import MarkovChainModel
from models.lstm_model import LSTMAttackModel
from predictor import AttackPredictor

# Setup Flask app with static and template folders for React frontend
static_folder = os.path.join(project_root, 'frontend', 'build')
app = Flask(__name__, static_folder=static_folder, static_url_path='')
CORS(app)  # Enable CORS for frontend

# Initialize predictor (load once at startup)
print("Initializing Attack Prediction System...")
predictor = AttackPredictor()
predictor.load_models()
print("System ready!\n")


@app.route('/api')
@app.route('/api/info')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Attack Pattern Predictor API',
        'version': '1.0.0',
        'endpoints': {
            '/api': 'API information',
            '/api/predict': 'POST - Predict next attack',
            '/api/health': 'GET - Health check',
            '/api/attacks': 'GET - List all attack types'
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': all([
            predictor.preprocessor is not None,
            predictor.markov_model is not None,
            predictor.lstm_model is not None
        ])
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict next attack in sequence
    
    Request body:
    {
        "sequence": ["scan", "login_attempt", "brute_force"],
        "model": "ensemble",  # optional: "ensemble", "markov", or "lstm"
        "top_k": 5  # optional: number of predictions to return
    }
    
    Response:
    {
        "success": true,
        "input_sequence": [...],
        "predicted_attack": "privilege_escalation",
        "confidence": 0.915,
        "risk_level": "HIGH",
        "risk_description": "...",
        "top_predictions": [...]
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Extract sequence
        sequence = data.get('sequence', [])
        
        if not sequence:
            return jsonify({
                'success': False,
                'error': 'Empty sequence provided'
            }), 400
        
        if not isinstance(sequence, list):
            return jsonify({
                'success': False,
                'error': 'Sequence must be a list of attack names'
            }), 400
        
        # Extract optional parameters
        model_type = data.get('model', 'ensemble')
        top_k = data.get('top_k', 5)
        
        # Validate model type
        if model_type not in ['ensemble', 'markov', 'lstm']:
            return jsonify({
                'success': False,
                'error': 'Invalid model type. Must be "ensemble", "markov", or "lstm"'
            }), 400
        
        # Make prediction
        result = predictor.predict_next_attack(
            sequence=sequence,
            model_type=model_type,
            top_k=top_k
        )
        
        # Check for errors
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error'],
                'input_sequence': sequence
            }), 400
        
        # Add risk description
        result['risk_description'] = predictor.get_risk_description(result['risk_level'])
        result['success'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/attacks', methods=['GET'])
def list_attacks():
    """List all available attack types"""
    try:
        # Get all attacks from preprocessor
        all_attacks = list(predictor.preprocessor.attack_to_idx.keys())
        
        # Group by risk level
        attacks_by_risk = {
            'LOW': [],
            'MEDIUM': [],
            'HIGH': []
        }
        
        from predictor import RISK_LEVELS
        
        for attack in sorted(all_attacks):
            risk = RISK_LEVELS.get(attack, 'MEDIUM')
            attacks_by_risk[risk].append(attack)
        
        return jsonify({
            'success': True,
            'total_attacks': len(all_attacks),
            'attacks_by_risk': attacks_by_risk,
            'all_attacks': sorted(all_attacks)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/example', methods=['GET'])
def get_example():
    """Get example attack sequences"""
    examples = [
        {
            'name': 'Reconnaissance Phase',
            'sequence': ['scan', 'port_scan', 'service_enum'],
            'description': 'Initial reconnaissance activities'
        },
        {
            'name': 'Credential Attack',
            'sequence': ['scan', 'login_attempt', 'brute_force'],
            'description': 'Attempting to gain access through credentials'
        },
        {
            'name': 'Advanced Persistent Threat',
            'sequence': ['phishing', 'login_attempt', 'privilege_escalation', 'lateral_movement'],
            'description': 'Sophisticated multi-stage attack'
        },
        {
            'name': 'Web Application Attack',
            'sequence': ['scan', 'service_enum', 'exploit_public_app'],
            'description': 'Targeting web application vulnerabilities'
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })


# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React app for all non-API routes"""
    if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Attack Pattern Predictor API Server")
    print("="*70)
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting Flask server on http://localhost:{port}")
    print("\nAvailable endpoints:")
    print("   GET  /api       - API information")
    print("   GET  /api/health - Health check")
    print("   POST /api/predict - Predict next attack")
    print("   GET  /api/attacks - List all attack types")
    print("   GET  /api/example - Get example sequences")
    print("   GET  /           - React frontend app")
    print("\nUse Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
