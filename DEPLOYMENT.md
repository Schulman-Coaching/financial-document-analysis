# Financial Document Analysis - Deployment Guide

## Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Financial Document Analysis"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/financial-document-analysis.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `financial-document-analysis`
   - Main file path: `financial_analysis_app.py`
   - Click "Deploy"

3. **Configure Secrets (for Google Drive):**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add your Google credentials as TOML:
   ```toml
   [google]
   credentials_json = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     ...
   }
   '''
   ```

### Option 2: Heroku

1. **Create Procfile:**
   ```
   web: streamlit run financial_analysis_app.py --server.port=$PORT
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Google Cloud Run

1. **Create Dockerfile** (see Dockerfile in repo)
2. **Build and Deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/financial-analysis
   gcloud run deploy --image gcr.io/PROJECT_ID/financial-analysis --platform managed
   ```

### Option 4: AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04)
2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```
3. **Run with systemd service** (see systemd service file)

## Google Drive Integration Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Financial Document Analysis"
3. Enable Google Drive API:
   - APIs & Services > Library
   - Search "Google Drive API"
   - Click Enable

### Step 2: Create OAuth Credentials

1. APIs & Services > Credentials
2. Create Credentials > OAuth 2.0 Client ID
3. Application type: **Web application** (for cloud deployment)
4. Authorized redirect URIs:
   - For Streamlit Cloud: `https://YOUR-APP.streamlit.app`
   - For local: `http://localhost:8501`
5. Download credentials JSON

### Step 3: Configure OAuth Consent Screen

1. APIs & Services > OAuth consent screen
2. User Type: External
3. App information:
   - App name: "Financial Document Analysis"
   - User support email: your-email@domain.com
4. Scopes: Add Google Drive scopes
5. Test users: Add your email addresses

### Step 4: Set Up Secrets

**For Streamlit Cloud:**
- Add credentials in app settings > Secrets
- Use `st.secrets` to access in code

**For other platforms:**
- Use environment variables
- Store credentials securely (AWS Secrets Manager, etc.)

## Environment Variables

Create `.env` file (DO NOT commit to git):
```bash
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
GOOGLE_TOKEN_PATH=/path/to/token.json
```

## Security Considerations

1. **Never commit credentials to git**
   - Add to `.gitignore`: `credentials.json`, `token.json`, `.env`

2. **Use secrets management**
   - Streamlit Cloud: Built-in secrets
   - AWS: Secrets Manager
   - GCP: Secret Manager
   - Heroku: Config Vars

3. **Implement authentication**
   - Add user login (streamlit-authenticator)
   - Restrict access to authorized users

4. **Data encryption**
   - Encrypt sensitive data at rest
   - Use HTTPS for all connections

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All calculations work correctly
- [ ] Google Drive integration functional (if configured)
- [ ] Secrets properly configured
- [ ] HTTPS enabled
- [ ] Error logging set up
- [ ] Backup strategy in place
- [ ] User authentication enabled (if needed)

## Monitoring & Maintenance

- Monitor app performance in Streamlit Cloud dashboard
- Check logs regularly for errors
- Update dependencies monthly
- Review Google API quotas

## Support

For issues or questions:
- Check Streamlit docs: https://docs.streamlit.io
- Google Drive API: https://developers.google.com/drive
