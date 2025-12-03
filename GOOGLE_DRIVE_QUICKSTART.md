# 🎯 Google Drive Setup - Quick Start Guide

## Choose Your Path

### 🏠 Path 1: Local Development (Start Here - Easiest!)
**Best for:** Testing on your computer first
**Time:** 10 minutes
**Result:** Works on http://localhost:8501

### ☁️ Path 2: Streamlit Cloud (After Local Works)
**Best for:** Production deployment
**Time:** 5 minutes (after local setup)
**Result:** Works on your deployed app

---

# 🏠 LOCAL SETUP (Recommended First)

## Step-by-Step Checklist

### ✅ Step 1: Open Google Cloud Console
- [ ] Go to: https://console.cloud.google.com/
- [ ] Sign in with your Google account
- [ ] You should see the Google Cloud dashboard

### ✅ Step 2: Create Project
- [ ] Click project dropdown (top left, says "Select a project")
- [ ] Click "NEW PROJECT"
- [ ] Name: `Financial Document Analysis`
- [ ] Click "CREATE"
- [ ] Wait 30 seconds
- [ ] Select your new project from the dropdown

### ✅ Step 3: Enable Google Drive API
- [ ] Click hamburger menu (☰) → APIs & Services → Library
- [ ] Search: `Google Drive API`
- [ ] Click on it
- [ ] Click "ENABLE"
- [ ] Wait for it to enable

### ✅ Step 4: Configure OAuth Consent
- [ ] Go to: APIs & Services → OAuth consent screen
- [ ] User Type: **External**
- [ ] Click "CREATE"

**Fill in the form:**
- [ ] App name: `Financial Document Analysis`
- [ ] User support email: Your email
- [ ] Developer contact: Your email
- [ ] Click "SAVE AND CONTINUE"

**Scopes:**
- [ ] Click "ADD OR REMOVE SCOPES"
- [ ] Search: `drive`
- [ ] Check: `.../auth/drive` and `.../auth/drive.file`
- [ ] Click "UPDATE"
- [ ] Click "SAVE AND CONTINUE"

**Test Users:**
- [ ] Click "ADD USERS"
- [ ] Add your email
- [ ] Click "ADD"
- [ ] Click "SAVE AND CONTINUE"
- [ ] Click "BACK TO DASHBOARD"

### ✅ Step 5: Create OAuth Credentials
- [ ] Go to: APIs & Services → Credentials
- [ ] Click "+ CREATE CREDENTIALS"
- [ ] Select "OAuth client ID"
- [ ] Application type: **Desktop app**
- [ ] Name: `Financial Analysis Desktop`
- [ ] Click "CREATE"

### ✅ Step 6: Download Credentials
- [ ] Click "DOWNLOAD JSON" in the popup
- [ ] File saves to Downloads folder

### ✅ Step 7: Move Credentials to Project
Open Terminal and run:
```bash
cd /Users/elieschulman/financial-document-analysis
mv ~/Downloads/client_secret_*.json credentials.json
ls -la credentials.json
```

You should see: `credentials.json` listed

### ✅ Step 8: Test in Your App
- [ ] Open http://localhost:8501 (should already be running)
- [ ] Click "📁 Google Drive Manager" in sidebar
- [ ] Click "🔌 Connect"
- [ ] Browser opens → Sign in
- [ ] Click "Allow" (may show warning - click "Continue")
- [ ] See "✅ Connected to Google Drive!"

### ✅ Step 9: Create Test Case
- [ ] Go to "Create Case" tab
- [ ] Fill in:
  - Case ID: `TEST-2024-001`
  - Client Name: `Test Client`
  - Case Type: `Divorce`
  - Jurisdiction: `Test County`
- [ ] Click "Create Case Folder"
- [ ] See success message

