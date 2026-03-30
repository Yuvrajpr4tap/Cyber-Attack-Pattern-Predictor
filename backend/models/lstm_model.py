"""
LSTM Model for Attack Pattern Prediction
Advanced sequence model using TensorFlow/Keras
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import AttackPreprocessor


class LSTMAttackModel:
    """LSTM model for attack sequence prediction"""
    
    def __init__(self, vocab_size, max_length, embedding_dim=64):
        """
        Initialize LSTM model
        
        Args:
            vocab_size: Size of attack vocabulary
            max_length: Maximum sequence length
            embedding_dim: Dimension of embedding layer
        """
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.embedding_dim = embedding_dim
        self.model = None
        self.history = None
        
    def build_model(self):
        """Build LSTM architecture"""
        print(" Building LSTM model...")
        
        model = Sequential([
            # Embedding layer
            Embedding(
                input_dim=self.vocab_size,
                output_dim=self.embedding_dim,
                input_length=self.max_length,
                mask_zero=True
            ),
            
            # LSTM layers
            LSTM(128, return_sequences=True),
            Dropout(0.3),
            LSTM(64),
            Dropout(0.3),
            
            # Dense layers
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(self.vocab_size, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        
        print(" Model architecture:")
        model.summary()
        
        return self
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """
        Train the LSTM model
        
        Args:
            X_train: Training sequences
            y_train: Training labels
            X_val: Validation sequences
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
        """
        print(f"\n Training LSTM model...")
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                'models/lstm_model_best.keras',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=0
            )
        ]
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\n✅ Training complete!")
        
        # Print final metrics
        final_acc = self.history.history['accuracy'][-1]
        final_val_acc = self.history.history['val_accuracy'][-1]
        print(f"Final training accuracy: {final_acc:.2%}")
        print(f"Final validation accuracy: {final_val_acc:.2%}")
        
        return self
    
    def predict(self, sequence, top_k=5):
        """
        Predict next attack
        
        Args:
            sequence: Encoded sequence (padded)
            top_k: Return top k predictions
            
        Returns:
            List of (attack_idx, probability) tuples
        """
        if len(sequence.shape) == 1:
            sequence = sequence.reshape(1, -1)
        
        predictions = self.model.predict(sequence, verbose=0)[0]
        
        # Get top k predictions
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        top_predictions = [(idx, predictions[idx]) for idx in top_indices]
        
        return top_predictions
    
    def predict_next(self, sequence):
        """
        Predict single most likely next attack
        
        Args:
            sequence: Encoded sequence (padded)
            
        Returns:
            (attack_idx, confidence)
        """
        predictions = self.predict(sequence, top_k=1)
        if predictions:
            return predictions[0]
        return (None, 0.0)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model on test set
        
        Args:
            X_test: Test sequences
            y_test: Test labels
            
        Returns:
            (loss, accuracy)
        """
        print("\n Evaluating on test set...")
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {loss:.4f}")
        print(f"Test Accuracy: {accuracy:.2%}")
        return loss, accuracy
    
    def save(self, filepath):
        """Save model to file"""
        self.model.save(filepath)
        print(f" Saved LSTM model to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load model from file"""
        model = load_model(filepath)
        print(f" Loaded LSTM model from {filepath}")
        
        # Wrap in LSTMAttackModel
        # Extract shape information from model configuration
        vocab_size = model.output_shape[-1]
        max_length = model.input_shape[1]
        embedding_dim = model.layers[0].output_dim
        
        lstm_model = LSTMAttackModel(
            vocab_size=vocab_size,
            max_length=max_length,
            embedding_dim=embedding_dim
        )
        lstm_model.model = model
        return lstm_model
    
    def plot_training_history(self, save_path='models/training_history.png'):
        """Plot training history"""
        if self.history is None:
            print("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy plot
        ax1.plot(self.history.history['accuracy'], label='Train')
        ax1.plot(self.history.history['val_accuracy'], label='Validation')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.history.history['loss'], label='Train')
        ax2.plot(self.history.history['val_loss'], label='Validation')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f" Saved training history plot to {save_path}")
        plt.close()


def train_lstm_model():
    """Train and save LSTM model"""
    print("🔥 Training LSTM Attack Prediction Model\n")
    
    # Load preprocessor
    preprocessor = AttackPreprocessor.load('models/preprocessor.pkl')
    
    # Load data
    print("\n Loading training data...")
    X_train = np.load('data/X_train.npy')
    X_test = np.load('data/X_test.npy')
    y_train = np.load('data/y_train.npy')
    y_test = np.load('data/y_test.npy')
    
    print(f" Training set: {X_train.shape}")
    print(f" Test set: {X_test.shape}")
    
    # Create model
    lstm_model = LSTMAttackModel(
        vocab_size=preprocessor.vocab_size,
        max_length=preprocessor.max_sequence_length,
        embedding_dim=64
    )
    
    # Build and train
    lstm_model.build_model()
    lstm_model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
    
    # Evaluate
    lstm_model.evaluate(X_test, y_test)
    
    # Save model
    lstm_model.save('models/lstm_model.keras')
    
    # Plot training history
    lstm_model.plot_training_history()
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    test_seq = X_test[0:1]
    predictions = lstm_model.predict(test_seq, top_k=5)
    
    print(f"Input sequence: {preprocessor.decode_sequence(test_seq[0])}")
    print("Top 5 predictions:")
    for idx, prob in predictions:
        attack_name = preprocessor.decode_attack(idx)
        print(f"  {attack_name}: {prob:.2%}")
    
    print("\n✅ LSTM model training complete!")
    return lstm_model


if __name__ == "__main__":
    model = train_lstm_model()
