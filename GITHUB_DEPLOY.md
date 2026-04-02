# 🚀 Deploy via GitHub (GitHub Actions → Render)

## Step 1: Push to GitHub

Your code is ready. Push to GitHub:

```bash
git push origin main
```

## Step 2: Connect Render to GitHub

1. Go to https://render.com
2. Sign up with **GitHub**
3. Click **"New +"** → **"Web Service"**
4. Select **"Build and deploy from a Git repository"**
5. Connect your GitHub account
6. Select your repo: `E-Commerce-Website-LifestyleMart`
7. Configure:
   - **Name:** `lifestylemart`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
8. Click **"Create Web Service"**

## Step 3: Auto-Deploy Enabled! 🎉

Now every time you push to GitHub, Render automatically deploys!

**Your URL:** `https://lifestylemart.onrender.com`

---

## 🔑 Login Credentials

- **Admin:** `admin@lifestylemart.com` / `admin123`
- **User:** `john@example.com` / `password123`

---

## 🔄 How It Works

1. You push code to GitHub
2. GitHub Actions triggers
3. Render automatically deploys
4. Your site updates in 2 minutes

---

## 📁 Files Created for Deployment

- `.github/workflows/deploy.yml` - GitHub Actions workflow
- `Dockerfile` - Container config
- `railway.toml` - Railway config (backup)
- `netlify.toml` - Netlify config (backup)
- `Procfile` - Process file
- `runtime.txt` - Python version

---

## 🆘 Need Help?

If GitHub Actions fails, use the **direct Render method**:
1. https://render.com → New Web Service
2. Connect GitHub repo
3. Deploy manually (no Actions needed)
