"""
Prediction Engine
Combines Markov and LSTM models for attack prediction with confidence and risk scoring
"""

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import AttackPreprocessor
from models.markov_model import MarkovChainModel
from models.lstm_model import LSTMAttackModel


# Risk level classification
RISK_LEVELS = {
    # LOW risk attacks
    'scan': 'LOW', 'port_scan': 'LOW', 'reconnaissance': 'LOW', 'login_attempt': 'LOW',
    'service_enum': 'LOW', 'os_fingerprint': 'LOW', 'network_discovery': 'LOW',
    
    # MEDIUM risk attacks
    'brute_force': 'MEDIUM', 'password_spray': 'MEDIUM', 'credential_stuffing': 'MEDIUM',
    'sql_injection': 'MEDIUM', 'command_injection': 'MEDIUM', 'phishing': 'MEDIUM',
    'exploit_public_app': 'MEDIUM', 'hash_crack': 'MEDIUM', 'file_search': 'MEDIUM',
    'account_discovery': 'MEDIUM', 'system_info': 'MEDIUM', 'drive_by_download': 'MEDIUM',
    
    # HIGH risk attacks
    'privilege_escalation': 'HIGH', 'lateral_movement': 'HIGH', 'data_exfiltration': 'HIGH',
    'backdoor_installation': 'HIGH', 'credential_theft': 'HIGH', 'credential_dumping': 'HIGH',
    'pass_the_hash': 'HIGH', 'exploit_vulnerability': 'HIGH', 'sudo_abuse': 'HIGH',
    'dll_hijacking': 'HIGH', 'remote_desktop': 'HIGH', 'smb_exploit': 'HIGH',
    'scheduled_task': 'HIGH', 'registry_modification': 'HIGH', 'service_creation': 'HIGH',
    'log_deletion': 'HIGH', 'disable_av': 'HIGH', 'obfuscation': 'HIGH',
    'process_injection': 'HIGH', 'keylogging': 'HIGH', 'token_theft': 'HIGH',
    'data_collection': 'HIGH', 'screen_capture': 'HIGH', 'clipboard_data': 'HIGH',
    'email_collection': 'HIGH', 'exfil_over_c2': 'HIGH', 'exfil_to_cloud': 'HIGH',
    'dns_exfiltration': 'HIGH', 'data_destruction': 'HIGH', 'ransomware': 'HIGH',
    'defacement': 'HIGH', 'dos_attack': 'HIGH', 'persistence': 'HIGH'
}


