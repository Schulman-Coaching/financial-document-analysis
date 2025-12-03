# 📁 Google Drive Integration - Complete Setup Guide

## Overview

This guide will help you set up Google Drive integration for your Financial Document Analysis app. This allows you to:
- Create organized case folders in Google Drive
- Upload and categorize financial documents
- Search and retrieve documents across all cases
- Track document metadata and versions

---

## 🎯 Two Setup Options

### Option A: Local Development (Easiest to Start)
Best for testing and development on your computer

### Option B: Streamlit Cloud (For Production)
Best for deployed app accessible from anywhere

**Recommendation:** Start with Option A to test, then move to Option B for production.

---

## 📋 Prerequisites

You'll need:
- A Google account
- Access to Google Cloud Console
- 10-15 minutes for setup

---

# Option A: Local Development Setup

## Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Open: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project:**
   - Click the project dropdown (top left, next to "Google Cloud")
   - Click "NEW PROJECT"
   - Project name: `Financial Document Analysis`
   - Organization: Leave as default (or select your org)
   - Click "CREATE"
   - Wait for project creation (takes ~30 seconds)

3. **Select Your Project:**
   - Click the project dropdown again
   - Select "Financial Document Analysis"

## Step 2: Enable Google Drive API

1. **Navigate to APIs & Services:**
   - Click the hamburger menu (☰) in top left
   - Go to: **APIs & Services** → **Library**

2. **Enable Google Drive API:**
   - In the search box, type: `Google Drive API`
   - Click on "Google Drive API"
   - Click the blue **"ENABLE"** button
   - Wait for it to enable (~10 seconds)

## Step 3: Create OAuth 2.0 Credentials

1. **Go to Credentials:**
   - Click hamburger menu (☰)
   - Go to: **APIs & Services** → **Credentials**

2. **Configure OAuth Consent Screen (First Time Only):**
   - Click **"CONFIGURE CONSENT SCREEN"**
   - User Type: Select **"External"**
   - Click **"CREATE"**
   
   **App Information:**
   - App name: `Financial Document Analysis`
   - User support email: Your email address
   - Developer contact: Your email address
   - Click **"SAVE AND CONTINUE"**
   
   **Scopes:**
   - Click **"ADD OR REMOVE SCOPES"**
   - Search for: `drive`
   - Check these scopes:
     - `.../auth/drive` (See, edit, create, and delete all Google Drive files)
     - `.../auth/drive.file` (See, edit, create, and delete only files you open)
   - Click **"UPDATE"**
   - Click **"SAVE AND CONTINUE"**
   
   **Test Users:**
   - Click **"ADD USERS"**
   - Add your email address
   - Click **"ADD"**
   - Click **"SAVE AND CONTINUE"**
   
   **Summary:**
   - Review and click **"BACK TO DASHBOARD"**

3. **Create OAuth Client ID:**
   - Go back to: **APIs & Services** → **Credentials**
   - Click **"+ CREATE CREDENTIALS"** (top)
   - Select **"OAuth client ID"**
   
   **Application type:**
   - Select: **"Desktop app"**
   - Name: `Financial Analysis Desktop Client`
   - Click **"CREATE"**

4. **Download Credentials:**
   - A popup appears with your Client ID and Secret
   - Click **"DOWNLOAD JSON"**
   - Save the file (it will be named something like `client_secret_XXX.json`)

## Step 4: Configure Your App

1. **Rename the Downloaded File:**
   ```bash
   cd /Users/elieschulman/financial-document-analysis
   mv ~/Downloads/client_secret_*.json credentials.json
   ```

2. **Verify the File:**
   ```bash
   ls -la credentials.json
   ```
   
   You should see the file listed.

## Step 5: Test the Integration

1. **Open Your Local App:**
   - Your app should already be running at http://localhost:8501
   - If not, run: `streamlit run financial_analysis_app.py`

