# file: financial_analysis_app.py
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from financial_analyzer import (
    SupportCalculatorNY,
    FinancialConsistencyAnalyzer,
    NetWorthStatement
)

# Optional Google Drive integration
try:
    from drive_manager import FamilyLawDriveManager, CaseMetadata, DocumentMetadata
    DRIVE_AVAILABLE = True
except ImportError:
    DRIVE_AVAILABLE = False

# Optional OCR integration
try:
    from ocr_processor import OCRProcessor, create_ocr_processor
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def main():
    st.set_page_config(
        page_title="Financial Document Analysis",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 NY Family Law Financial Document Analysis")
    st.markdown("Analyze Net Worth Statements, Tax Returns, and Calculate Support")
    st.markdown("---")

    # Initialize session state
    if 'support_calculator' not in st.session_state:
        st.session_state.support_calculator = SupportCalculatorNY()
    if 'consistency_analyzer' not in st.session_state:
        st.session_state.consistency_analyzer = FinancialConsistencyAnalyzer()

    # Sidebar for navigation
    with st.sidebar:
        st.header("Analysis Modules")
        
        # Build module list
        modules = ["Support Calculator", "Document Consistency",
                  "Hidden Income Detection", "Full Analysis Report"]

        if OCR_AVAILABLE:
            modules.append("🔍 OCR Document Scanner")

        if DRIVE_AVAILABLE:
            modules.append("📁 Google Drive Manager")
        
        module = st.radio("Select Analysis:", modules)

        st.markdown("---")
        st.info("**NY Law References:**\n"
                "- DRL §240(1-b): Child Support\n"
                "- DRL §236: Maintenance\n"
                "- Uniform Rule 202.16(b): Net Worth Statements")
        
        if OCR_AVAILABLE:
            st.markdown("---")
            st.success("✅ OCR Document Recognition Available")

        if DRIVE_AVAILABLE:
            st.markdown("---")
            st.success("✅ Google Drive Integration Available")

    if module == "Support Calculator":
        st.header("NY Support Calculations")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Payer Information")
            payer_income = st.number_input(
                "Payer Annual Income ($)",
                min_value=0.0,
                value=185000.0,
                step=1000.0
            )
            payer_bonus = st.number_input(
                "Payer Bonus/Commission ($)",
                min_value=0.0,
                value=25000.0,
                step=1000.0
            )

        with col2:
            st.subheader("Payee Information")
            payee_income = st.number_input(
                "Payee Annual Income ($)",
                min_value=0.0,
                value=65000.0,
                step=1000.0
            )
            marriage_years = st.slider(
                "Years of Marriage",
                min_value=0,
                max_value=50,
                value=12
            )

        st.subheader("Child Support Parameters")
        col3, col4, col5 = st.columns(3)

        with col3:
            num_children = st.selectbox(
                "Number of Children",
                options=[1, 2, 3, 4, 5],
                index=1
            )
            special_needs = st.checkbox("Special Needs Children")

        with col4:
            health_insurance = st.number_input(
                "Annual Health Insurance ($)",
                min_value=0.0,
                value=6000.0,
                step=500.0
            )
            childcare = st.number_input(
                "Annual Childcare ($)",
                min_value=0.0,
                value=12000.0,
                step=1000.0
            )

        with col5:
            education = st.number_input(
                "Annual Education ($)",
                min_value=0.0,
                value=8000.0,
                step=1000.0
            )
            pendente_lite = st.checkbox("Pendente Lite Calculation")

        if st.button("Calculate Support", type="primary"):
            with st.spinner("Calculating..."):
                # Child Support
                child_support = st.session_state.support_calculator.calculate_child_support(
                    payer_income=payer_income + payer_bonus,
                    payee_income=payee_income,
                    num_children=num_children,
                    special_needs=special_needs,
                    health_insurance_cost=health_insurance,
                    childcare_cost=childcare,
                    education_cost=education
                )

                # Maintenance
                maintenance = st.session_state.support_calculator.calculate_maintenance(
                    payer_income=payer_income + payer_bonus,
                    payee_income=payee_income,
                    duration_years=marriage_years,
                    pendente_lite=pendente_lite
                )

                # Display results
                st.success("Calculations Complete!")

                # Create tabs for results
                tab1, tab2 = st.tabs(["Child Support", "Maintenance"])

                with tab1:
                    st.subheader("Child Support Calculation")

                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "Monthly Obligation",
                            f"${child_support['total_obligation']/12:,.2f}",
                            f"{child_support['cssa_percentage']:.1%} CSSA rate"
                        )
                    with col2:
                        st.metric(
                            "Annual Total",
                            f"${child_support['total_obligation']:,.2f}"
                        )
                    with col3:
                        st.metric(
                            "Payer Share",
                            f"{child_support['payer_income_share']}%"
                        )

                    # Detailed breakdown
                    with st.expander("Detailed Calculation"):
                        st.write("**Income Analysis:**")
                        st.write(f"- Payer Income: ${payer_income + payer_bonus:,.2f}")
                        st.write(f"- Payee Income: ${payee_income:,.2f}")
                        st.write(f"- Combined Income: ${child_support['combined_parental_income']:,.2f}")

                        st.write("\n**Support Components:**")
                        st.write(f"- Basic Support: ${child_support['basic_support_amount']:,.2f}")
                        st.write(f"- Add-ons: ${sum(child_support['add_ons'].values()):,.2f}")
                        for addon, amount in child_support['add_ons'].items():
                            if amount > 0:
                                st.write(f"  • {addon.replace('_', ' ').title()}: ${amount:,.2f}")

                with tab2:
                    st.subheader("Maintenance Calculation")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "Monthly Amount",
                            f"${maintenance['maintenance_amount']/12:,.2f}",
                            f"{maintenance['duration']}"
                        )
                    with col2:
                        income_cap_status = "Applied" if maintenance['income_cap_applied'] else "Not Applied"
                        st.metric(
                            "Income Cap",
                            income_cap_status,
                            f"${st.session_state.support_calculator.maintenance_cap:,.0f}"
                        )
                    with col3:
                        st.metric(
                            "Formula",
                            maintenance['calculation_method'],
                            maintenance['formula_used']
                        )

    elif module == "Document Consistency":
        st.header("Document Consistency Analysis")

        st.subheader("Upload Financial Documents")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Net Worth Statement**")
            nw_assets = st.text_area(
                "Assets (JSON format)",
                value='{"Checking": 15000, "Savings": 45000, "401k": 280000}',
                height=100
            )
            nw_income = st.text_area(
                "Income Sources (JSON format)",
                value='{"Salary": 185000, "Bonus": 25000}',
                height=100
            )

        with col2:
            st.write("**Tax Return Data**")
            tax_wages = st.number_input(
                "W-2 Income ($)",
                min_value=0.0,
                value=185000.0
            )
            tax_business = st.number_input(
                "Business Income ($)",
                min_value=0.0,
                value=45000.0
            )
            tax_other = st.number_input(
                "Other Income ($)",
                min_value=0.0,
                value=5000.0
            )

        if st.button("Analyze Consistency", type="primary"):
            try:
                # Parse inputs
                assets = json.loads(nw_assets)
                income_sources = json.loads(nw_income)

                # Create sample net worth
                net_worth = NetWorthStatement(
                    party_name="Sample Client",
                    preparation_date=datetime.now().strftime("%Y-%m-%d"),
                    assets=assets,
                    liabilities={},
                    income_sources=income_sources,
                    expenses={},
                    marital_property_flag={},
                    separate_property_flag={}
                )

                # Create tax analysis
                tax_analysis = {
                    'income_sources': {
                        'wages': tax_wages,
                        'business_income': tax_business,
                        'other_income': tax_other
                    }
                }

                # Perform analysis
                analysis = st.session_state.consistency_analyzer._compare_income_sources(
                    net_worth, tax_analysis, []
                )

                # Display results
                st.subheader("Consistency Analysis Results")

                if analysis['discrepancies']:
                    st.warning(f"Found {len(analysis['discrepancies'])} discrepancies")

                    for disc in analysis['discrepancies']:
                        with st.expander(f"{disc['type']}"):
                            st.write(f"**Source 1:** {disc.get('source1', 'N/A')}")
                            st.write(f"**Source 2:** {disc.get('source2', 'N/A')}")
                            st.write(f"**Variance:** {disc.get('variance', 'N/A')}")
                            st.write(f"**Explanation:** {disc.get('explanation', 'N/A')}")
                else:
                    st.success("No significant discrepancies found")

            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check your input.")

    elif module == "Hidden Income Detection":
        st.header("Hidden Income Detection")

        st.info("""
        This module analyzes financial patterns to identify potential hidden income:
        - Regular deposits not matching reported income
        - Large cash withdrawals
        - Transfers to unknown accounts
        - Lifestyle exceeding reported means
        """)

        # Sample analysis
        st.subheader("Sample Detection Analysis")

        with st.expander("Common Hidden Income Indicators"):
            st.write("""
            **1. Cash Business Indicators:**
            - Regular large cash deposits
            - Business with high cash transactions
            - Inconsistent revenue reporting

            **2. Asset Hiding Indicators:**
            - Transfers to family members
            - Offshore account transfers
            - Cryptocurrency purchases

            **3. Underreporting Indicators:**
            - Lifestyle exceeds reported income
            - Business expenses disproportionate to income
            - Multiple bank accounts not disclosed
            """)

        # Upload transaction data
        st.subheader("Upload Transaction Data")
        uploaded_file = st.file_uploader(
            "Upload CSV with transactions",
            type=['csv'],
            help="CSV should have columns: Date, Description, Amount"
        )

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(f"Loaded {len(df)} transactions")
            st.dataframe(df.head())

    elif module == "Full Analysis Report":
        st.header("Comprehensive Financial Analysis Report")

        st.write("Generate a complete financial analysis report including:")
        st.write("- Support calculations")
        st.write("- Document consistency analysis")
        st.write("- Hidden income indicators")
        st.write("- Legal recommendations")

        if st.button("Generate Sample Report", type="primary"):
            with st.spinner("Generating report..."):
                # This would integrate all modules
                st.info("Full integration of all modules would go here")

                # Sample report sections
                report_sections = [
                    "1. Executive Summary",
                    "2. Support Calculations",
                    "3. Asset Analysis",
                    "4. Income Consistency",
                    "5. Expense Analysis",
                    "6. Hidden Income Indicators",
                    "7. Legal Recommendations",
                    "8. Next Steps"
                ]

                for section in report_sections:
                    with st.expander(section):
                        st.write(f"Detailed analysis for {section} would appear here.")

                # Download button for report
                sample_report = "\n".join(report_sections)
                st.download_button(
                    label="📥 Download Report Template",
                    data=sample_report,
                    file_name="financial_analysis_report.txt",
                    mime="text/plain"
                )

    elif module == "🔍 OCR Document Scanner":
        st.header("OCR Document Recognition")

        if not OCR_AVAILABLE:
            st.error("OCR module not available. Please install required packages.")
            return

        st.info("""
        **Upload scanned documents or images to extract text and financial data.**

        Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP

        The scanner will automatically:
        - Extract all text from the document
        - Identify the document type (tax return, bank statement, etc.)
        - Extract financial amounts with context
        - Find dates, account numbers, and key values
        """)

        # Initialize OCR processor
        if 'ocr_processor' not in st.session_state:
            try:
                st.session_state.ocr_processor = create_ocr_processor()
            except Exception as e:
                st.error(f"Failed to initialize OCR: {e}")
                st.info("Make sure Tesseract is installed: `brew install tesseract`")
                return

        # File upload
        uploaded_file = st.file_uploader(
            "Upload document for OCR",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'],
            help="Upload a scanned document or image to extract text"
        )

        if uploaded_file is not None:
            st.write(f"**File:** {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

            col1, col2 = st.columns([1, 3])

            with col1:
                process_btn = st.button("🔍 Process Document", type="primary")

            if process_btn:
                with st.spinner("Processing document with OCR..."):
                    try:
                        # Get file type
                        file_ext = uploaded_file.name.split('.')[-1].lower()

                        # Process the file
                        result = st.session_state.ocr_processor.process_bytes(
                            uploaded_file.read(),
                            file_ext
                        )

                        # Store result in session
                        st.session_state.ocr_result = result

                        st.success(f"✅ Processed {result.pages} page(s) in {result.processing_time:.2f}s")

                    except Exception as e:
                        st.error(f"Error processing document: {e}")

            # Display results if available
            if 'ocr_result' in st.session_state and st.session_state.ocr_result:
                result = st.session_state.ocr_result

                # Results tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📄 Extracted Text",
                    "💰 Financial Data",
                    "📊 Key Values",
                    "ℹ️ Document Info"
                ])

                with tab1:
                    st.subheader("Extracted Text")
                    st.text_area(
                        "Full Text",
                        result.text,
                        height=400,
                        help="Raw text extracted from the document"
                    )

                    # Download button
                    st.download_button(
                        "📥 Download Text",
                        result.text,
                        file_name=f"{uploaded_file.name}_extracted.txt",
                        mime="text/plain"
                    )

                with tab2:
                    st.subheader("Extracted Financial Amounts")

                    amounts = result.extracted_data.get('amounts', [])

                    if amounts:
                        st.write(f"Found **{len(amounts)}** currency amounts:")

                        # Create dataframe for amounts
                        amounts_df = pd.DataFrame(amounts)
                        amounts_df = amounts_df.sort_values('value', ascending=False)

                        st.dataframe(
                            amounts_df,
                            column_config={
                                "value": st.column_config.NumberColumn(
                                    "Amount",
                                    format="$%.2f"
                                ),
                                "formatted": "Original",
                                "context": "Context"
                            },
                            use_container_width=True
                        )

                        # Summary statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total", f"${sum(a['value'] for a in amounts):,.2f}")
                        with col2:
                            st.metric("Largest", f"${max(a['value'] for a in amounts):,.2f}")
                        with col3:
                            st.metric("Count", len(amounts))
                    else:
                        st.info("No currency amounts detected in the document.")

                    # Dates
                    st.subheader("Dates Found")
                    dates = result.extracted_data.get('dates', [])
                    if dates:
                        st.write(", ".join(dates))
                    else:
                        st.info("No dates detected.")

                with tab3:
                    st.subheader("Key-Value Pairs")

                    key_values = result.extracted_data.get('key_values', {})

                    if key_values:
                        for key, value in key_values.items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.info("No key-value pairs automatically extracted.")

                    # Account numbers (if found)
                    accounts = result.extracted_data.get('account_numbers', [])
                    if accounts:
                        st.subheader("Account Numbers")
                        for acc in accounts:
                            st.code(acc)

                    # Sensitive data warnings
                    if result.extracted_data.get('ssn_detected'):
                        st.warning("⚠️ SSN pattern detected in document")

                    if result.extracted_data.get('ein_detected'):
                        st.warning("⚠️ EIN pattern detected in document")

                with tab4:
                    st.subheader("Document Information")

                    col1, col2 = st.columns(2)

                    with col1:
                        doc_type = result.extracted_data.get('document_type', 'unknown')
                        doc_type_display = doc_type.replace('_', ' ').title()

                        st.metric("Detected Type", doc_type_display)
                        st.metric("Pages", result.pages)
                        st.metric("Processing Time", f"{result.processing_time:.2f}s")

                    with col2:
                        st.metric("OCR Confidence", f"{result.confidence:.1f}%")
                        st.metric("Text Length", f"{len(result.text):,} chars")

                        emails = result.extracted_data.get('emails', [])
                        phones = result.extracted_data.get('phone_numbers', [])
                        st.metric("Emails Found", len(emails))
                        st.metric("Phone Numbers", len(phones))

                    if result.warnings:
                        st.subheader("Warnings")
                        for warning in result.warnings:
                            st.warning(warning)

                    # Export data as JSON
                    st.subheader("Export Data")
                    export_data = {
                        'document_type': result.extracted_data.get('document_type'),
                        'amounts': result.extracted_data.get('amounts', []),
                        'dates': result.extracted_data.get('dates', []),
                        'key_values': result.extracted_data.get('key_values', {}),
                        'confidence': result.confidence,
                        'pages': result.pages
                    }

                    st.download_button(
                        "📥 Download Extracted Data (JSON)",
                        json.dumps(export_data, indent=2),
                        file_name=f"{uploaded_file.name}_data.json",
                        mime="application/json"
                    )

    elif module == "📁 Google Drive Manager":
        st.header("Google Drive Document Manager")
        
        if not DRIVE_AVAILABLE:
            st.error("Google Drive integration not available. Please install required packages.")
            return
        
        # Initialize Drive Manager in session state
        if 'drive_manager' not in st.session_state:
            st.session_state.drive_manager = None
        
        # Check for credentials
        has_credentials = os.path.exists('credentials.json') or 'google' in st.secrets
        
        if not has_credentials:
            st.warning("⚠️ Google Drive credentials not configured")
            
            with st.expander("📖 Setup Instructions"):
                st.markdown("""
                ### Google Drive API Setup
                
                1. **Create Google Cloud Project:**
                   - Go to [Google Cloud Console](https://console.cloud.google.com/)
                   - Create a new project
                
                2. **Enable Google Drive API:**
                   - Navigate to APIs & Services > Library
                   - Search for "Google Drive API"
                   - Click "Enable"
                
                3. **Create OAuth Credentials:**
                   - Go to APIs & Services > Credentials
                   - Create OAuth 2.0 Client ID
                   - Application type: Web application
                   - Download credentials as JSON
                
                4. **Configure Credentials:**
                   - For local: Save as `credentials.json` in project directory
                   - For cloud: Add to Streamlit secrets
                
                For detailed instructions, see `DEPLOYMENT.md`
                """)
        else:
            # Authentication section
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Drive Connection")
            
            with col2:
                if st.button("🔌 Connect"):
                    with st.spinner("Authenticating..."):
                        try:
                            drive_manager = FamilyLawDriveManager()
                            if drive_manager.authenticate():
                                drive_manager.initialize_drive_structure()
                                drive_manager._load_document_index()
                                st.session_state.drive_manager = drive_manager
                                st.success("✅ Connected to Google Drive!")
                            else:
                                st.error("Authentication failed")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            if st.session_state.drive_manager:
                st.success("✅ Google Drive Connected")
                
                # Tabs for different operations
                tab1, tab2, tab3 = st.tabs(["Create Case", "Upload Documents", "Search Documents"])
                
                with tab1:
                    st.subheader("Create New Case")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        case_id = st.text_input("Case ID*", placeholder="FL-2024-001")
                        client_name = st.text_input("Client Name*", placeholder="Jane Doe")
                        case_type = st.selectbox(
                            "Case Type*",
                            ["Divorce", "Divorce with Children", "Child Custody", 
                             "Child Support", "Maintenance", "Modification"]
                        )
                    
                    with col2:
                        opposing_party = st.text_input("Opposing Party", placeholder="John Doe")
                        jurisdiction = st.text_input("Jurisdiction*", placeholder="Kings County")
                        attorney = st.text_input("Attorney Assigned", placeholder="Robert Johnson, Esq.")
                    
                    if st.button("Create Case Folder", type="primary"):
                        if case_id and client_name and jurisdiction:
                            with st.spinner("Creating case folder..."):
                                case_metadata = CaseMetadata(
                                    case_id=case_id,
                                    client_name=client_name,
                                    opposing_party=opposing_party,
                                    case_type=case_type,
                                    jurisdiction=jurisdiction,
                                    filing_date=datetime.now().strftime("%Y-%m-%d"),
                                    status="Active",
                                    attorney_assigned=attorney,
                                    paralegal_assigned="",
                                    tags=[case_type.lower()]
                                )
                                
                                folder_id = st.session_state.drive_manager.create_case_folder(case_metadata)
                                
                                if folder_id:
                                    st.success(f"✅ Created case folder for {case_id}")
                                else:
                                    st.error("Failed to create case folder")
                        else:
                            st.warning("Please fill in all required fields (*)")
                
                with tab2:
                    st.subheader("Upload Document")
                    
                    # Get list of cases
                    cases = list(st.session_state.drive_manager.case_index.keys())
                    
                    if not cases:
                        st.info("No cases found. Create a case first.")
                    else:
                        selected_case = st.selectbox("Select Case", cases)
                        
                        uploaded_file = st.file_uploader(
                            "Choose file",
                            type=['pdf', 'docx', 'doc', 'txt', 'xlsx', 'jpg', 'png']
                        )
                        
                        doc_type = st.selectbox(
                            "Document Type",
                            ["net_worth", "tax_return", "bank_statement", "pay_stub",
                             "complaint", "answer", "motion", "letter", "email", "other"]
                        )
                        
                        description = st.text_area("Description (optional)")
                        confidential = st.checkbox("Mark as Confidential")
                        
                        if uploaded_file and st.button("Upload to Drive", type="primary"):
                            with st.spinner("Uploading..."):
                                # Save temp file
                                temp_path = f"/tmp/{uploaded_file.name}"
                                with open(temp_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                
                                # Upload to Drive
                                metadata = st.session_state.drive_manager.upload_document(
                                    file_path=temp_path,
                                    case_id=selected_case,
                                    document_type=doc_type,
                                    description=description,
                                    confidential=confidential
                                )
                                
                                # Clean up
                                os.remove(temp_path)
                                
                                if metadata:
                                    st.success(f"✅ Uploaded: {metadata.document_name}")
                                else:
                                    st.error("Upload failed")
                
                with tab3:
                    st.subheader("Search Documents")
                    
                    search_query = st.text_input("Search", placeholder="Enter keywords...")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        filter_case = st.selectbox(
                            "Filter by Case",
                            ["All Cases"] + list(st.session_state.drive_manager.case_index.keys())
                        )
                    
                    with col2:
                        filter_type = st.selectbox(
                            "Filter by Type",
                            ["All Types", "net_worth", "tax_return", "bank_statement", 
                             "pay_stub", "complaint", "motion", "letter"]
                        )
                    
                    if st.button("Search"):
                        case_filter = None if filter_case == "All Cases" else filter_case
                        type_filter = None if filter_type == "All Types" else filter_type
                        
                        results = st.session_state.drive_manager.search_documents(
                            query=search_query or "",
                            case_id=case_filter,
                            document_type=type_filter
                        )
                        
                        st.write(f"Found {len(results)} documents")
                        
                        for doc in results:
                            with st.expander(f"📄 {doc.document_name}"):
                                st.write(f"**Case:** {doc.case_id}")
                                st.write(f"**Type:** {doc.document_type}")
                                st.write(f"**Uploaded:** {doc.created_date}")
                                st.write(f"**Description:** {doc.description}")
                                if doc.confidential:
                                    st.warning("🔒 Confidential")

if __name__ == "__main__":
    main()

