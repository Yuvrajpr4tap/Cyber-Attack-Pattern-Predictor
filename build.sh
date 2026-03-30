#!/bin/bash
# Render Build Script
# This script runs during the build phase on Render

set -e  # Exit on error

echo "========================================"
echo "Building Attack Pattern Predictor"
echo "========================================"

# Step 1: Install Python dependencies
echo ""
echo "[1/4] Installing Python dependencies..."
pip install -r requirements.txt --upgrade

# Step 2: Generate training data if it doesn't exist
echo ""
echo "[2/4] Generating training data..."
if [ ! -f "data/training_pairs.csv" ]; then
    echo "  → Creating synthetic dataset..."
    cd data
    python generate_data.py
    cd ..
else
    echo "  → Dataset already exists, skipping generation"
fi

# Step 3: Generate/train models if they don't exist
echo ""
echo "[3/4] Preparing models..."
mkdir -p models

# Check if models exist, if not, regenerate
if [ ! -f "models/preprocessor.pkl" ]; then
    echo "  → Regenerating preprocessor..."
    python backend/utils/regenerate_preprocessor.py
else
    echo "  → Preprocessor already exists"
fi

if [ ! -f "models/markov_model.pkl" ]; then
    echo "  → Training Markov model..."
    python -c "
from backend.models.markov_model import MarkovChainModel
import pandas as pd

df = pd.read_csv('data/training_pairs.csv')
markov = MarkovChainModel()
markov.train(df)
markov.save('models/markov_model.pkl')
print('Markov model trained and saved!')
"
else
    echo "  → Markov model already exists"
fi

if [ ! -f "models/lstm_model.keras" ]; then
    echo "  → Training LSTM model (this may take a few minutes)..."
    python -c "
import numpy as np
from backend.models.lstm_model import LSTMAttackModel

# Load data
X_train = np.load('data/X_train.npy')
y_train = np.load('data/y_train.npy')
X_test = np.load('data/X_test.npy')
y_test = np.load('data/y_test.npy')

# Get vocab size from test data shape
vocab_size = np.max([X_train.max(), X_test.max(), y_train.max(), y_test.max()]) + 1
max_length = X_train.shape[1]

# Train model
lstm = LSTMAttackModel(vocab_size=int(vocab_size), max_length=max_length)
lstm.build_model()
lstm.train(X_train, y_train, X_test, y_test, epochs=30, batch_size=16)
lstm.save('models/lstm_model.keras')
print('LSTM model trained and saved!')
"
else
    echo "  → LSTM model already exists"
fi

# Step 4: Build React frontend
echo ""
echo "[4/4] Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