class AttackPredictor:
    """Unified prediction engine using multiple models"""
    
    def __init__(self, models_dir='models'):
        """Initialize predictor with models"""
        self.models_dir = models_dir
        self.preprocessor = None
        self.markov_model = None
        self.lstm_model = None
        
    def load_models(self):
        """Load all models"""
        print("Loading models...")
        
        # Load preprocessor
        self.preprocessor = AttackPreprocessor.load(f'{self.models_dir}/preprocessor.pkl')
        
        # Load Markov model
        self.markov_model = MarkovChainModel.load(f'{self.models_dir}/markov_model.pkl')
        
        # Load LSTM model
        self.lstm_model = LSTMAttackModel.load(f'{self.models_dir}/lstm_model.keras')
        
        print("All models loaded successfully!")
        
    def predict_next_attack(self, sequence, model_type='ensemble', top_k=5):
        """
        Predict next attack in sequence
        
        Args:
            sequence: List of attack names (e.g., ['scan', 'login_attempt', 'brute_force'])
            model_type: 'markov', 'lstm', or 'ensemble' (default)
            top_k: Number of predictions to return
            
        Returns:
            dict with predictions, confidence, and risk assessment
        """
        if not sequence or len(sequence) == 0:
            return {
                'error': 'Empty sequence provided',
                'predictions': []
            }
        
        # Validate attacks exist in vocabulary
        valid_sequence = []
        for attack in sequence:
            if self.preprocessor.encode_attack(attack) != 0:
                valid_sequence.append(attack)
        
        if not valid_sequence:
            return {
                'error': 'No valid attacks in sequence',
                'predictions': []
            }
        
        predictions = []
        
        if model_type in ['markov', 'ensemble']:
            # Get Markov predictions
            markov_preds = self.markov_model.predict(valid_sequence, top_k=top_k)
            
            if model_type == 'markov':
                predictions = [
                    {
                        'attack': attack,
                        'confidence': float(prob),
                        'risk_level': RISK_LEVELS.get(attack, 'MEDIUM'),
                        'model': 'markov'
                    }
                    for attack, prob in markov_preds
                ]
        
        if model_type in ['lstm', 'ensemble']:
            # Encode and pad sequence for LSTM
            encoded = self.preprocessor.encode_sequence(valid_sequence)
            padded = pad_sequences([encoded], maxlen=self.preprocessor.max_sequence_length, padding='pre')
            
            # Get LSTM predictions
            lstm_preds = self.lstm_model.predict(padded[0], top_k=top_k)
            
            if model_type == 'lstm':
                predictions = [
                    {
                        'attack': self.preprocessor.decode_attack(idx),
                        'confidence': float(prob),
                        'risk_level': RISK_LEVELS.get(self.preprocessor.decode_attack(idx), 'MEDIUM'),
                        'model': 'lstm'
                    }
                    for idx, prob in lstm_preds
                    if self.preprocessor.decode_attack(idx) != 'unknown'
                ]
        
        if model_type == 'ensemble':
            # Combine predictions from both models
            combined_scores = {}
            
            # Add Markov predictions (weight: 0.3)
            for attack, prob in self.markov_model.predict(valid_sequence, top_k=10):
                combined_scores[attack] = combined_scores.get(attack, 0) + prob * 0.3
            
            # Add LSTM predictions (weight: 0.7)
            encoded = self.preprocessor.encode_sequence(valid_sequence)
            padded = pad_sequences([encoded], maxlen=self.preprocessor.max_sequence_length, padding='pre')
            lstm_preds = self.lstm_model.predict(padded[0], top_k=10)
            
            for idx, prob in lstm_preds:
                attack = self.preprocessor.decode_attack(idx)
                if attack != 'unknown':
                    combined_scores[attack] = combined_scores.get(attack, 0) + prob * 0.7
            
            # Sort and get top k
            sorted_preds = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            predictions = [
                {
                    'attack': attack,
                    'confidence': float(score),
                    'risk_level': RISK_LEVELS.get(attack, 'MEDIUM'),
                    'model': 'ensemble'
                }
                for attack, score in sorted_preds
            ]
        
        if not predictions:
            return {
                'error': 'No predictions available',
                'predictions': []
            }
        
        # Add overall risk assessment
        top_prediction = predictions[0]
        
        result = {
            'input_sequence': sequence,
            'valid_sequence': valid_sequence,
            'predicted_attack': top_prediction['attack'],
            'confidence': top_prediction['confidence'],
            'risk_level': top_prediction['risk_level'],
            'model_used': model_type,
            'top_predictions': predictions,
            'sequence_length': len(valid_sequence)
        }
        
        return result
    
    def get_risk_description(self, risk_level):
        """Get description for risk level"""
        descriptions = {
            'LOW': 'Reconnaissance or initial probing. Monitor but not immediately dangerous.',
            'MEDIUM': 'Active attack attempts. Requires attention and investigation.',
            'HIGH': 'Critical threat! Immediate action required. System compromise likely.'
        }
        return descriptions.get(risk_level, 'Unknown risk level')


def test_predictor():
    """Test the prediction engine"""
    print("Testing Attack Prediction Engine\n")
    
    # Initialize predictor
    predictor = AttackPredictor()
    predictor.load_models()
    
    # Test sequences
    test_sequences = [
        ['scan', 'port_scan', 'login_attempt'],
        ['scan', 'login_attempt', 'brute_force'],
        ['phishing', 'login_attempt', 'privilege_escalation'],
        ['port_scan', 'service_enum', 'exploit_public_app'],
    ]
    
    print("\nRunning test predictions...\n")
    
    for seq in test_sequences:
        print(f"{'='*70}")
        print(f"Input: {' -> '.join(seq)}")
        print(f"{'-'*70}")
        
        # Ensemble prediction
        result = predictor.predict_next_attack(seq, model_type='ensemble', top_k=5)
        
        if 'error' not in result:
            print(f"Predicted Next Attack: {result['predicted_attack']}")
            print(f"Confidence: {result['confidence']:.1%}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Risk Description: {predictor.get_risk_description(result['risk_level'])}")
            print(f"\nTop 5 Predictions:")
            for i, pred in enumerate(result['top_predictions'], 1):
                print(f"  {i}. {pred['attack']:<25} {pred['confidence']:>6.1%}  [{pred['risk_level']}]")
        else:
            print(f"Error: {result['error']}")
        
        print()
    
    print("Testing complete!")


if __name__ == "__main__":
    test_predictor()
