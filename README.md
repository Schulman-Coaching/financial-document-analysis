# Financial Document Analysis - NY Family Law

A comprehensive Streamlit application for analyzing financial documents in New York family law cases, with integrated Google Drive document management.

## Features

### 📊 Financial Analysis
- **Support Calculator**: Calculate child support and maintenance per NY law (DRL §240, §236)
- **Document Consistency Analysis**: Cross-reference net worth statements, tax returns, and bank statements
- **Hidden Income Detection**: Identify patterns suggesting unreported income
- **Comprehensive Reports**: Generate detailed financial analysis reports

### 📁 Google Drive Integration
- **Case Management**: Create organized folder structures for each case
- **Document Upload**: Upload and categorize financial documents
- **Search & Retrieval**: Search documents across all cases
- **Metadata Tracking**: Track document versions, confidentiality, and relationships

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/financial-document-analysis.git
   cd financial-document-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run financial_analysis_app.py
   ```

4. **Access the app:**
   Open your browser to `http://localhost:8501`

## Google Drive Setup (Optional)

The Google Drive integration is optional. The app works fully without it for financial analysis.

### Prerequisites
- Google Cloud account
- Google Drive API enabled

### Setup Steps

1. **Create Google Cloud Project:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project: "Financial Document Analysis"

2. **Enable Google Drive API:**
   - Navigate to: APIs & Services > Library
   - Search for "Google Drive API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials:**
   - Go to: APIs & Services > Credentials
   - Click "Create Credentials" > OAuth 2.0 Client ID
   - Application type: **Desktop app** (for local) or **Web application** (for cloud)
   - Download credentials JSON file

4. **Configure Credentials:**
   
   **For Local Development:**
   - Save downloaded file as `credentials.json` in project root
   - Run the app and click "Connect" in Google Drive Manager
   - Authorize in browser when prompted

   **For Cloud Deployment:**
   - Add credentials to Streamlit secrets (see Deployment section)

## Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/financial-document-analysis.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Repository: `financial-document-analysis`
   - Main file: `financial_analysis_app.py`
   - Click "Deploy"

3. **Configure Secrets (Optional - for Google Drive):**
   - In app settings, click "Secrets"
   - Add Google credentials:
   ```toml
   [google]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@project.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   ```

### Docker Deployment

```bash
# Build image
docker build -t financial-analysis .

# Run container
docker run -p 8501:8501 financial-analysis
```

### Other Platforms

See `DEPLOYMENT.md` for detailed instructions on:
- Heroku
- Google Cloud Run
- AWS EC2
- Azure App Service

## Usage

### Support Calculator

1. Select "Support Calculator" from sidebar
2. Enter payer and payee income information
3. Configure child support parameters
4. Click "Calculate Support"
5. Review detailed calculations and breakdowns

### Document Consistency Analysis

1. Select "Document Consistency" from sidebar
2. Upload or enter financial data
3. Click "Analyze Consistency"
4. Review discrepancies and red flags

### Google Drive Manager

1. Select "📁 Google Drive Manager" from sidebar
2. Click "Connect" to authenticate
3. Create cases with organized folder structures
4. Upload documents with metadata
5. Search and retrieve documents

## Project Structure

```
financial-document-analysis/
├── financial_analysis_app.py    # Main Streamlit application
├── financial_analyzer.py        # Core financial analysis logic
├── drive_manager.py             # Google Drive integration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── DEPLOYMENT.md               # Detailed deployment guide
├── USAGE.md                    # User guide
└── README.md                   # This file
```

## NY Law References

- **DRL §240(1-b)**: Child Support Standards Act (CSSA)
- **DRL §236**: Maintenance (Spousal Support)
- **Uniform Rule 202.16(b)**: Net Worth Statements

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit credentials:**
   - `credentials.json` and `token.json` are in `.gitignore`
   - Use environment variables or secrets management

2. **Data Privacy:**
   - All financial data is processed locally or in your cloud instance
   - No data is sent to third parties
   - Google Drive data stays in your Google account

3. **Access Control:**
   - Implement user authentication for production use
   - Restrict access to authorized personnel only
   - Use HTTPS for all deployments

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
- Create an issue on GitHub
- Check `DEPLOYMENT.md` for deployment help
- Review `USAGE.md` for usage examples

## Disclaimer

This tool is for informational purposes only and does not constitute legal advice. Always consult with a qualified attorney for legal matters.

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Author:** Elie Schulman
