# Attack Pattern Predictor - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

**Backend (Python):**
```bash
pip install -r requirements.txt
```

**Frontend (React):**
```bash
cd frontend
npm install
cd ..
```

### Step 2: Start Servers

**Terminal 1 - Backend Server:**
```bash
python backend/app.py
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm start
```

### Step 3: Access Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5000

---

## 🧪 Test the System

Run the test suite:
```bash
python test_system.py
```

Test API directly:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sequence": ["scan", "login_attempt", "brute_force"]}'
```

---

## 📖 Example Usage

1. Open http://localhost:3000
2. Enter attack sequence: `scan, login_attempt, brute_force`
3. Click "Predict Next Attack"
4. View results with confidence and risk level

Or try the quick examples provided in the UI!

---

## 🔧 Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is not in use

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Install dependencies: `cd frontend && npm install`
- Check port 3000 is not in use

**Models not found:**
- Models are already trained and included in the `models/` directory
- If missing, run: `python backend/utils/preprocessing.py` then train models

---

## 📚 More Information

See the full README.md for:
- Detailed architecture
- API documentation
- Model performance metrics
- Project structure
- Contributing guidelines

---

**Ready to predict attacks! 🛡️**
