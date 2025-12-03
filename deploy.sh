#!/bin/bash
# Quick deployment script for Financial Document Analysis

echo "================================================"
echo "Financial Document Analysis - Deployment Helper"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Commit
echo ""
read -p "Enter commit message (default: 'Initial commit'): " commit_msg
commit_msg=${commit_msg:-"Initial commit"}
git commit -m "$commit_msg"
echo "✅ Files committed"

# Ask for remote repository
echo ""
echo "🔗 GitHub Repository Setup"
read -p "Enter your GitHub username: " github_user
read -p "Enter repository name (default: financial-document-analysis): " repo_name
repo_name=${repo_name:-"financial-document-analysis"}

# Add remote
echo ""
echo "Adding remote repository..."
git remote add origin "https://github.com/$github_user/$repo_name.git" 2>/dev/null || \
git remote set-url origin "https://github.com/$github_user/$repo_name.git"

echo ""
echo "📤 Ready to push to GitHub!"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "   Repository name: $repo_name"
echo "   Keep it private if handling sensitive data"
echo ""
echo "2. Push your code:"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Streamlit Cloud:"
echo "   - Go to: https://share.streamlit.io"
echo "   - Sign in with GitHub"
echo "   - Click 'New app'"
echo "   - Select repository: $repo_name"
echo "   - Main file: financial_analysis_app.py"
echo "   - Click 'Deploy'"
echo ""
echo "4. (Optional) Configure Google Drive:"
echo "   - In Streamlit Cloud app settings"
echo "   - Add secrets (see DEPLOYMENT.md)"
echo ""
echo "================================================"
echo "For detailed instructions, see DEPLOYMENT.md"
echo "================================================"
