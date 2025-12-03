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

    # Sidebar for navigation
    with st.sidebar:
        st.header("Analysis Modules")
        
        # Build module list
        modules = ["📊 Support Calculator", "📋 Case Intake",
                  "🔎 Document Consistency", "🕵️ Hidden Income Detection",
                  "📄 Full Analysis Report"]

        if TEMPLATES_AVAILABLE:
            modules.append("📝 Document Templates")

        if OCR_AVAILABLE:
            modules.append("🔍 OCR Document Scanner")

        if DRIVE_AVAILABLE:
            modules.append("📁 Google Drive Manager")

        modules.append("⚙️ Settings")

        module = st.radio("Select Module:", modules)

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