### ✅ Step 10: Verify in Google Drive
- [ ] Open https://drive.google.com
- [ ] Look for folder: `Family Law Practice`
- [ ] Inside: `1_Case Files` → `TEST-2024-001 - Test Client`

**🎉 SUCCESS! Local setup complete!**

---

# ☁️ STREAMLIT CLOUD SETUP

## Prerequisites
- ✅ Local setup working
- ✅ App deployed to Streamlit Cloud

## Quick Steps

### Option A: Use OAuth (Same as Local)
1. Upload `credentials.json` to Streamlit secrets
2. Format as TOML (see GOOGLE_DRIVE_SETUP.md)

### Option B: Use Service Account (Recommended)

#### Step 1: Create Service Account
- [ ] Go to: https://console.cloud.google.com/
- [ ] IAM & Admin → Service Accounts
- [ ] Click "CREATE SERVICE ACCOUNT"
- [ ] Name: `financial-analysis-service`
- [ ] Click "CREATE AND CONTINUE" → "CONTINUE" → "DONE"

#### Step 2: Create Key
- [ ] Find your service account
- [ ] Click three dots (⋮) → "Manage keys"
- [ ] "ADD KEY" → "Create new key"
- [ ] Type: **JSON**
- [ ] Click "CREATE"
- [ ] JSON file downloads

#### Step 3: Share Drive Folder
- [ ] Open the JSON file
- [ ] Copy the `client_email` (looks like: `xxx@xxx.iam.gserviceaccount.com`)
- [ ] Go to Google Drive
- [ ] Right-click "Family Law Practice" folder → Share
- [ ] Paste the email
- [ ] Give "Editor" access
- [ ] Uncheck "Notify"
- [ ] Click "Share"

#### Step 4: Add to Streamlit Secrets
- [ ] Go to: https://share.streamlit.io
- [ ] Your app → Settings → Secrets
- [ ] Copy contents of JSON file
- [ ] Format as TOML (see GOOGLE_DRIVE_SETUP.md for exact format)
- [ ] Click "Save"
- [ ] App restarts automatically

#### Step 5: Test
- [ ] Open your deployed app
- [ ] Go to Google Drive Manager
- [ ] Click "Connect"
- [ ] Should see "✅ Connected!"

---

# 🆘 Quick Troubleshooting

## "credentials.json not found"
**Fix:** Make sure file is in `/Users/elieschulman/financial-document-analysis/`

## "Authentication failed"
**Fix:** 
1. Delete `token.json` if it exists
2. Try connecting again
3. Make sure you clicked "Allow"

## "Google hasn't verified this app"
**Fix:** This is normal! Click "Advanced" → "Go to Financial Document Analysis (unsafe)"

## Works locally but not on cloud
**Fix:** Use service account instead of OAuth for cloud deployment

---

# 📊 What You Get

Once connected, you can:

✅ **Create Case Folders**
- Automatic folder structure
- Organized by case ID
- Standard subfolders (Pleadings, Financial, Discovery, etc.)

✅ **Upload Documents**
- Net worth statements
- Tax returns
- Bank statements
- Court filings
- Evidence

✅ **Search & Retrieve**
- Search across all cases
- Filter by type, date, case
- Quick access to any document

✅ **Track Metadata**
- Document versions
- Confidentiality flags
- Upload dates
- Related documents

---

# 🎯 Current Status

**Your app is ready for Google Drive!**

The integration code is already in your app. You just need to:
1. Set up Google Cloud credentials (10 min)
2. Connect in the app (1 click)
3. Start using it!

---

# 📞 Need More Help?

**Detailed Guide:** See `GOOGLE_DRIVE_SETUP.md`

**Quick Commands:**
```bash
# Check if credentials exist
ls -la credentials.json

# Run app locally
streamlit run financial_analysis_app.py

# Open Google Cloud Console
open https://console.cloud.google.com/

# Open Google Drive
open https://drive.google.com/
```

---

**Ready to set up? Follow the checklist above! ✅**