2. **Connect to Google Drive:**
   - In the sidebar, select **"📁 Google Drive Manager"**
   - Click the **"🔌 Connect"** button
   - A browser window will open asking you to sign in
   - Sign in with your Google account
   - Click **"Allow"** to grant permissions
   - You may see a warning "Google hasn't verified this app" - click **"Continue"** (it's your app!)

3. **Verify Connection:**
   - You should see "✅ Connected to Google Drive!"
   - The app will create a folder structure in your Google Drive
   - Check your Google Drive - you should see a folder called "Family Law Practice"

## Step 6: Test Creating a Case

1. **In the "Create Case" tab:**
   - Case ID: `TEST-2024-001`
   - Client Name: `Test Client`
   - Case Type: `Divorce`
   - Jurisdiction: `Test County`
   - Click **"Create Case Folder"**

2. **Verify in Google Drive:**
   - Open Google Drive in your browser
   - Navigate to: `Family Law Practice` → `1_Case Files`
   - You should see: `TEST-2024-001 - Test Client` folder

**Success!** Your local Google Drive integration is working! 🎉

---

# Option B: Streamlit Cloud Setup

## Prerequisites
- Completed deployment to Streamlit Cloud
- Your app is live at: `https://your-app.streamlit.app`

## Step 1: Create Service Account (Recommended for Cloud)

For cloud deployment, we'll use a Service Account instead of OAuth:

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com/
   - Select your "Financial Document Analysis" project

2. **Create Service Account:**
   - Go to: **IAM & Admin** → **Service Accounts**
   - Click **"+ CREATE SERVICE ACCOUNT"**
   
   **Service account details:**
   - Name: `financial-analysis-service`
   - Description: `Service account for Financial Document Analysis app`
   - Click **"CREATE AND CONTINUE"**
   
   **Grant access:**
   - Role: Skip this (click "CONTINUE")
   
   **Grant users access:**
   - Skip this (click "DONE")

3. **Create Key:**
   - Find your new service account in the list
   - Click the three dots (⋮) on the right
   - Select **"Manage keys"**
   - Click **"ADD KEY"** → **"Create new key"**
   - Key type: **JSON**
   - Click **"CREATE"**
   - A JSON file will download automatically

4. **Enable Drive API for Service Account:**
   - The Drive API should already be enabled from earlier
   - If not, go to **APIs & Services** → **Library** → Enable "Google Drive API"

## Step 2: Share Drive Folder with Service Account

1. **Find Service Account Email:**
   - Open the downloaded JSON file
   - Look for `"client_email"` - it looks like:
     `financial-analysis-service@your-project.iam.gserviceaccount.com`
   - Copy this email address

2. **Share Your Drive Folder:**
   - Open Google Drive
   - Find or create the "Family Law Practice" folder
   - Right-click → **"Share"**
   - Paste the service account email
   - Give it **"Editor"** access
   - Uncheck "Notify people"
   - Click **"Share"**

## Step 3: Add Credentials to Streamlit Cloud

1. **Go to Streamlit Cloud Dashboard:**
   - https://share.streamlit.io
   - Find your app
   - Click the three dots (⋮) → **"Settings"**

2. **Add Secrets:**
   - In the left sidebar, click **"Secrets"**
   - You'll see a text editor

3. **Format Your Secrets:**
   - Open the downloaded service account JSON file
   - Copy its contents
   - In Streamlit Secrets, paste in this format:

   ```toml
   # Google Drive Service Account Credentials
   [google]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nYour-Full-Private-Key-Here\n-----END PRIVATE KEY-----\n"
   client_email = "financial-analysis-service@your-project.iam.gserviceaccount.com"
   client_id = "123456789012345678901"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
   universe_domain = "googleapis.com"
   ```

   **Important Notes:**
   - Replace all values with those from your JSON file
   - Keep the private_key exactly as is, including `\n` characters
   - Make sure there are no extra quotes or formatting issues

4. **Save:**
   - Click **"Save"**
   - Your app will automatically restart

## Step 4: Update Code for Service Account (Optional)

The current code is designed for OAuth. For service accounts, you may need to update `drive_manager.py`. However, let's test first with the current setup.

## Step 5: Test on Streamlit Cloud

1. **Open Your Deployed App:**
   - Go to: `https://your-app.streamlit.app`

2. **Navigate to Google Drive Manager:**
   - Select "📁 Google Drive Manager" from sidebar
   - Click "Connect"

3. **Verify:**
   - Should show "✅ Connected to Google Drive!"
   - Try creating a test case

---

# 🔧 Troubleshooting

## Common Issues

### "credentials.json not found"
**Solution:**
- For local: Make sure `credentials.json` is in the project root
- For cloud: Check that secrets are properly formatted in Streamlit Cloud

### "Authentication failed"
**Solution:**
- Delete `token.json` and try again
- Make sure you clicked "Allow" in the OAuth consent screen
- Check that Drive API is enabled

### "Permission denied" when creating folders
**Solution:**
- For service account: Make sure you shared the Drive folder with the service account email
- Check that the service account has "Editor" permissions

### "Google hasn't verified this app"
**Solution:**
- This is normal for personal projects
- Click "Advanced" → "Go to [app name] (unsafe)"
- This warning only appears because you haven't submitted for Google verification (not needed for personal use)

### App works locally but not on Streamlit Cloud
**Solution:**
- Service accounts work better for cloud deployment
- Make sure secrets are properly formatted (check for extra quotes, missing newlines)
- Check Streamlit Cloud logs for specific errors

---

# 📊 What You Can Do Now

Once Google Drive is connected:

### 1. Create Case Folders
- Organized structure for each case
- Automatic subfolder creation
- Metadata tracking

### 2. Upload Documents
- Financial documents (net worth, tax returns, bank statements)
- Legal documents (pleadings, motions, orders)
- Evidence (emails, photos, messages)
- Automatic categorization

### 3. Search Documents
- Search across all cases
- Filter by case, type, date
- Quick retrieval

### 4. Generate Reports
- Case document summaries
- Missing document checks
- Document statistics

---

# 🔒 Security Best Practices

1. **Never Commit Credentials:**
   - `credentials.json` is in `.gitignore`
   - Never share your service account JSON file

2. **Use Service Accounts for Production:**
   - More secure than OAuth for server applications
   - No user interaction needed
   - Better for automated processes

3. **Limit Permissions:**
   - Only grant necessary Drive scopes
   - Use separate service accounts for different apps

4. **Regular Audits:**
   - Review service account access periodically
   - Remove unused credentials

---

# 📞 Need Help?

**Google Cloud Issues:**
- Google Cloud Console Help: https://cloud.google.com/support
- Drive API Docs: https://developers.google.com/drive

**App Issues:**
- Check app logs in Streamlit Cloud
- Review `drive_manager.py` code
- Test locally first before deploying

---

# ✅ Quick Checklist

## For Local Development:
- [ ] Created Google Cloud project
- [ ] Enabled Google Drive API
- [ ] Created OAuth credentials
- [ ] Downloaded credentials.json
- [ ] Placed credentials.json in project root
- [ ] Connected in app
- [ ] Tested creating a case

## For Streamlit Cloud:
- [ ] Created service account
- [ ] Downloaded service account JSON
- [ ] Shared Drive folder with service account
- [ ] Added secrets to Streamlit Cloud
- [ ] Tested connection on deployed app

---

**You're all set! Your Google Drive integration is ready to use! 🎉**
