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

# Firm configuration and report generation
try:
    from firm_config import FirmConfig, get_default_config, NASSAU_COUNTY_CONFIG, CASE_TYPES
    from report_generator import ReportGenerator, create_report_generator
    FIRM_CONFIG_AVAILABLE = True
except ImportError:
    FIRM_CONFIG_AVAILABLE = False

# Document templates
try:
    from document_templates import DocumentTemplates, create_document_templates, PartyInfo, ChildInfo
    TEMPLATES_AVAILABLE = True
except ImportError:
    TEMPLATES_AVAILABLE = False

# ROI Calculator
try:
    from roi_calculator import ROICalculator, create_roi_calculator, TimeTracker, create_time_tracker
    ROI_AVAILABLE = True
except ImportError:
    ROI_AVAILABLE = False

# Case Manager
try:
    from case_manager import CaseManager, create_case_manager, CaseStatus, CaseType, DeadlineType, TaskPriority
    CASE_MANAGER_AVAILABLE = True
except ImportError:
    CASE_MANAGER_AVAILABLE = False


def main():
    # Load firm configuration
    if FIRM_CONFIG_AVAILABLE:
        firm_config = get_default_config()
        report_gen = create_report_generator(firm_config)
    else:
        firm_config = None
        report_gen = None

    if TEMPLATES_AVAILABLE:
        doc_templates = create_document_templates(firm_config)
    else:
        doc_templates = None

    st.set_page_config(
        page_title=f"Financial Analysis | {firm_config.firm_name if firm_config else 'Family Law'}",
        page_icon="⚖️",
        layout="wide"
    )

    # Header with firm branding
    if firm_config:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(f"⚖️ {firm_config.firm_name}")
            st.markdown(f"*{firm_config.firm_tagline}*")
        with col2:
            st.markdown(f"**📞 {firm_config.phone}**")
            st.markdown(f"📍 {firm_config.primary_jurisdiction}")
    else:
        st.title("💰 NY Family Law Financial Document Analysis")
        st.markdown("Analyze Net Worth Statements, Tax Returns, and Calculate Support")

    st.markdown("---")

    # Initialize session state
    if 'support_calculator' not in st.session_state:
        st.session_state.support_calculator = SupportCalculatorNY()
    if 'consistency_analyzer' not in st.session_state:
        st.session_state.consistency_analyzer = FinancialConsistencyAnalyzer()

    # Sidebar for navigation - Organized by Client Lifecycle
    with st.sidebar:
        st.header("📋 Client Lifecycle")

        # Build module groups by lifecycle stage
        lifecycle_stages = {}

        # Stage 1: Intake & Engagement
        lifecycle_stages["1️⃣ INTAKE"] = ["📋 Case Intake"]
        if TEMPLATES_AVAILABLE:
            lifecycle_stages["1️⃣ INTAKE"].extend([
                "📜 Engagement Letter",
                "✉️ Welcome Letter"
            ])

        # Stage 2: Correspondence
        if TEMPLATES_AVAILABLE:
            lifecycle_stages["2️⃣ CORRESPONDENCE"] = [
                "📨 Demand Letter",
                "📧 Letter to Counsel"
            ]

        # Stage 3: Pleadings & Filings
        if TEMPLATES_AVAILABLE:
            lifecycle_stages["3️⃣ PLEADINGS"] = [
                "📑 Summons with Notice",
                "📝 Verified Complaint",
                "⚖️ Notice of Appearance"
            ]

        # Stage 4: Financial Analysis
        lifecycle_stages["4️⃣ FINANCIAL"] = [
            "📊 Support Calculator",
            "💰 Net Worth Statement",
            "👶 Child Support Worksheet",
            "🔎 Document Consistency",
            "🕵️ Hidden Income Detection"
        ]

        # Stage 5: Settlement & Trial
        if TEMPLATES_AVAILABLE:
            lifecycle_stages["5️⃣ RESOLUTION"] = [
                "🤝 Settlement Agreement",
                "🛡️ Order of Protection"
            ]

        # Stage 6: Tools & Management
        lifecycle_stages["6️⃣ TOOLS"] = ["📄 Full Analysis Report"]
        if OCR_AVAILABLE:
            lifecycle_stages["6️⃣ TOOLS"].append("🔍 OCR Scanner")
        if DRIVE_AVAILABLE:
            lifecycle_stages["6️⃣ TOOLS"].append("📁 Google Drive")
        if CASE_MANAGER_AVAILABLE:
            lifecycle_stages["6️⃣ TOOLS"].append("📂 Case Management")
        if ROI_AVAILABLE:
            lifecycle_stages["6️⃣ TOOLS"].extend(["📈 ROI Dashboard", "🎯 Sales Demo"])
        lifecycle_stages["6️⃣ TOOLS"].append("⚙️ Settings")

        # Create expandable sections for each stage
        all_modules = []
        for stage, modules in lifecycle_stages.items():
            with st.expander(stage, expanded=(stage == "1️⃣ INTAKE")):
                for mod in modules:
                    all_modules.append(mod)
                    st.write(f"  {mod}")

        st.markdown("---")
        module = st.selectbox("Quick Select:", all_modules)

        st.markdown("---")
        st.info("**Client Workflow:**\n"
                "1. Intake → Engagement\n"
                "2. Correspondence\n"
                "3. Pleadings & Filings\n"
                "4. Financial Analysis\n"
                "5. Settlement/Trial\n"
                "6. Resolution")

        # Status indicators
        st.markdown("---")
        st.caption("**System Status**")
        status_cols = st.columns(2)
        with status_cols[0]:
            if TEMPLATES_AVAILABLE:
                st.success("✅ Templates")
            if OCR_AVAILABLE:
                st.success("✅ OCR")
        with status_cols[1]:
            if CASE_MANAGER_AVAILABLE:
                st.success("✅ Cases")
            if ROI_AVAILABLE:
                st.success("✅ ROI")

    if module == "📊 Support Calculator":
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

    elif module == "📋 Case Intake":
        st.header("New Case Intake")

        if not FIRM_CONFIG_AVAILABLE:
            st.warning("Firm configuration not available.")

        # Case Type Selection
        st.subheader("Case Information")

        col1, col2 = st.columns(2)

        with col1:
            case_type = st.selectbox(
                "Case Type",
                list(CASE_TYPES.keys()) if FIRM_CONFIG_AVAILABLE else [
                    "contested_divorce", "uncontested_divorce", "custody_modification",
                    "child_support", "domestic_violence"
                ],
                format_func=lambda x: CASE_TYPES.get(x, {}).get('name', x.replace('_', ' ').title()) if FIRM_CONFIG_AVAILABLE else x.replace('_', ' ').title()
            )

            case_id = st.text_input("Case/Matter ID", placeholder="2024-FL-001")

        with col2:
            court = st.selectbox(
                "Court",
                firm_config.courts if firm_config else [
                    "Nassau County Supreme Court",
                    "Nassau County Family Court",
                    "Queens County Supreme Court"
                ]
            )
            intake_date = st.date_input("Intake Date", datetime.now())

        # Domestic Violence Alert
        if case_type == "domestic_violence":
            st.error("""
            ⚠️ **DOMESTIC VIOLENCE CASE - SAFETY PROTOCOLS**

            - Ensure client safety before proceeding
            - Verify confidential contact information
            - Consider Address Confidentiality Program
            - Check for existing Orders of Protection
            - Assess immediate safety needs
            """)

            safety_assessed = st.checkbox("✅ Safety assessment completed")
            if not safety_assessed:
                st.warning("Please complete safety assessment before proceeding.")

        st.markdown("---")

        # Client Information
        st.subheader("Client Information")

        col1, col2 = st.columns(2)

        with col1:
            client_name = st.text_input("Client Full Name*")
            client_dob = st.date_input("Date of Birth", min_value=datetime(1940, 1, 1))
            client_phone = st.text_input("Phone Number*")
            client_email = st.text_input("Email Address")

        with col2:
            client_address = st.text_area("Current Address", height=100)
            client_employer = st.text_input("Employer")
            client_income = st.number_input("Annual Income ($)", min_value=0.0, step=1000.0)

        st.markdown("---")

        # Opposing Party Information
        st.subheader("Opposing Party Information")

        col1, col2 = st.columns(2)

        with col1:
            opposing_name = st.text_input("Opposing Party Name")
            opposing_dob = st.date_input("Opposing Party DOB", min_value=datetime(1940, 1, 1), key="opp_dob")
            opposing_phone = st.text_input("Opposing Party Phone (if known)")

        with col2:
            opposing_address = st.text_area("Opposing Party Address (if known)", height=100)
            opposing_employer = st.text_input("Opposing Party Employer (if known)")
            opposing_income = st.number_input("Opposing Party Income (estimated)", min_value=0.0, step=1000.0)
            opposing_attorney = st.text_input("Opposing Attorney (if known)")

        st.markdown("---")

        # Marriage/Relationship Information
        st.subheader("Marriage Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            marriage_date = st.date_input("Date of Marriage", min_value=datetime(1950, 1, 1))

        with col2:
            separation_date = st.date_input("Date of Separation", min_value=datetime(1950, 1, 1), key="sep_date")

        with col3:
            marriage_years = (separation_date - marriage_date).days // 365 if separation_date > marriage_date else 0
            st.metric("Length of Marriage", f"{marriage_years} years")

        grounds = st.selectbox(
            "Grounds for Divorce",
            ["Irretrievable Breakdown (No-Fault)", "Cruel and Inhuman Treatment",
             "Abandonment", "Imprisonment", "Adultery", "Living Apart (Separation Agreement)",
             "Living Apart (Judgment of Separation)"]
        )

        st.markdown("---")

        # Children Information
        st.subheader("Children")

        has_children = st.checkbox("Minor children involved")

        children_data = []
        if has_children:
            num_children = st.number_input("Number of Minor Children", min_value=1, max_value=10, value=1)

            for i in range(int(num_children)):
                with st.expander(f"Child {i + 1}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        child_name = st.text_input(f"Name", key=f"child_name_{i}")
                        child_dob = st.date_input(f"Date of Birth", key=f"child_dob_{i}")
                    with col2:
                        child_residence = st.selectbox(
                            f"Currently Resides With",
                            ["Client", "Opposing Party", "Shared/Alternating", "Other"],
                            key=f"child_res_{i}"
                        )
                        child_special = st.checkbox(f"Special Needs", key=f"child_special_{i}")

                    children_data.append({
                        "name": child_name,
                        "dob": str(child_dob),
                        "residence": child_residence,
                        "special_needs": child_special
                    })

        st.markdown("---")

        # Financial Overview
        st.subheader("Financial Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Assets**")
            residence_value = st.number_input("Marital Residence Value ($)", min_value=0.0, step=10000.0)
            retirement_value = st.number_input("Retirement Accounts ($)", min_value=0.0, step=1000.0)
            bank_accounts = st.number_input("Bank Accounts ($)", min_value=0.0, step=1000.0)
            other_assets = st.number_input("Other Assets ($)", min_value=0.0, step=1000.0)

        with col2:
            st.write("**Liabilities**")
            mortgage = st.number_input("Mortgage Balance ($)", min_value=0.0, step=1000.0)
            credit_cards = st.number_input("Credit Card Debt ($)", min_value=0.0, step=100.0)
            other_debt = st.number_input("Other Debt ($)", min_value=0.0, step=100.0)

        total_assets = residence_value + retirement_value + bank_accounts + other_assets
        total_liabilities = mortgage + credit_cards + other_debt
        net_worth = total_assets - total_liabilities

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assets", f"${total_assets:,.2f}")
        with col2:
            st.metric("Total Liabilities", f"${total_liabilities:,.2f}")
        with col3:
            st.metric("Estimated Net Worth", f"${net_worth:,.2f}",
                     delta=f"${net_worth:,.2f}" if net_worth > 0 else None)

        st.markdown("---")

        # Generate Intake Summary
        if st.button("📄 Generate Intake Summary", type="primary"):
            if client_name:
                client_info = {
                    "name": client_name,
                    "dob": str(client_dob),
                    "phone": client_phone,
                    "email": client_email,
                    "address": client_address,
                    "employer": client_employer,
                    "opposing_name": opposing_name,
                    "opposing_dob": str(opposing_dob),
                    "opposing_address": opposing_address,
                    "opposing_employer": opposing_employer,
                    "opposing_attorney": opposing_attorney,
                    "marriage_date": str(marriage_date),
                    "separation_date": str(separation_date),
                    "marriage_years": marriage_years
                }

                financial_overview = {
                    "client_income": client_income,
                    "opposing_income": opposing_income,
                    "residence_value": residence_value,
                    "retirement": retirement_value,
                    "bank_accounts": bank_accounts,
                    "other_assets": other_assets,
                    "mortgage": mortgage,
                    "credit_cards": credit_cards,
                    "other_debt": other_debt
                }

                if report_gen:
                    report = report_gen.generate_case_intake_summary(
                        client_info=client_info,
                        case_type=CASE_TYPES.get(case_type, {}).get('name', case_type),
                        financial_overview=financial_overview,
                        children_info=children_data if has_children else None,
                        domestic_violence=(case_type == "domestic_violence")
                    )

                    st.success("✅ Intake Summary Generated!")

                    st.text_area("Intake Summary", report, height=400)

                    st.download_button(
                        "📥 Download Intake Summary",
                        report,
                        file_name=f"intake_{case_id or 'new'}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.info("Report generator not available.")
            else:
                st.warning("Please enter client name.")

    elif module == "🔎 Document Consistency":
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

    elif module == "🕵️ Hidden Income Detection":
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

    elif module == "📄 Full Analysis Report":
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

    elif module == "📝 Document Templates":
        st.header("Legal Document Templates")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
            return

        st.info("""
        **Generate professional legal documents based on official NY State court forms.**

        Available templates:
        - Net Worth Statement (DRL 236)
        - Verified Complaint for Divorce
        - Child Support Worksheet (CSSA)
        - Family Offense Petition (Order of Protection)
        - Stipulation of Settlement
        """)

        template_type = st.selectbox(
            "Select Document Template",
            ["Net Worth Statement", "Verified Complaint", "Child Support Worksheet",
             "Family Offense Petition", "Stipulation of Settlement"]
        )

        st.markdown("---")

        # Common party information
        st.subheader("Party Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Party 1 (Plaintiff/Petitioner)**")
            p1_name = st.text_input("Full Name*", key="p1_name")
            p1_address = st.text_input("Street Address", key="p1_addr")
            p1_city = st.text_input("City", value="Woodmere", key="p1_city")
            p1_state = st.text_input("State", value="NY", key="p1_state")
            p1_zip = st.text_input("ZIP", key="p1_zip")
            p1_phone = st.text_input("Phone", key="p1_phone")
            p1_dob = st.text_input("Date of Birth", key="p1_dob")
            p1_employer = st.text_input("Employer", key="p1_emp")

        with col2:
            st.write("**Party 2 (Defendant/Respondent)**")
            p2_name = st.text_input("Full Name*", key="p2_name")
            p2_address = st.text_input("Street Address", key="p2_addr")
            p2_city = st.text_input("City", key="p2_city")
            p2_state = st.text_input("State", value="NY", key="p2_state")
            p2_zip = st.text_input("ZIP", key="p2_zip")
            p2_phone = st.text_input("Phone", key="p2_phone")
            p2_dob = st.text_input("Date of Birth", key="p2_dob")
            p2_employer = st.text_input("Employer", key="p2_emp")

        st.markdown("---")

        # Case information
        st.subheader("Case Information")
        col1, col2 = st.columns(2)

        with col1:
            county = st.selectbox(
                "County",
                ["Nassau", "Queens", "Kings", "Suffolk", "New York", "Westchester", "Other"]
            )
            index_number = st.text_input("Index/Docket Number", placeholder="Leave blank if new case")

        with col2:
            marriage_date = st.text_input("Date of Marriage", placeholder="MM/DD/YYYY")
            separation_date = st.text_input("Date of Separation", placeholder="MM/DD/YYYY")

        # Template-specific inputs
        st.markdown("---")

        if template_type == "Net Worth Statement":
            st.subheader("Financial Information")
            st.info("Complete financial details will be added to the template for manual completion.")

            if st.button("📄 Generate Net Worth Statement", type="primary"):
                if p1_name and p2_name:
                    party1 = PartyInfo(
                        name=p1_name, address=p1_address, city=p1_city,
                        state=p1_state, zip_code=p1_zip, phone=p1_phone,
                        dob=p1_dob, employer=p1_employer
                    )
                    party2 = PartyInfo(
                        name=p2_name, address=p2_address, city=p2_city,
                        state=p2_state, zip_code=p2_zip, phone=p2_phone,
                        dob=p2_dob, employer=p2_employer
                    )

                    doc = doc_templates.generate_net_worth_statement(
                        party=party1, spouse=party2, county=county,
                        index_number=index_number or "_______________",
                        income_data={}, assets={}, liabilities={}, expenses={}
                    )

                    st.success("✅ Net Worth Statement Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Net Worth Statement",
                        doc,
                        file_name=f"net_worth_statement_{p1_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

        elif template_type == "Verified Complaint":
            st.subheader("Divorce Information")

            marriage_place = st.text_input("Place of Marriage (City, State)")

            grounds = st.selectbox(
                "Grounds for Divorce",
                ["Irretrievable Breakdown (DRL §170(7))", "Cruel and Inhuman Treatment",
                 "Abandonment", "Imprisonment", "Adultery"]
            )

            has_children = st.checkbox("Children of the marriage")
            children_data = []
            if has_children:
                num_children = st.number_input("Number of children", 1, 10, 1)
                for i in range(int(num_children)):
                    with st.expander(f"Child {i+1}"):
                        c_name = st.text_input("Name", key=f"vc_child_name_{i}")
                        c_dob = st.text_input("Date of Birth", key=f"vc_child_dob_{i}")
                        c_age = st.number_input("Age", 0, 21, key=f"vc_child_age_{i}")
                        c_res = st.selectbox("Resides with", ["Plaintiff", "Defendant", "Both"], key=f"vc_child_res_{i}")
                        children_data.append(ChildInfo(name=c_name, dob=c_dob, age=c_age, residence=c_res))

            if st.button("📄 Generate Verified Complaint", type="primary"):
                if p1_name and p2_name:
                    plaintiff = PartyInfo(
                        name=p1_name, address=p1_address, city=p1_city,
                        state=p1_state, zip_code=p1_zip, phone=p1_phone, dob=p1_dob
                    )
                    defendant = PartyInfo(
                        name=p2_name, address=p2_address, city=p2_city,
                        state=p2_state, zip_code=p2_zip, phone=p2_phone, dob=p2_dob
                    )

                    doc = doc_templates.generate_verified_complaint(
                        plaintiff=plaintiff, defendant=defendant, county=county,
                        marriage_date=marriage_date or "_______________",
                        marriage_place=marriage_place or "_______________",
                        separation_date=separation_date or "_______________",
                        children=children_data, grounds=grounds
                    )

                    st.success("✅ Verified Complaint Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Verified Complaint",
                        doc,
                        file_name=f"verified_complaint_{p1_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

        elif template_type == "Child Support Worksheet":
            st.subheader("Income & Child Information")

            col1, col2 = st.columns(2)
            with col1:
                custodial_income = st.number_input("Custodial Parent Income ($)", 0.0, step=1000.0)
            with col2:
                non_custodial_income = st.number_input("Non-Custodial Parent Income ($)", 0.0, step=1000.0)

            num_children = st.number_input("Number of Children", 1, 5, 1)
            children_data = []
            for i in range(int(num_children)):
                with st.expander(f"Child {i+1}"):
                    c_name = st.text_input("Name", key=f"cs_child_name_{i}")
                    c_dob = st.text_input("Date of Birth", key=f"cs_child_dob_{i}")
                    c_age = st.number_input("Age", 0, 21, key=f"cs_child_age_{i}")
                    children_data.append(ChildInfo(name=c_name, dob=c_dob, age=c_age, residence="Custodial Parent"))

            st.subheader("Add-On Expenses (Annual)")
            col1, col2, col3 = st.columns(3)
            with col1:
                childcare = st.number_input("Child Care ($)", 0.0, step=100.0)
            with col2:
                health_ins = st.number_input("Health Insurance ($)", 0.0, step=100.0)
            with col3:
                education = st.number_input("Education ($)", 0.0, step=100.0)

            if st.button("📄 Generate Child Support Worksheet", type="primary"):
                if p1_name and p2_name:
                    custodial = PartyInfo(
                        name=p1_name, address=p1_address, city=p1_city,
                        state=p1_state, zip_code=p1_zip, phone=p1_phone
                    )
                    non_custodial = PartyInfo(
                        name=p2_name, address=p2_address, city=p2_city,
                        state=p2_state, zip_code=p2_zip, phone=p2_phone
                    )

                    doc = doc_templates.generate_child_support_worksheet(
                        custodial_parent=custodial, non_custodial_parent=non_custodial,
                        county=county, children=children_data,
                        custodial_income=custodial_income, non_custodial_income=non_custodial_income,
                        childcare_cost=childcare, health_insurance=health_ins, education_cost=education
                    )

                    st.success("✅ Child Support Worksheet Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Child Support Worksheet",
                        doc,
                        file_name=f"child_support_worksheet_{p1_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

        elif template_type == "Family Offense Petition":
            st.subheader("Order of Protection Request")

            st.warning("⚠️ **DOMESTIC VIOLENCE SAFETY NOTICE**: If you are in immediate danger, call 911.")

            relationship = st.selectbox(
                "Relationship to Respondent",
                ["Currently Married", "Formerly Married", "Have Child in Common",
                 "Currently in Intimate Relationship", "Formerly in Intimate Relationship",
                 "Related by Blood", "Members of Same Household"]
            )

            st.subheader("Incidents")
            num_incidents = st.number_input("Number of Incidents to Report", 1, 5, 1)
            incidents = []
            for i in range(int(num_incidents)):
                with st.expander(f"Incident {i+1}"):
                    inc_date = st.text_input("Date", key=f"inc_date_{i}")
                    inc_time = st.text_input("Time", key=f"inc_time_{i}")
                    inc_location = st.text_input("Location", key=f"inc_loc_{i}")
                    inc_desc = st.text_area("Description", key=f"inc_desc_{i}")
                    inc_injuries = st.text_input("Injuries (if any)", key=f"inc_inj_{i}")
                    incidents.append({
                        "date": inc_date, "time": inc_time, "location": inc_location,
                        "description": inc_desc, "injuries": inc_injuries
                    })

            st.subheader("Relief Requested")
            relief = st.multiselect(
                "Select all that apply",
                ["Stay away from Petitioner", "Stay away from home",
                 "Stay away from workplace", "Stay away from children",
                 "Refrain from contacting Petitioner", "Surrender firearms",
                 "Refrain from committing family offenses"]
            )

            if st.button("📄 Generate Family Offense Petition", type="primary"):
                if p1_name and p2_name:
                    petitioner = PartyInfo(
                        name=p1_name, address=p1_address, city=p1_city,
                        state=p1_state, zip_code=p1_zip, phone=p1_phone, dob=p1_dob
                    )
                    respondent = PartyInfo(
                        name=p2_name, address=p2_address, city=p2_city,
                        state=p2_state, zip_code=p2_zip, phone=p2_phone, dob=p2_dob
                    )

                    doc = doc_templates.generate_family_offense_petition(
                        petitioner=petitioner, respondent=respondent, county=county,
                        relationship=relationship, incidents=incidents, relief_requested=relief
                    )

                    st.success("✅ Family Offense Petition Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Family Offense Petition",
                        doc,
                        file_name=f"family_offense_petition_{p1_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

        elif template_type == "Stipulation of Settlement":
            st.subheader("Settlement Terms")

            custody = st.selectbox(
                "Custody Arrangement",
                ["Joint Legal and Physical Custody", "Sole Custody to Plaintiff",
                 "Sole Custody to Defendant", "Joint Legal, Primary Physical to Plaintiff",
                 "Joint Legal, Primary Physical to Defendant"]
            )

            col1, col2 = st.columns(2)
            with col1:
                child_support = st.number_input("Monthly Child Support ($)", 0.0, step=100.0)
            with col2:
                maintenance = st.number_input("Monthly Maintenance ($)", 0.0, step=100.0)

            maintenance_duration = st.text_input("Maintenance Duration", placeholder="e.g., 5 years")

            has_children = st.checkbox("Children of the marriage", key="stip_children")
            children_data = []
            if has_children:
                num_children = st.number_input("Number of children", 1, 10, 1, key="stip_num_children")
                for i in range(int(num_children)):
                    with st.expander(f"Child {i+1}"):
                        c_name = st.text_input("Name", key=f"stip_child_name_{i}")
                        c_dob = st.text_input("Date of Birth", key=f"stip_child_dob_{i}")
                        c_age = st.number_input("Age", 0, 21, key=f"stip_child_age_{i}")
                        children_data.append(ChildInfo(name=c_name, dob=c_dob, age=c_age, residence=""))

            if st.button("📄 Generate Stipulation of Settlement", type="primary"):
                if p1_name and p2_name:
                    plaintiff = PartyInfo(
                        name=p1_name, address=p1_address, city=p1_city,
                        state=p1_state, zip_code=p1_zip, phone=p1_phone
                    )
                    defendant = PartyInfo(
                        name=p2_name, address=p2_address, city=p2_city,
                        state=p2_state, zip_code=p2_zip, phone=p2_phone
                    )

                    doc = doc_templates.generate_stipulation_of_settlement(
                        plaintiff=plaintiff, defendant=defendant, county=county,
                        index_number=index_number or "_______________",
                        marriage_date=marriage_date or "_______________",
                        children=children_data, custody_arrangement=custody,
                        child_support_monthly=child_support, maintenance_monthly=maintenance,
                        maintenance_duration=maintenance_duration or "_______________",
                        property_division={}
                    )

                    st.success("✅ Stipulation of Settlement Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Stipulation of Settlement",
                        doc,
                        file_name=f"stipulation_settlement_{p1_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

    # ========================================================================
    # LIFECYCLE STAGE 1: INTAKE & ENGAGEMENT
    # ========================================================================

    elif module == "📜 Engagement Letter":
        st.header("📜 Engagement Letter / Retainer Agreement")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a professional engagement letter that complies with 22 NYCRR Part 1215.**

            This document establishes the attorney-client relationship and outlines:
            - Scope of representation
            - Fee structure and retainer requirements
            - Client responsibilities
            - Terms of engagement
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Client Information")
                client_name = st.text_input("Client Full Name*", key="eng_client_name")
                client_address = st.text_input("Street Address*", key="eng_client_addr")
                client_city = st.text_input("City", value="Woodmere", key="eng_client_city")
                client_state = st.text_input("State", value="NY", key="eng_client_state")
                client_zip = st.text_input("ZIP Code", key="eng_client_zip")
                client_phone = st.text_input("Phone Number", key="eng_client_phone")
                client_email = st.text_input("Email Address", key="eng_client_email")

            with col2:
                st.subheader("Case & Fee Information")
                case_type = st.selectbox(
                    "Case Type*",
                    ["Contested Divorce", "Uncontested Divorce", "Child Custody",
                     "Child Support Modification", "Spousal Maintenance",
                     "Order of Protection", "Post-Judgment Enforcement"]
                )
                retainer_amount = st.number_input("Retainer Amount ($)", 2500.0, 25000.0, 5000.0, 500.0)
                hourly_rate = st.number_input("Partner Hourly Rate ($)", 250.0, 750.0, 450.0, 25.0)

            st.subheader("Scope of Representation")
            scope_options = st.multiselect(
                "Select all services included in this engagement:",
                [
                    "Negotiate and prepare a settlement agreement",
                    "Represent client in divorce proceedings",
                    "Represent client in custody/visitation matters",
                    "Represent client in child support proceedings",
                    "Represent client in spousal maintenance proceedings",
                    "Prepare and file all necessary court documents",
                    "Attend all court appearances",
                    "Conduct discovery and depositions",
                    "Prepare for and conduct trial if necessary",
                    "Negotiate and draft stipulation of settlement"
                ],
                default=["Represent client in divorce proceedings",
                        "Prepare and file all necessary court documents",
                        "Attend all court appearances"]
            )

            if st.button("📄 Generate Engagement Letter", type="primary"):
                if client_name and client_address:
                    client = PartyInfo(
                        name=client_name, address=client_address, city=client_city,
                        state=client_state, zip_code=client_zip, phone=client_phone,
                        email=client_email
                    )

                    doc = doc_templates.generate_engagement_letter(
                        client=client,
                        case_type=case_type,
                        retainer_amount=retainer_amount,
                        hourly_rate=hourly_rate,
                        scope_of_representation=scope_options
                    )

                    st.success("✅ Engagement Letter Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Engagement Letter",
                        doc,
                        file_name=f"engagement_letter_{client_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter client name and address.")

    elif module == "✉️ Welcome Letter":
        st.header("✉️ Initial Client Letter / Welcome Letter")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a welcome letter for new clients.**

            This letter provides:
            - Introduction to the legal team
            - Overview of the case and next steps
            - List of documents needed from the client
            - Important reminders and expectations
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Client Information")
                client_name = st.text_input("Client Full Name*", key="wel_client_name")
                client_address = st.text_input("Street Address*", key="wel_client_addr")
                client_city = st.text_input("City", value="Woodmere", key="wel_client_city")
                client_state = st.text_input("State", value="NY", key="wel_client_state")
                client_zip = st.text_input("ZIP Code", key="wel_client_zip")

            with col2:
                st.subheader("Case Information")
                case_type = st.selectbox(
                    "Case Type*",
                    ["Divorce", "Child Custody", "Child Support", "Spousal Maintenance",
                     "Order of Protection", "Post-Judgment Modification"],
                    key="wel_case_type"
                )

            st.subheader("Next Steps")
            next_steps = st.multiselect(
                "Select the next steps for this client:",
                [
                    "Complete and return the Client Intake Form",
                    "Gather and provide financial documents",
                    "Schedule follow-up meeting to discuss strategy",
                    "Prepare Statement of Net Worth",
                    "File Summons with Notice",
                    "Serve opposing party with court papers",
                    "Attend Preliminary Conference",
                    "Begin discovery process",
                    "Schedule court appearance"
                ],
                default=[
                    "Complete and return the Client Intake Form",
                    "Gather and provide financial documents",
                    "Schedule follow-up meeting to discuss strategy"
                ]
            )

            st.subheader("Documents Needed")
            docs_needed = st.multiselect(
                "Select documents to request from client:",
                [
                    "Last 3 years of tax returns (complete with all schedules)",
                    "Last 3 months of pay stubs",
                    "Last 12 months of bank statements (all accounts)",
                    "Last 12 months of credit card statements",
                    "Retirement account statements (401k, IRA, pension)",
                    "Mortgage statement and deed",
                    "Vehicle titles and loan statements",
                    "Life insurance policies",
                    "Health insurance information",
                    "Marriage certificate",
                    "Birth certificates for all children",
                    "Prior court orders (if any)",
                    "Prenuptial or postnuptial agreement (if any)"
                ],
                default=[
                    "Last 3 years of tax returns (complete with all schedules)",
                    "Last 3 months of pay stubs",
                    "Last 12 months of bank statements (all accounts)",
                    "Marriage certificate"
                ]
            )

            if st.button("📄 Generate Welcome Letter", type="primary"):
                if client_name and client_address:
                    client = PartyInfo(
                        name=client_name, address=client_address, city=client_city,
                        state=client_state, zip_code=client_zip, phone=""
                    )

                    doc = doc_templates.generate_initial_client_letter(
                        client=client,
                        case_type=case_type,
                        next_steps=next_steps,
                        documents_needed=docs_needed
                    )

                    st.success("✅ Welcome Letter Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Welcome Letter",
                        doc,
                        file_name=f"welcome_letter_{client_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter client name and address.")

    # ========================================================================
    # LIFECYCLE STAGE 2: CORRESPONDENCE
    # ========================================================================

    elif module == "📨 Demand Letter":
        st.header("📨 Initial Demand Letter")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a demand letter to the opposing party.**

            Use this when:
            - Client wants to attempt settlement before filing
            - Need to put opposing party on notice
            - Requesting specific actions or responses
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Our Client")
                client_name = st.text_input("Client Name*", key="dem_client_name")
                client_address = st.text_input("Client Address", key="dem_client_addr")
                client_city = st.text_input("City", key="dem_client_city")
                client_state = st.text_input("State", value="NY", key="dem_client_state")
                client_zip = st.text_input("ZIP", key="dem_client_zip")

            with col2:
                st.subheader("Opposing Party")
                opp_name = st.text_input("Opposing Party Name*", key="dem_opp_name")
                opp_address = st.text_input("Opposing Party Address*", key="dem_opp_addr")
                opp_city = st.text_input("City", key="dem_opp_city")
                opp_state = st.text_input("State", value="NY", key="dem_opp_state")
                opp_zip = st.text_input("ZIP", key="dem_opp_zip")

            case_type = st.selectbox(
                "Matter Type",
                ["Divorce and Property Division", "Child Custody",
                 "Child Support Arrears", "Spousal Maintenance",
                 "Enforcement of Court Order", "Other Family Matter"]
            )

            st.subheader("Demands")
            demands = st.multiselect(
                "Select demands to include:",
                [
                    "Immediately cease all contact with our client",
                    "Provide full financial disclosure within 20 days",
                    "Pay outstanding child support arrears",
                    "Pay outstanding maintenance arrears",
                    "Return marital property in your possession",
                    "Comply with existing court orders",
                    "Vacate the marital residence",
                    "Return children to custodial parent",
                    "Cease dissipation of marital assets",
                    "Maintain health insurance coverage",
                    "Respond to this letter within 20 days"
                ],
                default=["Provide full financial disclosure within 20 days",
                        "Respond to this letter within 20 days"]
            )

            deadline_days = st.slider("Response Deadline (days)", 10, 30, 20)

            if st.button("📄 Generate Demand Letter", type="primary"):
                if client_name and opp_name and opp_address:
                    client = PartyInfo(
                        name=client_name, address=client_address, city=client_city,
                        state=client_state, zip_code=client_zip, phone=""
                    )
                    opposing = PartyInfo(
                        name=opp_name, address=opp_address, city=opp_city,
                        state=opp_state, zip_code=opp_zip, phone=""
                    )

                    doc = doc_templates.generate_demand_letter(
                        client=client,
                        opposing_party=opposing,
                        case_type=case_type,
                        demands=demands,
                        deadline_days=deadline_days
                    )

                    st.success("✅ Demand Letter Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Demand Letter",
                        doc,
                        file_name=f"demand_letter_{opp_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter client name and opposing party information.")

    elif module == "📧 Letter to Counsel":
        st.header("📧 Letter to Opposing Counsel")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a professional letter to opposing counsel.**

            Use this for:
            - Initial contact and notice of representation
            - Discovery requests and scheduling
            - Settlement discussions
            - Conference scheduling
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Our Client")
                client_name = st.text_input("Client Name*", key="opp_client_name")

                st.subheader("Opposing Party")
                opp_name = st.text_input("Opposing Party Name*", key="opp_party_name")

            with col2:
                st.subheader("Opposing Counsel")
                opp_attorney = st.text_input("Attorney Name*", key="opp_atty_name")
                opp_firm = st.text_input("Firm Name", key="opp_firm")
                opp_firm_addr = st.text_area("Firm Address", key="opp_firm_addr")

            case_type = st.selectbox(
                "Case Type",
                ["Divorce", "Custody/Visitation", "Child Support",
                 "Spousal Maintenance", "Post-Judgment Modification"]
            )
            index_number = st.text_input("Index/Docket Number (if assigned)")

            if st.button("📄 Generate Letter to Counsel", type="primary"):
                if client_name and opp_name and opp_attorney:
                    client = PartyInfo(
                        name=client_name, address="", city="", state="NY",
                        zip_code="", phone=""
                    )
                    opposing = PartyInfo(
                        name=opp_name, address="", city="", state="NY",
                        zip_code="", phone=""
                    )

                    doc = doc_templates.generate_opposing_counsel_letter(
                        client=client,
                        opposing_party=opposing,
                        opposing_attorney=opp_attorney,
                        opposing_firm=opp_firm,
                        opposing_address=opp_firm_addr,
                        case_type=case_type,
                        index_number=index_number
                    )

                    st.success("✅ Letter to Counsel Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Letter",
                        doc,
                        file_name=f"letter_to_counsel_{opp_attorney.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter all required information.")

    # ========================================================================
    # LIFECYCLE STAGE 3: PLEADINGS & FILINGS
    # ========================================================================

    elif module == "📑 Summons with Notice":
        st.header("📑 Summons with Notice")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a Summons with Notice to commence a divorce action.**

            This document:
            - Formally commences the divorce action
            - Notifies defendant of the lawsuit
            - Includes automatic orders (DRL §236(B)(2)(b))
            - Specifies relief sought
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Plaintiff")
                plaintiff_name = st.text_input("Plaintiff Name*", key="sum_plaintiff_name")
                plaintiff_address = st.text_input("Address", key="sum_plaintiff_addr")
                plaintiff_city = st.text_input("City", key="sum_plaintiff_city")
                plaintiff_state = st.text_input("State", value="NY", key="sum_plaintiff_state")
                plaintiff_zip = st.text_input("ZIP", key="sum_plaintiff_zip")

            with col2:
                st.subheader("Defendant")
                defendant_name = st.text_input("Defendant Name*", key="sum_defendant_name")
                defendant_address = st.text_input("Address", key="sum_defendant_addr")
                defendant_city = st.text_input("City", key="sum_defendant_city")
                defendant_state = st.text_input("State", value="NY", key="sum_defendant_state")
                defendant_zip = st.text_input("ZIP", key="sum_defendant_zip")

            county = st.selectbox(
                "County",
                ["Nassau", "Suffolk", "Queens", "Kings", "New York", "Bronx",
                 "Westchester", "Rockland", "Orange", "Dutchess"],
                key="sum_county"
            )

            st.subheader("Relief Requested")
            relief = st.multiselect(
                "Select all relief sought:",
                [
                    "Absolute divorce",
                    "Equitable distribution of marital property",
                    "Spousal maintenance",
                    "Child custody",
                    "Child support",
                    "Counsel fees",
                    "Exclusive use of marital residence"
                ],
                default=["Absolute divorce", "Equitable distribution of marital property"]
            )

            if st.button("📄 Generate Summons with Notice", type="primary"):
                if plaintiff_name and defendant_name:
                    plaintiff = PartyInfo(
                        name=plaintiff_name, address=plaintiff_address, city=plaintiff_city,
                        state=plaintiff_state, zip_code=plaintiff_zip, phone=""
                    )
                    defendant = PartyInfo(
                        name=defendant_name, address=defendant_address, city=defendant_city,
                        state=defendant_state, zip_code=defendant_zip, phone=""
                    )

                    doc = doc_templates.generate_summons_with_notice(
                        plaintiff=plaintiff,
                        defendant=defendant,
                        county=county,
                        relief_requested=relief
                    )

                    st.success("✅ Summons with Notice Generated!")
                    st.text_area("Document Preview", doc, height=500)
                    st.download_button(
                        "📥 Download Summons",
                        doc,
                        file_name=f"summons_{plaintiff_name.replace(' ', '_')}_v_{defendant_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please enter both party names.")

    elif module == "📝 Verified Complaint":
        st.header("📝 Verified Complaint for Divorce")
        st.info("Redirecting to Document Templates for Verified Complaint generation...")
        st.markdown("Use the **📝 Document Templates** section and select **Verified Complaint**")

    elif module == "⚖️ Notice of Appearance":
        st.header("⚖️ Notice of Appearance")

        if not TEMPLATES_AVAILABLE:
            st.error("Document templates module not available.")
        else:
            st.info("""
            **Generate a Notice of Appearance for an existing case.**

            Use when:
            - Entering appearance for a client in pending litigation
            - Substituting as new counsel
            - Formalizing representation in court
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Our Client")
                client_name = st.text_input("Client Name*", key="noa_client_name")
                client_address = st.text_input("Address", key="noa_client_addr")
                client_city = st.text_input("City", key="noa_client_city")
                client_state = st.text_input("State", value="NY", key="noa_client_state")
                client_zip = st.text_input("ZIP", key="noa_client_zip")

            with col2:
                st.subheader("Opposing Party")
                opp_name = st.text_input("Opposing Party Name*", key="noa_opp_name")

            col1, col2 = st.columns(2)

            with col1:
                county = st.selectbox(
                    "County",
                    ["Nassau", "Suffolk", "Queens", "Kings", "New York", "Bronx"],
                    key="noa_county"
                )
                index_number = st.text_input("Index Number*", key="noa_index")

            with col2:
                attorney_name = st.text_input("Appearing Attorney Name*", key="noa_atty")

            if st.button("📄 Generate Notice of Appearance", type="primary"):
                if client_name and opp_name and index_number and attorney_name:
                    client = PartyInfo(
                        name=client_name, address=client_address, city=client_city,
                        state=client_state, zip_code=client_zip, phone=""
                    )
                    opp = PartyInfo(
                        name=opp_name, address="", city="", state="NY",
                        zip_code="", phone=""
                    )

                    doc = doc_templates.generate_notice_of_appearance(
                        client=client,
                        opposing_party=opp,
                        county=county,
                        index_number=index_number,
                        attorney_name=attorney_name
                    )

                    st.success("✅ Notice of Appearance Generated!")
                    st.text_area("Document Preview", doc, height=400)
                    st.download_button(
                        "📥 Download Notice of Appearance",
                        doc,
                        file_name=f"notice_of_appearance_{client_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Please fill in all required fields.")

    # ========================================================================
    # LIFECYCLE STAGE 4: FINANCIAL ANALYSIS (Mapped to existing templates)
    # ========================================================================

    elif module == "💰 Net Worth Statement":
        st.header("💰 Net Worth Statement (DRL §236)")
        st.info("Redirecting to Document Templates for Net Worth Statement generation...")
        st.markdown("Use the **📝 Document Templates** section and select **Net Worth Statement**")

    elif module == "👶 Child Support Worksheet":
        st.header("👶 Child Support Worksheet (CSSA)")
        st.info("Redirecting to Document Templates for Child Support Worksheet generation...")
        st.markdown("Use the **📝 Document Templates** section and select **Child Support Worksheet**")

    # ========================================================================
    # LIFECYCLE STAGE 5: SETTLEMENT & RESOLUTION (Mapped to existing templates)
    # ========================================================================

    elif module == "🤝 Settlement Agreement":
        st.header("🤝 Stipulation of Settlement")
        st.info("Redirecting to Document Templates for Settlement Agreement generation...")
        st.markdown("Use the **📝 Document Templates** section and select **Stipulation of Settlement**")

    elif module == "🛡️ Order of Protection":
        st.header("🛡️ Order of Protection Petition")
        st.info("Redirecting to Document Templates for Order of Protection petition...")
        st.markdown("Use the **📝 Document Templates** section and select **Family Offense Petition**")

    # ========================================================================
    # LIFECYCLE STAGE 6: TOOLS - Renamed modules
    # ========================================================================

    elif module == "🔍 OCR Scanner":
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

    elif module == "📁 Google Drive" or module == "📁 Google Drive Manager":
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

    elif module == "📂 Case Management":
        st.header("Case Management System")

        if not CASE_MANAGER_AVAILABLE:
            st.error("Case management module not available.")
        else:
            # Initialize case manager in session state
            if 'case_manager' not in st.session_state:
                st.session_state.case_manager = create_case_manager()

            cm = st.session_state.case_manager

            # Dashboard overview
            dashboard = cm.get_dashboard_data()

            # Key metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Active Cases", dashboard['active_cases'])
            with col2:
                overdue_color = "🔴" if dashboard['overdue_deadlines'] > 0 else "🟢"
                st.metric(f"{overdue_color} Overdue", dashboard['overdue_deadlines'])
            with col3:
                st.metric("📅 Upcoming (7 days)", dashboard['upcoming_deadlines'])
            with col4:
                st.metric("📋 Pending Tasks", dashboard['pending_tasks'])

            st.markdown("---")

            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Dashboard", "📁 Cases", "📅 Deadlines", "✅ Tasks", "➕ New Case"
            ])

            with tab1:
                st.subheader("Practice Dashboard")

                # Alerts section
                if dashboard['overdue_deadlines'] > 0:
                    st.error(f"⚠️ {dashboard['overdue_deadlines']} OVERDUE DEADLINE(S) - Action Required!")

                    for dl in dashboard['overdue_list']:
                        case = cm.cases.get(dl.case_id)
                        client = case.client_name if case else "Unknown"
                        st.warning(f"**{dl.title}** - {client} ({abs(dl.days_until_due)} days overdue)")

                # Upcoming deadlines
                if dashboard['upcoming_list']:
                    st.subheader("📅 Upcoming Deadlines (7 Days)")
                    for dl in dashboard['upcoming_list']:
                        case = cm.cases.get(dl.case_id)
                        client = case.client_name if case else "Unknown"
                        urgency = dl.urgency_level

                        if urgency == "CRITICAL":
                            st.error(f"🔴 **{dl.title}** - {client} | Due: {dl.due_date} (TOMORROW)")
                        elif urgency == "URGENT":
                            st.warning(f"🟠 **{dl.title}** - {client} | Due: {dl.due_date} ({dl.days_until_due} days)")
                        else:
                            st.info(f"📆 **{dl.title}** - {client} | Due: {dl.due_date}")

                # Urgent tasks
                if dashboard['urgent_task_list']:
                    st.subheader("🚨 Urgent Tasks")
                    for task in dashboard['urgent_task_list']:
                        case = cm.cases.get(task.case_id)
                        client = case.client_name if case else "Unknown"
                        st.warning(f"**{task.title}** - {client}")

                # Case distribution charts
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Cases by Status")
                    if dashboard['status_breakdown']:
                        for status, count in dashboard['status_breakdown'].items():
                            st.write(f"• {status}: **{count}**")

                with col2:
                    st.subheader("Cases by Type")
                    if dashboard['type_breakdown']:
                        for case_type, count in dashboard['type_breakdown'].items():
                            st.write(f"• {case_type}: **{count}**")

                # Weekly report
                if st.button("📄 Generate Weekly Report"):
                    report = cm.generate_weekly_report()
                    st.text_area("Weekly Report", report, height=400)
                    st.download_button(
                        "📥 Download Report",
                        report,
                        file_name=f"weekly_report_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )

            with tab2:
                st.subheader("All Cases")

                # Filter by status
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All"] + [s.value for s in CaseStatus]
                )

                cases = cm.get_all_cases(None if status_filter == "All" else status_filter)

                if not cases:
                    st.info("No cases found. Create a new case to get started.")
                else:
                    for case in cases:
                        with st.expander(f"📁 {case.client_name} vs. {case.opposing_party or 'N/A'} | {case.case_type}"):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"**Case Number:** {case.case_number or 'Pending'}")
                                st.write(f"**Status:** {case.status}")
                                st.write(f"**Court:** {case.court}")
                                st.write(f"**Judge:** {case.judge or 'TBD'}")

                            with col2:
                                st.write(f"**Opened:** {case.open_date}")
                                st.write(f"**Attorney:** {case.attorney or 'N/A'}")
                                st.write(f"**Paralegal:** {case.paralegal or 'N/A'}")

                            summary = cm.get_case_summary(case.id)
                            st.write(f"**Tasks:** {summary['completed_tasks']}/{summary['total_tasks']} completed")
                            st.write(f"**Deadlines:** {summary['completed_deadlines']}/{summary['total_deadlines']} completed")

                            # Quick actions
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("View Details", key=f"view_{case.id}"):
                                    st.session_state.selected_case = case.id
                            with col2:
                                new_status = st.selectbox(
                                    "Update Status",
                                    [s.value for s in CaseStatus],
                                    index=[s.value for s in CaseStatus].index(case.status) if case.status in [s.value for s in CaseStatus] else 0,
                                    key=f"status_{case.id}"
                                )
                                if new_status != case.status:
                                    cm.update_case(case.id, {'status': new_status})
                                    st.rerun()

            with tab3:
                st.subheader("Deadline Management")

                # Show upcoming deadlines
                days_ahead = st.slider("Show deadlines for next N days", 7, 90, 30)
                deadlines = cm.get_upcoming_deadlines(days_ahead)

                if not deadlines:
                    st.info("No upcoming deadlines.")
                else:
                    for dl in deadlines:
                        case = cm.cases.get(dl.case_id)
                        client = case.client_name if case else "Unknown"
                        urgency = dl.urgency_level

                        col1, col2, col3 = st.columns([3, 1, 1])

                        with col1:
                            if urgency in ["CRITICAL", "URGENT"]:
                                st.warning(f"**{dl.title}** - {client}")
                            else:
                                st.write(f"**{dl.title}** - {client}")
                            st.caption(f"{dl.deadline_type} | {dl.location}")

                        with col2:
                            st.write(f"📅 {dl.due_date}")
                            st.caption(f"{dl.days_until_due} days")

                        with col3:
                            if st.button("✓ Complete", key=f"complete_dl_{dl.id}"):
                                cm.complete_deadline(dl.id)
                                st.rerun()

                st.markdown("---")

                # Add new deadline
                st.subheader("Add New Deadline")

                case_options = {f"{c.client_name} ({c.id})": c.id for c in cm.cases.values()}

                if case_options:
                    col1, col2 = st.columns(2)

                    with col1:
                        selected_case = st.selectbox("Select Case", list(case_options.keys()), key="new_dl_case")
                        dl_title = st.text_input("Deadline Title", key="new_dl_title")
                        dl_type = st.selectbox("Type", [t.value for t in DeadlineType], key="new_dl_type")

                    with col2:
                        dl_date = st.date_input("Due Date", key="new_dl_date")
                        dl_time = st.time_input("Due Time (optional)", key="new_dl_time")
                        dl_location = st.text_input("Location", key="new_dl_loc")

                    if st.button("Add Deadline", type="primary"):
                        if dl_title:
                            cm.create_deadline({
                                'case_id': case_options[selected_case],
                                'title': dl_title,
                                'deadline_type': dl_type,
                                'due_date': dl_date.strftime("%Y-%m-%d"),
                                'due_time': dl_time.strftime("%H:%M") if dl_time else "",
                                'location': dl_location
                            })
                            st.success("✅ Deadline added!")
                            st.rerun()
                else:
                    st.info("Create a case first to add deadlines.")

            with tab4:
                st.subheader("Task Management")

                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    case_filter = st.selectbox(
                        "Filter by Case",
                        ["All Cases"] + [f"{c.client_name}" for c in cm.cases.values()],
                        key="task_case_filter"
                    )
                with col2:
                    priority_filter = st.multiselect(
                        "Filter by Priority",
                        ["Urgent", "High", "Medium", "Low"],
                        default=["Urgent", "High"],
                        key="task_priority_filter"
                    )

                # Get filtered tasks
                case_id_filter = None
                if case_filter != "All Cases":
                    for c in cm.cases.values():
                        if c.client_name == case_filter:
                            case_id_filter = c.id
                            break

                tasks = cm.get_pending_tasks(case_id_filter)
                tasks = [t for t in tasks if t.priority in priority_filter]

                if not tasks:
                    st.info("No pending tasks matching filters.")
                else:
                    for task in tasks:
                        case = cm.cases.get(task.case_id)
                        client = case.client_name if case else "Unknown"

                        priority_colors = {"Urgent": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}

                        col1, col2, col3 = st.columns([4, 1, 1])

                        with col1:
                            st.write(f"{priority_colors.get(task.priority, '⚪')} **{task.title}**")
                            st.caption(f"{client} | Est: {task.estimated_minutes} min")

                        with col2:
                            new_status = st.selectbox(
                                "Status",
                                ["Pending", "In Progress", "Completed"],
                                index=["Pending", "In Progress", "Completed"].index(task.status) if task.status in ["Pending", "In Progress", "Completed"] else 0,
                                key=f"task_status_{task.id}"
                            )
                            if new_status != task.status:
                                cm.update_task(task.id, {'status': new_status})
                                st.rerun()

                        with col3:
                            if st.button("✓ Done", key=f"complete_task_{task.id}"):
                                cm.update_task(task.id, {'status': 'Completed'})
                                st.rerun()

            with tab5:
                st.subheader("Create New Case")

                col1, col2 = st.columns(2)

                with col1:
                    new_client_name = st.text_input("Client Name*", key="new_case_client")
                    new_opposing = st.text_input("Opposing Party", key="new_case_opposing")
                    new_case_type = st.selectbox("Case Type*", [t.value for t in CaseType], key="new_case_type")
                    new_court = st.selectbox(
                        "Court*",
                        firm_config.courts if firm_config else ["Nassau County Supreme Court", "Nassau County Family Court"],
                        key="new_case_court"
                    )

                with col2:
                    new_case_number = st.text_input("Index/Docket Number", key="new_case_number")
                    new_judge = st.text_input("Judge (if known)", key="new_case_judge")
                    new_attorney = st.text_input("Attorney Assigned", key="new_case_attorney")
                    new_paralegal = st.text_input("Paralegal Assigned", key="new_case_paralegal")

                st.markdown("---")

                col1, col2 = st.columns(2)
                with col1:
                    new_marriage_date = st.date_input("Marriage Date", key="new_case_marriage")
                with col2:
                    new_separation_date = st.date_input("Separation Date", key="new_case_separation")

                new_description = st.text_area("Case Description/Notes", key="new_case_desc")

                col1, col2 = st.columns(2)
                with col1:
                    new_retainer = st.number_input("Retainer Amount ($)", 0.0, step=500.0, key="new_case_retainer")

                if st.button("Create Case", type="primary"):
                    if new_client_name:
                        case = cm.create_case({
                            'client_name': new_client_name,
                            'opposing_party': new_opposing,
                            'case_type': new_case_type,
                            'case_number': new_case_number,
                            'court': new_court,
                            'county': new_court.split()[0] if new_court else "Nassau",
                            'judge': new_judge,
                            'attorney': new_attorney,
                            'paralegal': new_paralegal,
                            'marriage_date': new_marriage_date.strftime("%Y-%m-%d"),
                            'separation_date': new_separation_date.strftime("%Y-%m-%d"),
                            'description': new_description,
                            'retainer_amount': new_retainer,
                            'retainer_balance': new_retainer
                        })

                        st.success(f"✅ Case created: {case.id}")
                        st.info("📋 Standard intake tasks have been automatically created.")
                        st.rerun()
                    else:
                        st.warning("Please enter client name.")

    elif module == "📈 ROI Dashboard":
        st.header("ROI & Efficiency Analytics")

        if not ROI_AVAILABLE:
            st.error("ROI calculator module not available.")
        else:
            # Initialize ROI calculator
            if 'roi_calculator' not in st.session_state:
                st.session_state.roi_calculator = create_roi_calculator()

            calc = st.session_state.roi_calculator

            st.info("""
            **Demonstrate the value of automation to your practice.**

            This dashboard shows real-time ROI calculations based on your firm's case volume
            and industry-standard time benchmarks for paralegal tasks.
            """)

            # Configuration section
            with st.expander("⚙️ Customize Your Practice Profile"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    new_cases = st.number_input("New Cases/Month", 1, 50, 8)
                    calc.case_volume.new_cases_per_month = new_cases

                with col2:
                    active_cases = st.number_input("Active Cases", 10, 200, 45)
                    calc.case_volume.active_cases = active_cases

                with col3:
                    paralegal_rate = st.number_input("Paralegal Hourly Rate ($)", 20.0, 75.0, 35.0)
                    calc.paralegal_costs.hourly_rate = paralegal_rate

            st.markdown("---")

            # Calculate ROI at different price points
            platform_cost = st.slider("Monthly Platform Cost ($)", 500, 3000, 1500, 100)
            roi = calc.calculate_full_roi(platform_cost)

            # Key metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Monthly Time Saved",
                    f"{roi.monthly_time_saved_hours:.1f} hrs",
                    f"{roi.efficiency_gain_percentage:.0f}% more efficient"
                )

            with col2:
                st.metric(
                    "Monthly Cost Saved",
                    f"${roi.monthly_cost_saved:,.0f}",
                    f"${roi.annual_cost_saved:,.0f}/year"
                )

            with col3:
                st.metric(
                    "Paralegal FTE Equivalent",
                    f"{roi.paralegal_fte_equivalent:.2f}",
                    "staff savings"
                )

            with col4:
                if roi.payback_period_months < 12:
                    st.metric(
                        "Payback Period",
                        f"{roi.payback_period_months:.1f} months",
                        f"{roi.roi_percentage:.0f}% ROI"
                    )
                else:
                    st.metric(
                        "ROI",
                        f"{roi.roi_percentage:.0f}%",
                        "Annual Return"
                    )

            st.markdown("---")

            # Task-by-task breakdown
            st.subheader("📊 Time Savings by Task")

            tasks = roi.tasks_automated

            # Create a dataframe for visualization
            task_data = []
            for task_name, data in tasks.items():
                task_data.append({
                    'Task': task_name,
                    'Manual (hrs)': data['manual_minutes'] / 60,
                    'Automated (hrs)': data['automated_minutes'] / 60,
                    'Saved (hrs)': data['savings_minutes'] / 60,
                    'Efficiency': f"{(data['savings_minutes'] / data['manual_minutes']) * 100:.0f}%"
                })

            df = pd.DataFrame(task_data)
            st.dataframe(df, use_container_width=True)

            # Visual comparison
            st.subheader("📈 Before vs. After Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Monthly Time Without Automation:**")
                total_manual = sum(t['manual_minutes'] for t in tasks.values()) / 60
                st.metric("Total Hours", f"{total_manual:.1f}")
                st.caption(f"= {total_manual / 40:.1f} work weeks")

            with col2:
                st.write("**Monthly Time With Platform:**")
                total_auto = sum(t['automated_minutes'] for t in tasks.values()) / 60
                st.metric("Total Hours", f"{total_auto:.1f}")
                st.caption(f"= {total_auto / 40:.1f} work weeks")

            st.markdown("---")

            # Financial Summary
            st.subheader("💰 Financial Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Cost Analysis (Annual)**")
                st.write(f"• Paralegal time saved: **${roi.annual_cost_saved:,.0f}**")
                st.write(f"• Platform cost: **${platform_cost * 12:,.0f}**")
                net_savings = roi.annual_cost_saved - (platform_cost * 12)
                st.write(f"• **Net Savings: ${net_savings:,.0f}**")

            with col2:
                st.write("**Value Beyond Cost Savings**")
                st.write("• Faster case turnaround")
                st.write("• Reduced errors in calculations")
                st.write("• Better deadline compliance")
                st.write("• Improved client satisfaction")
                st.write("• Scalability without hiring")

            # Download comparison report
            st.markdown("---")

            if st.button("📄 Generate ROI Report"):
                comparison = calc.generate_comparison_table()

                report = f"""
ROI ANALYSIS REPORT
Generated: {datetime.now().strftime("%B %d, %Y")}
{'=' * 60}

PRACTICE PROFILE
----------------
New Cases/Month: {calc.case_volume.new_cases_per_month}
Active Cases: {calc.case_volume.active_cases}
Paralegal Hourly Rate: ${calc.paralegal_costs.hourly_rate:.2f}

KEY METRICS
-----------
Monthly Time Saved: {roi.monthly_time_saved_hours:.1f} hours
Monthly Cost Saved: ${roi.monthly_cost_saved:,.2f}
Annual Cost Saved: ${roi.annual_cost_saved:,.2f}
Paralegal FTE Equivalent: {roi.paralegal_fte_equivalent:.2f}
Efficiency Gain: {roi.efficiency_gain_percentage:.0f}%
ROI: {roi.roi_percentage:.0f}%
Payback Period: {roi.payback_period_months:.1f} months

TASK COMPARISON
---------------
{comparison}

RECOMMENDATION
--------------
At ${platform_cost}/month, this platform delivers ${net_savings:,.0f} in net annual savings.
"""
                st.text_area("Report", report, height=400)
                st.download_button(
                    "📥 Download Report",
                    report,
                    file_name="roi_analysis_report.txt",
                    mime="text/plain"
                )

    elif module == "🎯 Sales Demo":
        st.header("Sales Demonstration Mode")

        if not ROI_AVAILABLE:
            st.error("Demo module not available.")
        else:
            calc = create_roi_calculator()

            st.success("""
            **Welcome to the Family Law Practice Automation Platform Demo!**

            This presentation demonstrates how our platform can transform your practice
            by automating time-consuming paralegal tasks while maintaining accuracy
            and compliance with NY Family Law requirements.
            """)

            # Demo navigation
            demo_section = st.radio(
                "Select Demo Section:",
                ["🎬 Executive Overview", "⏱️ Time Savings Demo", "💵 Pricing Options",
                 "🏆 Why Choose Us", "📋 Implementation Plan"],
                horizontal=True
            )

            st.markdown("---")

            if demo_section == "🎬 Executive Overview":
                st.subheader("Transform Your Family Law Practice")

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("""
                    ### The Challenge
                    Family law practices face increasing pressure to:
                    - Handle more cases with limited staff
                    - Maintain accuracy in complex financial calculations
                    - Meet strict court deadlines
                    - Reduce operating costs while improving service

                    ### Our Solution
                    A comprehensive automation platform designed specifically for
                    NY Family Law practices that:

                    ✅ **Automates document preparation** - Net Worth Statements,
                    Complaints, Child Support Worksheets in minutes, not hours

                    ✅ **Ensures calculation accuracy** - Built-in CSSA and DRL §236
                    compliance, eliminating costly errors

                    ✅ **Manages deadlines proactively** - Never miss a filing
                    deadline or court date again

                    ✅ **Extracts data from documents** - OCR technology reads
                    tax returns, bank statements, and pay stubs automatically

                    ✅ **Integrates with your workflow** - Google Drive integration
                    for seamless document management
                    """)

                with col2:
                    st.info("""
                    **Quick Stats**

                    📊 **83%** average efficiency gain

                    ⏱️ **62 hours** saved monthly

                    💰 **$2,800** monthly cost savings

                    📅 **0** missed deadlines

                    🎯 **3.2 month** payback period
                    """)

            elif demo_section == "⏱️ Time Savings Demo":
                st.subheader("Real-World Time Savings")

                # Interactive comparison
                st.write("### Select a task to see the time savings:")

                task_demos = {
                    "Net Worth Statement Preparation": {
                        "manual": 180,
                        "automated": 30,
                        "description": "Complete DRL §236 compliant statement with all schedules"
                    },
                    "Child Support Calculation": {
                        "manual": 45,
                        "automated": 5,
                        "description": "Full CSSA calculation with add-ons and pro-rata shares"
                    },
                    "Tax Return Analysis": {
                        "manual": 120,
                        "automated": 15,
                        "description": "Extract income, identify discrepancies, flag issues"
                    },
                    "Bank Statement Review": {
                        "manual": 60,
                        "automated": 10,
                        "description": "Analyze 3 months of transactions for patterns"
                    },
                    "Verified Complaint Drafting": {
                        "manual": 120,
                        "automated": 20,
                        "description": "Generate court-ready complaint with all allegations"
                    }
                }

                selected_task = st.selectbox("Choose a task:", list(task_demos.keys()))

                task = task_demos[selected_task]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Manual Time", f"{task['manual']} min")
                with col2:
                    st.metric("With Platform", f"{task['automated']} min")
                with col3:
                    savings = task['manual'] - task['automated']
                    pct = (savings / task['manual']) * 100
                    st.metric("Time Saved", f"{savings} min", f"{pct:.0f}% faster")

                st.info(f"**What's included:** {task['description']}")

                # Monthly impact
                st.markdown("---")
                st.write("### Monthly Impact (8 new cases)")

                monthly_manual = sum(t['manual'] for t in task_demos.values()) * 8
                monthly_auto = sum(t['automated'] for t in task_demos.values()) * 8

                col1, col2 = st.columns(2)

                with col1:
                    st.error(f"""
                    **Without Automation**
                    - {monthly_manual / 60:.0f} hours/month on these tasks
                    - {monthly_manual / 60 / 40:.1f} weeks of paralegal time
                    - ${monthly_manual / 60 * 45.50:.0f} in labor costs
                    """)

                with col2:
                    st.success(f"""
                    **With Our Platform**
                    - {monthly_auto / 60:.0f} hours/month on these tasks
                    - {monthly_auto / 60 / 40:.1f} weeks of paralegal time
                    - ${monthly_auto / 60 * 45.50:.0f} in labor costs
                    """)

            elif demo_section == "💵 Pricing Options":
                st.subheader("Investment Options")

                pricing = calc.generate_pricing_recommendation()

                col1, col2, col3 = st.columns(3)

                with col1:
                    tier = pricing['pricing_tiers']['starter']
                    st.markdown(f"""
                    ### 🥉 Starter
                    ## ${tier['price']}/month

                    **Best for:** Solo practitioners

                    **Includes:**
                    """)
                    for feature in tier['features']:
                        st.write(f"✓ {feature}")

                    st.info(f"ROI: {tier['roi_percentage']:.0f}%")

                with col2:
                    tier = pricing['pricing_tiers']['professional']
                    st.markdown(f"""
                    ### 🥈 Professional
                    ## ${tier['price']}/month

                    **Best for:** Small firms (2-5 attorneys)

                    **Includes:**
                    """)
                    for feature in tier['features']:
                        st.write(f"✓ {feature}")

                    st.success(f"**RECOMMENDED** - ROI: {tier['roi_percentage']:.0f}%")

                with col3:
                    tier = pricing['pricing_tiers']['enterprise']
                    st.markdown(f"""
                    ### 🥇 Enterprise
                    ## ${tier['price']}/month

                    **Best for:** Larger practices

                    **Includes:**
                    """)
                    for feature in tier['features']:
                        st.write(f"✓ {feature}")

                    st.info(f"ROI: {tier['roi_percentage']:.0f}%")

                st.markdown("---")

                # Alternative pricing
                st.write("### Alternative: One-Time License")

                alt = pricing['one_time_alternative']
                st.write(f"""
                - **Setup Fee:** ${alt['setup_fee']:,}
                - **Monthly Support:** ${alt['monthly_support']}/month
                - **Year 1 Total:** ${alt['total_year_1']:,}

                *{alt['note']}*
                """)

            elif demo_section == "🏆 Why Choose Us":
                st.subheader("Built for NY Family Law Practices")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
                    ### ⚖️ Legal Compliance Built-In

                    - **DRL §236** maintenance calculations
                    - **DRL §240(1-b)** CSSA child support
                    - **22 NYCRR §202.16(b)** Net Worth Statement format
                    - 2024 income caps automatically applied
                    - Nassau County court-specific formatting

                    ### 🔒 Security & Confidentiality

                    - Attorney-client privilege protected
                    - Encrypted data storage
                    - Secure Google Drive integration
                    - No data sharing with third parties
                    - HIPAA-compliant infrastructure

                    ### 🏠 Local Expertise

                    - Built for Nassau County practices
                    - Familiar with local court requirements
                    - Understands DV case sensitivities
                    - Knows the judges and procedures
                    """)

                with col2:
                    st.markdown("""
                    ### 🚀 Rapid Implementation

                    - Up and running in 1 week
                    - Import existing case data
                    - Train your team in 2 hours
                    - Full support during transition
                    - No disruption to current cases

                    ### 💪 Proven Results

                    > "We cut our document preparation time by 80%
                    > and haven't missed a deadline since implementing
                    > the platform."
                    >
                    > *— Family Law Attorney, Nassau County*

                    ### 📞 Dedicated Support

                    - Dedicated account manager
                    - Phone and email support
                    - Regular feature updates
                    - Custom template requests
                    - Training for new staff
                    """)

            elif demo_section == "📋 Implementation Plan":
                st.subheader("Getting Started is Easy")

                st.markdown("""
                ### Week 1: Setup & Configuration

                **Day 1-2:**
                - Account creation and branding setup
                - Google Drive integration
                - User account creation

                **Day 3-4:**
                - Import existing client/case data
                - Configure deadline calendars
                - Set up document templates

                **Day 5:**
                - Staff training session (2 hours)
                - Q&A and customization requests

                ---

                ### Week 2: Go Live

                **Day 6-7:**
                - Parallel operation (old + new system)
                - Real case processing with supervision

                **Day 8-10:**
                - Full transition to platform
                - Support available for any issues

                ---

                ### Ongoing

                - Weekly check-ins for first month
                - Monthly feature updates
                - Quarterly business reviews
                - Annual ROI assessments
                """)

                st.success("""
                ### Ready to Transform Your Practice?

                📞 **Schedule a Demo:** (347) 628-5440

                📧 **Email:** info@whitelawgroupny.com

                🌐 **Website:** wwlgny.com
                """)

    elif module == "⚙️ Settings":
        st.header("Settings & Configuration")

        if firm_config:
            st.subheader("Firm Information")

            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Firm Name", value=firm_config.firm_name, disabled=True)
                st.text_input("Phone", value=firm_config.phone, disabled=True)
                st.text_input("Email", value=firm_config.email, disabled=True)

            with col2:
                st.text_input("Address", value=firm_config.address, disabled=True)
                st.text_input("Website", value=firm_config.website, disabled=True)
                st.text_input("Primary Jurisdiction", value=firm_config.primary_jurisdiction, disabled=True)

            st.info("To customize firm settings, edit `firm_config.py`")

            st.markdown("---")

            st.subheader("Practice Areas")
            for area in firm_config.practice_areas:
                st.write(f"• {area}")

            st.markdown("---")

            st.subheader("Configured Courts")
            for court in firm_config.courts:
                st.write(f"• {court}")

        st.markdown("---")

        st.subheader("System Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            if OCR_AVAILABLE:
                st.success("✅ OCR Module")
            else:
                st.error("❌ OCR Module")

        with col2:
            if DRIVE_AVAILABLE:
                st.success("✅ Google Drive")
            else:
                st.error("❌ Google Drive")

        with col3:
            if FIRM_CONFIG_AVAILABLE:
                st.success("✅ Firm Config")
            else:
                st.error("❌ Firm Config")

        col1, col2, col3 = st.columns(3)

        with col1:
            if ROI_AVAILABLE:
                st.success("✅ ROI Analytics")
            else:
                st.error("❌ ROI Analytics")

        with col2:
            if CASE_MANAGER_AVAILABLE:
                st.success("✅ Case Manager")
            else:
                st.error("❌ Case Manager")

        with col3:
            if TEMPLATES_AVAILABLE:
                st.success("✅ Doc Templates")
            else:
                st.error("❌ Doc Templates")

        st.markdown("---")

        st.subheader("Nassau County Resources")

        if FIRM_CONFIG_AVAILABLE:
            st.write(f"**Courthouse:** {NASSAU_COUNTY_CONFIG['courthouse_address']}")
            st.write(f"**Family Court:** {NASSAU_COUNTY_CONFIG['family_court_address']}")

            st.write("\n**Filing Fees:**")
            for fee_type, amount in NASSAU_COUNTY_CONFIG['filing_fees'].items():
                st.write(f"• {fee_type.replace('_', ' ').title()}: ${amount}")

        st.markdown("---")

        st.subheader("About This Tool")
        st.markdown("""
        **Financial Document Analysis Tool**

        This tool is designed for family law practitioners to:
        - Calculate child support and maintenance under NY law
        - Analyze financial documents for discrepancies
        - Detect potential hidden income
        - Manage case documents via Google Drive
        - Extract text from scanned documents using OCR
        - Generate professional reports

        **Legal References:**
        - DRL §240(1-b): Child Support Standards Act
        - DRL §236(B)(6): Spousal Maintenance
        - 22 NYCRR §202.16(b): Net Worth Statement Requirements

        **Version:** 2.0 - White Law Group Edition
        """)

if __name__ == "__main__":
    main()

