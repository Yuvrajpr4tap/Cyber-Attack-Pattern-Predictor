@echo off
REM Render Build Script for Windows (for local testing)
REM This script prepares your project for Render deployment

echo.
echo ========================================
echo Building Attack Pattern Predictor
echo ========================================
echo.

REM Step 1: Install Python dependencies
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

REM Step 2: Generate training data if it doesn't exist
echo.
echo [2/4] Generating training data...
if not exist "data\training_pairs.csv" (
    echo   - Creating synthetic dataset...
    cd data
    python generate_data.py
    cd ..
) else (
    echo   - Dataset already exists, skipping generation
)

REM Step 3: Prepare models
echo.
echo [3/4] Preparing models...
if not exist "models" mkdir models

if not exist "models\preprocessor.pkl" (
    echo   - Regenerating preprocessor...
    python backend\utils\regenerate_preprocessor.py
) else (
    echo   - Preprocessor already exists
)

if not exist "models\markov_model.pkl" (
    echo   - Training Markov model...
    python -c "from backend.models.markov_model import MarkovChainModel; import pandas as pd; df = pd.read_csv('data\training_pairs.csv'); markov = MarkovChainModel(); markov.train(df); markov.save('models\markov_model.pkl'); print('Markov model trained!')"
) else (
    echo   - Markov model already exists
)

if not exist "models\lstm_model.keras" (
    echo   - Training LSTM model ^(this takes a few minutes^)...
    python -c "import numpy as np; from backend.models.lstm_model import LSTMAttackModel; X_train = np.load('data\X_train.npy'); y_train = np.load('data\y_train.npy'); X_test = np.load('data\X_test.npy'); y_test = np.load('data\y_test.npy'); vocab_size = int(max(X_train.max(), X_test.max(), y_train.max(), y_test.max())) + 1; max_length = X_train.shape[1]; lstm = LSTMAttackModel(vocab_size, max_length); lstm.build_model(); lstm.train(X_train, y_train, X_test, y_test, epochs=30, batch_size=16); lstm.save('models\lstm_model.keras')"
) else (
    echo   - LSTM model already exists
)

REM Step 4: Build React frontend
echo.
echo [4/4] Building React frontend...
cd frontend
call npm install
call npm run build
cd ..
if errorlevel 1 (
    echo ERROR: Failed to build frontend
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
