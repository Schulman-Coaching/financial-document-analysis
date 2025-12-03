#!/usr/bin/env python3
"""
OCR Document Processing Module for Financial Document Analysis
Extracts text from PDFs, images, and scanned documents using Tesseract OCR
"""

import os
import re
import tempfile
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import io

# Image processing
from PIL import Image
import pytesseract

# PDF processing
from pdf2image import convert_from_path, convert_from_bytes
import PyPDF2


@dataclass
class OCRResult:
    """Result of OCR processing"""
    text: str
    confidence: float
    pages: int
    extracted_data: Dict
    warnings: List[str]
    processing_time: float


@dataclass
class ExtractedFinancialData:
    """Structured financial data extracted from documents"""
    document_type: str
    amounts: List[Dict[str, float]]
    dates: List[str]
    names: List[str]
    account_numbers: List[str]
    addresses: List[str]
    raw_text: str


class OCRProcessor:
    """Process documents using OCR and extract financial information"""

    # Regex patterns for financial data extraction
    PATTERNS = {
        'currency': r'\$[\d,]+\.?\d{0,2}',
        'date_mdy': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        'date_ymd': r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'ein': r'\b\d{2}-\d{7}\b',
        'account_number': r'\b(?:Account|Acct)\.?\s*#?\s*:?\s*(\d{4,})\b',
        'routing_number': r'\b(?:Routing|ABA)\.?\s*#?\s*:?\s*(\d{9})\b',
        'phone': r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'zip_code': r'\b\d{5}(?:-\d{4})?\b',
    }

    # Financial document keywords
    DOCUMENT_TYPES = {
        'tax_return': ['form 1040', 'internal revenue', 'irs', 'tax return',
                       'adjusted gross income', 'taxable income', 'w-2', 'schedule'],
        'bank_statement': ['bank statement', 'account summary', 'beginning balance',
                          'ending balance', 'deposits', 'withdrawals', 'available balance'],
        'net_worth': ['net worth statement', 'statement of net worth', 'assets',
                     'liabilities', 'monthly expenses', 'schedule a', 'schedule b'],
        'pay_stub': ['pay stub', 'earnings statement', 'gross pay', 'net pay',
                    'ytd', 'deductions', 'federal tax', 'state tax'],
        'brokerage': ['brokerage statement', 'investment account', 'portfolio',
                     'securities', 'stocks', 'bonds', 'mutual funds'],
        'retirement': ['401k', '403b', 'ira', 'pension', 'retirement account',
                      'vested balance', 'employer match'],
        'mortgage': ['mortgage statement', 'loan statement', 'principal balance',
                    'escrow', 'property tax', 'homeowner insurance'],
        'credit_card': ['credit card statement', 'minimum payment', 'credit limit',
                       'available credit', 'apr', 'finance charge']
    }

    def __init__(self, tesseract_cmd: str = None):
        """Initialize OCR processor"""
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        # Verify tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR not found: {e}")

    def process_file(self, file_path: str) -> OCRResult:
        """Process a file and extract text using OCR"""
        start_time = datetime.now()
        warnings = []

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.pdf':
            text, pages, confidence = self._process_pdf(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
            text, pages, confidence = self._process_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

        # Extract structured data
        extracted_data = self._extract_financial_data(text)

        processing_time = (datetime.now() - start_time).total_seconds()

        return OCRResult(
            text=text,
            confidence=confidence,
            pages=pages,
            extracted_data=extracted_data,
            warnings=warnings,
            processing_time=processing_time
        )

    def process_bytes(self, file_bytes: bytes, file_type: str) -> OCRResult:
        """Process file bytes and extract text using OCR"""
        start_time = datetime.now()
        warnings = []

        if file_type == 'pdf':
            text, pages, confidence = self._process_pdf_bytes(file_bytes)
        elif file_type in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']:
            text, pages, confidence = self._process_image_bytes(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Extract structured data
        extracted_data = self._extract_financial_data(text)

        processing_time = (datetime.now() - start_time).total_seconds()

        return OCRResult(
            text=text,
            confidence=confidence,
            pages=pages,
            extracted_data=extracted_data,
            warnings=warnings,
            processing_time=processing_time
        )

    def _process_pdf(self, file_path: str) -> Tuple[str, int, float]:
        """Process a PDF file"""
        text_parts = []
        total_confidence = 0
        page_count = 0

        # First try to extract text directly (for text-based PDFs)
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                page_count = len(reader.pages)

                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text and len(page_text.strip()) > 50:
                        text_parts.append(page_text)
        except Exception:
            pass

        # If direct extraction failed or got little text, use OCR
        if len(''.join(text_parts).strip()) < 100:
            text_parts = []
            try:
                images = convert_from_path(file_path, dpi=300)
                page_count = len(images)

                for img in images:
                    # Get OCR data with confidence
                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

                    page_text = pytesseract.image_to_string(img)
                    text_parts.append(page_text)

                    # Calculate confidence
                    confidences = [int(c) for c in data['conf'] if c != '-1']
                    if confidences:
                        total_confidence += sum(confidences) / len(confidences)

            except Exception as e:
                raise RuntimeError(f"Error processing PDF with OCR: {e}")
        else:
            # Text was extracted directly, assume high confidence
            total_confidence = 95 * page_count

        avg_confidence = total_confidence / page_count if page_count > 0 else 0

        return '\n\n'.join(text_parts), page_count, avg_confidence

    def _process_pdf_bytes(self, file_bytes: bytes) -> Tuple[str, int, float]:
        """Process PDF from bytes"""
        text_parts = []
        total_confidence = 0
        page_count = 0

        # First try direct text extraction
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text and len(page_text.strip()) > 50:
                    text_parts.append(page_text)
        except Exception:
            pass

        # If direct extraction failed, use OCR
        if len(''.join(text_parts).strip()) < 100:
            text_parts = []
            try:
                images = convert_from_bytes(file_bytes, dpi=300)
                page_count = len(images)

                for img in images:
                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                    page_text = pytesseract.image_to_string(img)
                    text_parts.append(page_text)

                    confidences = [int(c) for c in data['conf'] if c != '-1']
                    if confidences:
                        total_confidence += sum(confidences) / len(confidences)

            except Exception as e:
                raise RuntimeError(f"Error processing PDF with OCR: {e}")
        else:
            total_confidence = 95 * page_count

        avg_confidence = total_confidence / page_count if page_count > 0 else 0

        return '\n\n'.join(text_parts), page_count, avg_confidence

    def _process_image(self, file_path: str) -> Tuple[str, int, float]:
        """Process an image file"""
        img = Image.open(file_path)

        # Preprocess image for better OCR
        img = self._preprocess_image(img)

        # Get OCR data with confidence
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(img)

        # Calculate confidence
        confidences = [int(c) for c in data['conf'] if c != '-1']
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return text, 1, avg_confidence

    def _process_image_bytes(self, file_bytes: bytes) -> Tuple[str, int, float]:
        """Process image from bytes"""
        img = Image.open(io.BytesIO(file_bytes))

        # Preprocess image for better OCR
        img = self._preprocess_image(img)

        # Get OCR data with confidence
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(img)

        # Calculate confidence
        confidences = [int(c) for c in data['conf'] if c != '-1']
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return text, 1, avg_confidence

    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert to grayscale
        img = img.convert('L')

        # Increase contrast and size for better OCR
        # Simple thresholding
        img = img.point(lambda x: 0 if x < 140 else 255)

        return img

    def _extract_financial_data(self, text: str) -> Dict:
        """Extract structured financial data from text"""
        data = {
            'document_type': self._detect_document_type(text),
            'amounts': self._extract_amounts(text),
            'dates': self._extract_dates(text),
            'account_numbers': self._extract_pattern(text, 'account_number'),
            'ssn_detected': bool(re.search(self.PATTERNS['ssn'], text)),
            'ein_detected': bool(re.search(self.PATTERNS['ein'], text)),
            'emails': self._extract_pattern(text, 'email'),
            'phone_numbers': self._extract_pattern(text, 'phone'),
            'key_values': self._extract_key_value_pairs(text)
        }

        return data

    def _detect_document_type(self, text: str) -> str:
        """Detect the type of financial document"""
        text_lower = text.lower()

        scores = {}
        for doc_type, keywords in self.DOCUMENT_TYPES.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[doc_type] = score

        if scores:
            return max(scores, key=scores.get)

        return 'unknown'

    def _extract_amounts(self, text: str) -> List[Dict]:
        """Extract currency amounts from text"""
        amounts = []

        # Find all currency patterns
        matches = re.finditer(self.PATTERNS['currency'], text)

        for match in matches:
            amount_str = match.group()
            # Clean and convert to float
            amount_value = float(amount_str.replace('$', '').replace(',', ''))

            # Get surrounding context (30 chars before and after)
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end].strip()

            amounts.append({
                'value': amount_value,
                'formatted': amount_str,
                'context': context
            })

        return amounts

    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        dates = []

        # MDY format
        mdy_matches = re.findall(self.PATTERNS['date_mdy'], text)
        dates.extend(mdy_matches)

        # YMD format
        ymd_matches = re.findall(self.PATTERNS['date_ymd'], text)
        dates.extend(ymd_matches)

        return list(set(dates))

    def _extract_pattern(self, text: str, pattern_name: str) -> List[str]:
        """Extract matches for a named pattern"""
        pattern = self.PATTERNS.get(pattern_name)
        if not pattern:
            return []

        matches = re.findall(pattern, text)
        return list(set(matches))

    def _extract_key_value_pairs(self, text: str) -> Dict[str, str]:
        """Extract key-value pairs from text"""
        pairs = {}

        # Common financial document patterns
        kv_patterns = [
            r'(Gross Pay|Gross Income|Total Income)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Net Pay|Net Income)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Total Assets)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Total Liabilities)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Beginning Balance)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Ending Balance)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Adjusted Gross Income)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Taxable Income)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Federal Tax)[:\s]+\$?([\d,]+\.?\d*)',
            r'(State Tax)[:\s]+\$?([\d,]+\.?\d*)',
            r'(Account Number|Acct #)[:\s]+(\d+)',
            r'(Period|Statement Date)[:\s]+([\d/\-]+)',
        ]

        for pattern in kv_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                pairs[key] = value

        return pairs


def create_ocr_processor() -> OCRProcessor:
    """Factory function to create OCR processor"""
    return OCRProcessor()
