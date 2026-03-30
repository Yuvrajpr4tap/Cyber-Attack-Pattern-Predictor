"""
Regenerate preprocessor with proper module context for pickle loading
"""

import sys
import os

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.insert(0, backend_dir)

# Change to project root
os.chdir(os.path.join(current_dir, '..', '..'))

# Import from proper module
from backend.utils.preprocessing import AttackPreprocessor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

print("Regenerating preprocessor with proper module context...")

# Load training data
df = pd.read_csv('data/training_pairs.csv')
print(f"Loaded {len(df)} training pairs")

# Initialize and fit preprocessor
preprocessor = AttackPreprocessor()
all_sequences = list(df['input_sequence']) + list(df['next_attack'].astype(str))
preprocessor.fit(all_sequences)

# Prepare sequences
X, y = preprocessor.prepare_sequences(df)
print(f"Prepared data shapes: X={X.shape}, y={y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Save everything
preprocessor.save('models/preprocessor.pkl')
np.save('data/X_train.npy', X_train)
np.save('data/X_test.npy', X_test)
np.save('data/y_train.npy', y_train)
np.save('data/y_test.npy', y_test)

print("Preprocessor regenerated successfully!")
