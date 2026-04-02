# Manual Deployment Guide for LifestyleMart

## Option 1: Render.com (Recommended - Free)

1. Go to https://render.com and create a free account
2. Click "New +" → "Web Service"
3. Connect your GitHub repo or use "Upload files"
4. Configure:
   - **Name:** lifestylemart
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free ($0/month)
5. Click "Create Web Service"

Your app will be live at: `https://lifestylemart.onrender.com`

---

## Option 2: Railway.app (Free $5 credit)

1. Go to https://railway.app and login with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Railway will auto-detect Python and deploy
5. Add environment variable: `PORT=5000`

---

## Option 3: PythonAnywhere (Always On Free)

1. Go to https://pythonanywhere.com and create account
2. Open Bash console
3. Run:
   ```
   git clone <your-repo-url>
   cd lifestyle-mart-python
   pip install -r requirements.txt
   ```
4. Go to Web tab → Add new web app
5. Select "Flask" and Python 3.11
6. Set path to `/home/<username>/lifestyle-mart-python/app.py`

---

## Default Login Credentials

- **Admin:** admin@lifestylemart.com / admin123
- **User:** john@example.com / password123

---

## Project Status

- Database: SQLite (file-based, auto-created)
- Data: 6 categories, 12 products, 3 users initialized
- Features: Auth, Cart, Checkout, Admin Panel, Reviews all working
- Broken git submodule: FIXED
