# file: financial_analysis_app.py
import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
from financial_analyzer import (
    SupportCalculatorNY,
    FinancialConsistencyAnalyzer,
    NetWorthStatement
)

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
        module = st.radio(
            "Select Analysis:",
            ["Support Calculator", "Document Consistency",
             "Hidden Income Detection", "Full Analysis Report"]
        )

        st.markdown("---")
        st.info("**NY Law References:**\n"
                "- DRL §240(1-b): Child Support\n"
                "- DRL §236: Maintenance\n"
                "- Uniform Rule 202.16(b): Net Worth Statements")

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

if __name__ == "__main__":
    main()
