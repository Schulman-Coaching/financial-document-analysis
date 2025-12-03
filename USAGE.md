# Usage Instructions

## Installation

```bash
# Core dependencies
pip install pandas numpy streamlit

# For PDF parsing (optional)
pip install PyPDF2 pdf2image pytesseract
sudo apt-get install tesseract-ocr  # On Linux
# Or on macOS: brew install tesseract
```

## Running the Application

### Web App (Streamlit)
```bash
streamlit run financial_analysis_app.py
```

### Command-line Version
```bash
python financial_analyzer.py
```

## Features

- **Support Calculator**: Calculate NY child support (CSSA) and maintenance per DRL §240 and §236
- **Document Consistency**: Compare Net Worth Statements with tax returns
- **Hidden Income Detection**: Identify potential unreported income patterns
- **Full Analysis Report**: Generate comprehensive financial analysis reports
