"""
Data Preprocessing Module
Handles encoding, sequence preparation, and train/test split
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import Counter


class AttackPreprocessor:
    """Preprocesses attack sequences for model training"""
    
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.attack_to_idx = {}
        self.idx_to_attack = {}
        self.vocab_size = 0
        self.max_sequence_length = 0
        
    def fit(self, sequences):
        """
        Fit the encoder on attack sequences
        
        Args:
            sequences: List of attack sequences (strings or lists)
        """
        # Extract all unique attacks
        all_attacks = []
        for seq in sequences:
            if isinstance(seq, str):
                attacks = seq.split(' -> ')
            else:
                attacks = seq
            all_attacks.extend(attacks)
        
        # Get unique attacks
        unique_attacks = sorted(list(set(all_attacks)))
        
        # Fit label encoder
        self.label_encoder.fit(unique_attacks)
        
        # Create mappings
        self.attack_to_idx = {attack: idx + 1 for idx, attack in enumerate(unique_attacks)}  # Start from 1 (0 is padding)
        self.idx_to_attack = {idx: attack for attack, idx in self.attack_to_idx.items()}
        self.vocab_size = len(unique_attacks) + 1  # +1 for padding
        
        # Calculate max sequence length
        max_len = 0
        for seq in sequences:
            if isinstance(seq, str):
                length = len(seq.split(' -> '))
            else:
                length = len(seq)
            max_len = max(max_len, length)
        
        self.max_sequence_length = max_len
        
        print(f"Fitted preprocessor:")
        print(f"  - Vocabulary size: {self.vocab_size}")
        print(f"  - Unique attacks: {len(unique_attacks)}")
        print(f"  - Max sequence length: {self.max_sequence_length}")
        
        return self
    
    def encode_sequence(self, sequence):
        """
        Encode a single attack sequence
        
        Args:
            sequence: String or list of attacks
            
        Returns:
            List of encoded indices
        """
        if isinstance(sequence, str):
            attacks = sequence.split(' -> ')
        else:
            attacks = sequence
        
        encoded = [self.attack_to_idx.get(attack, 0) for attack in attacks]
        return encoded
    
    def decode_sequence(self, encoded_sequence):
        """
        Decode an encoded sequence back to attack names
        
        Args:
            encoded_sequence: List of indices
            
        Returns:
            List of attack names
        """
        decoded = [self.idx_to_attack.get(idx, 'unknown') for idx in encoded_sequence if idx != 0]
        return decoded
    
    def encode_attack(self, attack_name):
        """Encode a single attack name"""
        return self.attack_to_idx.get(attack_name, 0)
    
    def decode_attack(self, attack_idx):
        """Decode a single attack index"""
        return self.idx_to_attack.get(attack_idx, 'unknown')
    
    def prepare_sequences(self, df, pad=True):
        """
        Prepare sequences for training
        
        Args:
            df: DataFrame with 'input_sequence' and 'next_attack' columns
            pad: Whether to pad sequences
            
        Returns:
            X, y arrays for training
        """
        X = []
        y = []
        
        for idx, row in df.iterrows():
            # Encode input sequence
            input_seq = self.encode_sequence(row['input_sequence'])
            
            # Encode output attack
            output = self.encode_attack(row['next_attack'])
            
            if output != 0:  # Skip unknown attacks
                X.append(input_seq)
                y.append(output)
        
        # Pad sequences if requested
        if pad:
            X = pad_sequences(X, maxlen=self.max_sequence_length, padding='pre')
        
        return np.array(X), np.array(y)
    
    def save(self, filepath):
        """Save preprocessor to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"Saved preprocessor to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load preprocessor from file"""
        with open(filepath, 'rb') as f:
            preprocessor = pickle.load(f)
        print(f"Loaded preprocessor from {filepath}")
        return preprocessor


def prepare_training_data():
    """Load and prepare training data"""
    print("Loading training data...")
    df = pd.read_csv('data/training_pairs.csv')
    
    print(f"Loaded {len(df)} training pairs")
    
    # Initialize and fit preprocessor
    print("\nFitting preprocessor...")
    preprocessor = AttackPreprocessor()
    
    # Combine input and output to get all attacks
    all_sequences = list(df['input_sequence']) + list(df['next_attack'].astype(str))
    preprocessor.fit(all_sequences)
    
    # Prepare sequences
    print("\nEncoding sequences...")
    X, y = preprocessor.prepare_sequences(df)
    
    print(f"Prepared data shapes:")
    print(f"  - X: {X.shape}")
    print(f"  - y: {y.shape}")
    
    # Split data
    print("\nSplitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )
    
    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Save preprocessor
    preprocessor.save('models/preprocessor.pkl')
    
    # Save prepared data
    np.save('data/X_train.npy', X_train)
    np.save('data/X_test.npy', X_test)
    np.save('data/y_train.npy', y_train)
    np.save('data/y_test.npy', y_test)
    
    print("\nSaved preprocessed data:")
    print("  - models/preprocessor.pkl")
    print("  - data/X_train.npy, X_test.npy")
    print("  - data/y_train.npy, y_test.npy")
    
    return preprocessor, (X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    print("Attack Pattern Preprocessing\n")
    preprocessor, data = prepare_training_data()
    print("\nPreprocessing complete!")
