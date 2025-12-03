# 🚀 Quick Deployment Reference

## Local Development
```bash
# Run the app
streamlit run financial_analysis_app.py

# Access at: http://localhost:8501
```

## Deploy to Streamlit Cloud (FREE)

### Step 1: Prepare Git
```bash
./deploy.sh
# Follow the prompts
```

### Step 2: Create GitHub Repo
- Go to: https://github.com/new
- Name: `financial-document-analysis`
- Visibility: Private (recommended)
- Click "Create repository"

### Step 3: Push Code
```bash
git push -u origin main
```

### Step 4: Deploy on Streamlit
1. Visit: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `financial-document-analysis`
5. Branch: `main`
6. Main file: `financial_analysis_app.py`
7. Click "Deploy"

**Done! Your app will be live in ~2 minutes**

## Google Drive Setup (Optional)

### Get Credentials:
1. https://console.cloud.google.com/
2. Create project → Enable Drive API
3. Create OAuth 2.0 credentials
4. Download JSON

### Local:
```bash
mv ~/Downloads/credentials.json .
```

### Cloud (Streamlit):
- App Settings → Secrets
- Paste credentials JSON

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run financial_analysis_app.py

# Build Docker image
docker build -t financial-analysis .

# Run Docker container
docker run -p 8501:8501 financial-analysis

# Deploy helper
./deploy.sh
```

## URLs

- **Local:** http://localhost:8501
- **Streamlit Cloud:** https://YOUR-APP.streamlit.app
- **GitHub:** https://github.com/YOUR-USERNAME/financial-document-analysis

## Support

- **Full Docs:** README.md
- **Deployment:** DEPLOYMENT.md
- **Setup Summary:** SETUP_COMPLETE.md
