# Render Deployment Guide

Attack Pattern Predictor - Complete Deployment on Render

## Overview

This guide explains how to deploy the Attack Pattern Predictor application on Render. The application consists of:
- **Backend**: Flask API (Python)
- **Frontend**: React Dashboard
- **Models**: LSTM + Markov Chain ensemble

---

## Prerequisites

1. **Render Account**: Sign up at https://render.com (free tier available)
2. **GitHub Repository**: Project must be pushed to GitHub
3. **Connected GitHub Account**: Link your Render account to GitHub

---

## Step 1: Prepare Your Repository

Your repository should already be cleaned and pushed. Verify you have:

```
✓ .gitignore (excludes large files)
✓ requirements.txt (Python dependencies)
✓ Procfile (build and run instructions)
✓ build.sh (build script for Render)
✓ frontend/ (React app)
✓ backend/ (Flask API)
✓ data/ (for generating datasets)
```

Commit and push the build script:

```bash
git add build.sh build.bat
git commit -m "Add Render deployment scripts"
git push origin main
```

---

## Step 2: Create a Render Web Service

### 2.1 Go to Render Dashboard
1. Log in to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**

### 2.2 Connect GitHub Repository
1. Select **"Connect to GitHub"**
2. Find and select **`Cyber-Attack-Pattern-Predictor`**
3. Click **"Create Web Service"**

### 2.3 Configure Web Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `attack-pattern-predictor` |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app` |

### 2.4 Configure Environment Variables

Add these in the **"Environment"** section:

```
FLASK_ENV = production
PYTHONUNBUFFERED = true
```

### 2.5 Choose Plan

- **Free Plan**: 750 free hours/month (good for testing)
- **Paid Plans**: Start at $7/month for more resources

Click **"Create Web Service"**

---

## Step 3: Monitor Deployment

### 3.1 Build Process
- Render will start building automatically
- Check the **"Logs"** tab to monitor progress
- The build process will:
  1. Install Python dependencies
  2. Generate training data
  3. Train/prepare models (5-10 minutes)
  4. Build React frontend (2-3 minutes)
  5. Start Flask server

### 3.2 Expected Log Output
```
[1/4] Installing Python dependencies...
[2/4] Generating training data...
[3/4] Preparing models...
  → Regenerating preprocessor...
  → Training Markov model...
  → Training LSTM model (this may take a few minutes)...
[4/4] Building React frontend...
Build completed successfully!
```

### 3.3 Deployment Success
- Green checkmark: ✅ Deployment successful
- You'll get a URL like: `https://attack-pattern-predictor-xxxx.onrender.com`

---

## Step 4: Test Your Deployment

### 4.1 Access the Application
1. Click the service URL in Render dashboard
2. Should see the Attack Pattern Predictor dashboard

### 4.2 Test API Endpoints

**Health Check:**
```bash
curl https://your-app.onrender.com/api/health
```

**Get Example Attacks:**
```bash
curl https://your-app.onrender.com/api/example
```

**Make a Prediction:**
```bash
curl -X POST https://your-app.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sequence": ["scan", "login_attempt", "brute_force"],
    "model": "ensemble",
    "top_k": 5
  }'
```

---

## Step 5: Troubleshooting

### Build Fails with "ModuleNotFoundError"
**Cause**: Missing dependencies
**Fix**: Update `requirements.txt` and redeploy

### Models Training Takes Too Long
**Cause**: Free tier has limited resources
**Fix**: Upgrade to paid plan or wait for build to complete (may take 20+ mins)

### Service Sleeps After Inactivity
**Cause**: Free tier services auto-pause
**Fix**: Upgrade to paid plan for always-on service

### CORS Errors in Frontend
**Already Fixed**: CORS is enabled in Flask app

### Models Not Found on Deploy
**Already Fixed**: `build.sh` auto-generates models during build

---

## Step 6: Continuous Deployment

Every time you push to GitHub:

```bash
git add .
git commit -m "Update prediction models"
git push origin main
```

Render will:
1. Detect the change
2. Rebuild the service
3. Redeploy automatically
4. Zero downtime (rolling restart)

---

## Step 7: Monitor Performance (Optional)

In Render Dashboard:
- **Metrics**: CPU, Memory, Disk usage
- **Logs**: Real-time application logs
- **Alerts**: Set up notifications for failures

---

## Step 8: Custom Domain (Optional)

To add a custom domain:

1. Go to **"Settings"** tab
2. Scroll to **"Custom Domains"**
3. Add your domain (requires DNS configuration)
4. Follow Render's DNS setup guide

---

## Costs & Limits

### Free Tier
- 750 free hours/month (~1 service running 24/7)
- Auto-pauses after 15 minutes of inactivity
- 400 MB RAM, 0.5 CPU

### Starter Plan ($7/month)
- Always-on service
- 1 GB RAM, 0.5 CPU
- No auto-pause

### Pro Plan ($12/month+)
- More RAM and CPU
- Concurrent requests

---

## Environment Variables

Add more variables in Render dashboard if needed:

```bash
# Debug mode (disable in production)
FLASK_DEBUG = false

# Model paths (these are relative to project root)
MODELS_DIR = models
DATA_DIR = data
```

Update `backend/app.py` if you change paths.

---

## File Descriptions

- **`Procfile`**: Defines build and web commands
- **`build.sh`**: Shell script for building on Linux/Render
- **`build.bat`**: Windows batch script for local testing
- **`requirements.txt`**: Python package dependencies
- **`runtime.txt`**: Python version specification
- **`frontend/package.json`**: React dependencies and scripts

---

## Next Steps

1. ✅ Deploy on Render
2. ✅ Monitor first deployment
3. ✅ Test all API endpoints
4. 📊 Monitor performance metrics
5. 🔧 Optimize model training (optional)
6. 🌐 Add custom domain (optional)
7. 📧 Set up error notifications (optional)

---

## Support

For issues:
1. Check Render build logs
2. Verify requirements.txt has all dependencies
3. Ensure model training completes
4. Check disk space (models are ~300 MB)

For Render-specific help: https://render.com/docs

---

## Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render account created
- [ ] Web Service created on Render
- [ ] Build command: `bash build.sh`
- [ ] Start command configured
- [ ] Deployment completed successfully
- [ ] Frontend loads without errors
- [ ] `/api/health` returns 200 OK
- [ ] Predictions work correctly
- [ ] Custom domain added (optional)

---

**Deployment Complete!** 🎉

Your Attack Pattern Predictor is now live on Render!
