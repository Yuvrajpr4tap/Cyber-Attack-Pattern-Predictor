"""
Markov Chain Baseline Model
Rule-based transition model for attack prediction
"""

import pandas as pd
import numpy as np
import pickle
from collections import defaultdict, Counter


class MarkovChainModel:
    """Markov Chain model for attack sequence prediction"""
    
    def __init__(self, order=1):
        """
        Initialize Markov Chain
        
        Args:
            order: Order of the Markov chain (1 = first-order, uses only last state)
        """
        self.order = order
        self.transitions = defaultdict(Counter)
        self.transition_probs = {}
        
    def train(self, sequences):
        """
        Train the Markov chain on attack sequences
        
        Args:
            sequences: List of attack sequences (each is a list of attack names)
        """
        print(f" Training Markov Chain (order={self.order})...")
        
        for sequence in sequences:
            # Build transitions
            for i in range(len(sequence) - 1):
                if self.order == 1:
                    current_state = sequence[i]
                else:
                    # For higher order, use tuple of previous states
                    start_idx = max(0, i - self.order + 1)
                    current_state = tuple(sequence[start_idx:i+1])
                
                next_state = sequence[i + 1]
                self.transitions[current_state][next_state] += 1
        
        # Calculate probabilities
        for state, next_states in self.transitions.items():
            total = sum(next_states.values())
            self.transition_probs[state] = {
                next_state: count / total 
                for next_state, count in next_states.items()
            }
        
        print(f" Trained on {len(sequences)} sequences")
        print(f" Learned {len(self.transitions)} state transitions")
        
    def predict(self, sequence, top_k=5):
        """
        Predict next attack in sequence
        
        Args:
            sequence: List of attacks so far
            top_k: Return top k predictions
            
        Returns:
            List of (attack, probability) tuples
        """
        if not sequence:
            return []
        
        # Get current state
        if self.order == 1:
            current_state = sequence[-1]
        else:
            start_idx = max(0, len(sequence) - self.order)
            current_state = tuple(sequence[start_idx:])
        
        # Get predictions
        if current_state in self.transition_probs:
            predictions = sorted(
                self.transition_probs[current_state].items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
            return predictions
        else:
            # State not seen, return empty
            return []
    
    def predict_next(self, sequence):
        """
        Predict the single most likely next attack
        
        Args:
            sequence: List of attacks
            
        Returns:
            (attack_name, confidence) or (None, 0.0)
        """
        predictions = self.predict(sequence, top_k=1)
        if predictions:
            return predictions[0]
        return (None, 0.0)
    
    def save(self, filepath):
        """Save model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f" Saved Markov model to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load model from file"""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        print(f" Loaded Markov model from {filepath}")
        return model


def train_markov_model():
    """Train and save Markov chain model"""
    print("🔥 Training Markov Chain Baseline Model\n")
    
    # Load data
    print("📊 Loading training data...")
    df_sequences = pd.read_csv('data/attack_sequences.csv')
    df_training = pd.read_csv('data/training_pairs.csv')
    
    print(f" Loaded {len(df_sequences)} sequences")
    
    # Convert sequences to lists
    sequences = []
    for seq_str in df_sequences['attack_sequence']:
        sequence = seq_str.split(' -> ')
        sequences.append(sequence)
    
    # Train first-order Markov chain
    print("\n🎯 Training first-order Markov chain...")
    markov_model = MarkovChainModel(order=1)
    markov_model.train(sequences)
    
    # Test predictions
    print("\n🧪 Testing predictions...")
    test_sequence = ['scan', 'port_scan', 'login_attempt']
    predictions = markov_model.predict(test_sequence, top_k=5)
    
    print(f"\nTest sequence: {' -> '.join(test_sequence)}")
    print("Top 5 predictions:")
    for attack, prob in predictions:
        print(f"  {attack}: {prob:.2%}")
    
    # Save model
    markov_model.save('models/markov_model.pkl')
    
    # Evaluate on test set
    print("\n📊 Evaluating on test data...")
    correct = 0
    total = 0
    
    for idx, row in df_training.head(100).iterrows():
        input_seq = row['input_sequence'].split(' -> ')
        true_next = row['next_attack']
        
        pred_next, confidence = markov_model.predict_next(input_seq)
        
        if pred_next == true_next:
            correct += 1
        total += 1
    
    accuracy = correct / total if total > 0 else 0
    print(f" Accuracy on sample: {accuracy:.2%} ({correct}/{total})")
    
    print("\n✅ Markov model training complete!")
    return markov_model


if __name__ == "__main__":
    model = train_markov_model()
