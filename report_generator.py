#!/usr/bin/env python3
"""
PDF Report Generator for Family Law Financial Analysis
Generates professional, client-ready reports
"""

import io
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# For PDF generation we'll use a simple HTML-to-text approach
# In production, you might use reportlab or weasyprint


@dataclass
class ReportSection:
    """A section of a report"""
    title: str
    content: str
    subsections: List['ReportSection'] = None


class ReportGenerator:
    """Generate professional PDF reports for family law cases"""

    def __init__(self, firm_name: str = "The White Law Group",
                 firm_phone: str = "(347) 628-5440",
                 firm_address: str = "4 Brower Ave Suite 3, Woodmere, NY 11598"):
        self.firm_name = firm_name
        self.firm_phone = firm_phone
        self.firm_address = firm_address

    def generate_support_report(self,
                                case_info: Dict,
                                child_support: Dict,
                                maintenance: Dict,
                                party_info: Dict) -> str:
        """Generate a comprehensive support calculation report"""

        report_date = datetime.now().strftime("%B %d, %Y")

        report = f"""
{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}

                    CHILD SUPPORT & MAINTENANCE ANALYSIS

Prepared by: {self.firm_name}
Date: {report_date}
Case: {case_info.get('case_id', 'N/A')}
Client: {case_info.get('client_name', 'N/A')}

{'=' * 70}

1. EXECUTIVE SUMMARY
{'-' * 70}

This analysis provides calculations for child support and spousal
maintenance obligations under New York Domestic Relations Law.

Key Findings:
• Recommended Monthly Child Support: ${child_support.get('total_obligation', 0) / 12:,.2f}
• Recommended Monthly Maintenance: ${maintenance.get('maintenance_amount', 0) / 12:,.2f}
• Combined Monthly Obligation: ${(child_support.get('total_obligation', 0) + maintenance.get('maintenance_amount', 0)) / 12:,.2f}

{'=' * 70}

2. PARTY INFORMATION
{'-' * 70}

PAYER:
  Name: {party_info.get('payer_name', 'N/A')}
  Annual Income: ${party_info.get('payer_income', 0):,.2f}
  Additional Income: ${party_info.get('payer_bonus', 0):,.2f}
  Total Income: ${party_info.get('payer_income', 0) + party_info.get('payer_bonus', 0):,.2f}

PAYEE:
  Name: {party_info.get('payee_name', 'N/A')}
  Annual Income: ${party_info.get('payee_income', 0):,.2f}

CHILDREN:
  Number of Children: {party_info.get('num_children', 0)}
  Special Needs: {'Yes' if party_info.get('special_needs') else 'No'}

{'=' * 70}

3. CHILD SUPPORT CALCULATION (DRL §240)
{'-' * 70}

Under the Child Support Standards Act (CSSA), child support is
calculated as follows:

INCOME ANALYSIS:
  Payer Gross Income:      ${party_info.get('payer_income', 0) + party_info.get('payer_bonus', 0):,.2f}
  Payee Gross Income:      ${party_info.get('payee_income', 0):,.2f}
  Combined Parental Income: ${child_support.get('combined_parental_income', 0):,.2f}

CSSA CALCULATION:
  Number of Children: {party_info.get('num_children', 0)}
  CSSA Percentage: {child_support.get('cssa_percentage', 0) * 100:.1f}%
  Payer's Pro Rata Share: {child_support.get('payer_income_share', 0)}%

  Basic Support Amount: ${child_support.get('basic_support_amount', 0):,.2f}

ADD-ON EXPENSES (Pro Rata Share):
"""
        # Add-ons
        add_ons = child_support.get('add_ons', {})
        for addon_name, addon_amount in add_ons.items():
            if addon_amount > 0:
                report += f"  {addon_name.replace('_', ' ').title()}: ${addon_amount:,.2f}\n"

        report += f"""
TOTAL ANNUAL CHILD SUPPORT: ${child_support.get('total_obligation', 0):,.2f}
MONTHLY CHILD SUPPORT: ${child_support.get('total_obligation', 0) / 12:,.2f}

{'=' * 70}

4. SPOUSAL MAINTENANCE CALCULATION (DRL §236)
{'-' * 70}

Under the 2015 Maintenance Guidelines:

CALCULATION METHOD: {maintenance.get('calculation_method', 'N/A')}
FORMULA USED: {maintenance.get('formula_used', 'N/A')}

Duration of Marriage: {party_info.get('marriage_years', 0)} years
Income Cap Applied: {'Yes' if maintenance.get('income_cap_applied') else 'No'}

MAINTENANCE AMOUNT:
  Annual Maintenance: ${maintenance.get('maintenance_amount', 0):,.2f}
  Monthly Maintenance: ${maintenance.get('maintenance_amount', 0) / 12:,.2f}

DURATION: {maintenance.get('duration', 'N/A')}

{'=' * 70}

5. COMBINED OBLIGATIONS
{'-' * 70}

                          MONTHLY        ANNUAL
Child Support:           ${child_support.get('total_obligation', 0) / 12:>10,.2f}   ${child_support.get('total_obligation', 0):>12,.2f}
Maintenance:             ${maintenance.get('maintenance_amount', 0) / 12:>10,.2f}   ${maintenance.get('maintenance_amount', 0):>12,.2f}
                         {'-' * 10}   {'-' * 12}
TOTAL:                   ${(child_support.get('total_obligation', 0) + maintenance.get('maintenance_amount', 0)) / 12:>10,.2f}   ${child_support.get('total_obligation', 0) + maintenance.get('maintenance_amount', 0):>12,.2f}

{'=' * 70}

6. DEVIATION FACTORS TO CONSIDER
{'-' * 70}

The court may deviate from guideline calculations based on:

Child Support (DRL §240(1-b)(f)):
  □ Financial resources of parents and child
  □ Physical and emotional health of child
  □ Standard of living child would have enjoyed
  □ Tax consequences
  □ Non-monetary contributions of parents
  □ Educational needs of parents
  □ Disparity in parental incomes
  □ Other children supported by non-custodial parent
  □ Extraordinary expenses for visitation

Maintenance (DRL §236(B)(6)(a)):
  □ Age and health of parties
  □ Present and future earning capacity
  □ Need for training or education
  □ Wasteful dissipation of marital property
  □ Transfer of assets made in contemplation of divorce
  □ Any other factor the court expressly finds just and proper

{'=' * 70}

7. LEGAL REFERENCES
{'-' * 70}

• DRL §240(1-b): Child Support Standards Act
• DRL §236(B)(6): Spousal Maintenance
• 22 NYCRR §202.16(b): Net Worth Statement Requirements
• CSSA Cap (2024): $183,000 combined parental income

{'=' * 70}

                         DISCLAIMER
{'-' * 70}

This analysis is provided for informational purposes and does not
constitute legal advice. Actual support obligations may vary based
on judicial discretion, complete financial disclosure, and other
factors not reflected in this preliminary analysis.

{'=' * 70}

{self.firm_name}
{self.firm_address}
{self.firm_phone}

Report Generated: {report_date}

{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}
"""
        return report

    def generate_financial_summary(self,
                                   case_info: Dict,
                                   documents_analyzed: List[Dict],
                                   discrepancies: List[Dict],
                                   red_flags: List[str]) -> str:
        """Generate a financial document summary report"""

        report_date = datetime.now().strftime("%B %d, %Y")

        report = f"""
{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}

                    FINANCIAL DOCUMENT ANALYSIS SUMMARY

Prepared by: {self.firm_name}
Date: {report_date}
Case: {case_info.get('case_id', 'N/A')}
Client: {case_info.get('client_name', 'N/A')}
Opposing Party: {case_info.get('opposing_party', 'N/A')}

{'=' * 70}

1. DOCUMENTS ANALYZED
{'-' * 70}

"""
        for i, doc in enumerate(documents_analyzed, 1):
            report += f"""
Document {i}: {doc.get('name', 'Unknown')}
  Type: {doc.get('type', 'N/A')}
  Date: {doc.get('date', 'N/A')}
  Source: {doc.get('source', 'N/A')}
"""

        report += f"""
{'=' * 70}

2. DISCREPANCIES IDENTIFIED
{'-' * 70}

"""
        if discrepancies:
            for i, disc in enumerate(discrepancies, 1):
                report += f"""
Discrepancy {i}: {disc.get('type', 'Unknown')}
  Description: {disc.get('description', 'N/A')}
  Amount: ${disc.get('amount', 0):,.2f}
  Significance: {disc.get('significance', 'N/A')}
  Recommendation: {disc.get('recommendation', 'N/A')}
"""
        else:
            report += "No significant discrepancies identified.\n"

        report += f"""
{'=' * 70}

3. RED FLAGS
{'-' * 70}

"""
        if red_flags:
            for flag in red_flags:
                report += f"⚠ {flag}\n"
        else:
            report += "No red flags identified.\n"

        report += f"""
{'=' * 70}

4. RECOMMENDATIONS
{'-' * 70}

Based on this analysis, we recommend:

1. [Further investigation of identified discrepancies]
2. [Subpoena additional records if needed]
3. [Forensic accounting consultation if warranted]

{'=' * 70}

{self.firm_name}
{self.firm_address}
{self.firm_phone}

Report Generated: {report_date}

{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}
"""
        return report

    def generate_case_intake_summary(self,
                                     client_info: Dict,
                                     case_type: str,
                                     financial_overview: Dict,
                                     children_info: List[Dict] = None,
                                     domestic_violence: bool = False) -> str:
        """Generate a case intake summary"""

        report_date = datetime.now().strftime("%B %d, %Y")

        report = f"""
{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}

                         CASE INTAKE SUMMARY

Prepared by: {self.firm_name}
Date: {report_date}
Intake Completed By: ____________________

{'=' * 70}

1. CLIENT INFORMATION
{'-' * 70}

Name: {client_info.get('name', '_' * 30)}
Date of Birth: {client_info.get('dob', '_' * 15)}
Address: {client_info.get('address', '_' * 40)}
Phone: {client_info.get('phone', '_' * 20)}
Email: {client_info.get('email', '_' * 30)}
Employer: {client_info.get('employer', '_' * 30)}

{'=' * 70}

2. CASE TYPE
{'-' * 70}

Primary Matter: {case_type}
"""

        if domestic_violence:
            report += """
⚠️  DOMESTIC VIOLENCE CONSIDERATIONS ⚠️
{'-' * 70}

Safety Planning Required: YES
Confidential Address Program: □ Yes □ No □ Needs Assessment
Order of Protection: □ Existing □ Needed □ Not Applicable
Criminal Case Pending: □ Yes □ No
"""

        report += f"""
{'=' * 70}

3. OPPOSING PARTY INFORMATION
{'-' * 70}

Name: {client_info.get('opposing_name', '_' * 30)}
Date of Birth: {client_info.get('opposing_dob', '_' * 15)}
Address: {client_info.get('opposing_address', '_' * 40)}
Employer: {client_info.get('opposing_employer', '_' * 30)}
Attorney (if known): {client_info.get('opposing_attorney', '_' * 30)}

{'=' * 70}

4. MARRIAGE INFORMATION
{'-' * 70}

Date of Marriage: {client_info.get('marriage_date', '_' * 15)}
Date of Separation: {client_info.get('separation_date', '_' * 15)}
Length of Marriage: {client_info.get('marriage_years', '___')} years
Grounds: □ Irretrievable Breakdown □ Other: ______________

{'=' * 70}

5. CHILDREN
{'-' * 70}

"""
        if children_info:
            for i, child in enumerate(children_info, 1):
                report += f"""
Child {i}:
  Name: {child.get('name', '_' * 25)}
  DOB: {child.get('dob', '_' * 12)} Age: {child.get('age', '___')}
  Residence: {child.get('residence', '_' * 30)}
  Special Needs: □ Yes □ No
  School: {child.get('school', '_' * 30)}
"""
        else:
            report += "□ No minor children\n"

        report += f"""
{'=' * 70}

6. FINANCIAL OVERVIEW
{'-' * 70}

CLIENT INCOME:
  Employment Income: ${financial_overview.get('client_income', 0):,.2f}
  Other Income: ${financial_overview.get('client_other_income', 0):,.2f}

OPPOSING PARTY INCOME (estimated):
  Employment Income: ${financial_overview.get('opposing_income', 0):,.2f}
  Other Income: ${financial_overview.get('opposing_other_income', 0):,.2f}

ASSETS (estimated total):
  Marital Residence: ${financial_overview.get('residence_value', 0):,.2f}
  Retirement Accounts: ${financial_overview.get('retirement', 0):,.2f}
  Bank Accounts: ${financial_overview.get('bank_accounts', 0):,.2f}
  Other Assets: ${financial_overview.get('other_assets', 0):,.2f}

LIABILITIES:
  Mortgage: ${financial_overview.get('mortgage', 0):,.2f}
  Credit Cards: ${financial_overview.get('credit_cards', 0):,.2f}
  Other Debt: ${financial_overview.get('other_debt', 0):,.2f}

{'=' * 70}

7. DOCUMENTS NEEDED
{'-' * 70}

□ Marriage Certificate
□ Birth Certificates (all children)
□ Last 3 years tax returns (both parties)
□ Last 3 months pay stubs (both parties)
□ Bank statements (last 12 months)
□ Retirement account statements
□ Mortgage statement / Deed
□ Vehicle titles/registrations
□ Life insurance policies
□ Health insurance information
□ Prior court orders (if any)
□ Prenuptial/Postnuptial Agreement (if any)

{'=' * 70}

8. INITIAL CASE ASSESSMENT
{'-' * 70}

Complexity Level: □ Low □ Medium □ High
Estimated Duration: _____ months
Urgency: □ Standard □ Expedited □ Emergency

Notes:
________________________________________________________________
________________________________________________________________
________________________________________________________________

{'=' * 70}

{self.firm_name}
{self.firm_address}
{self.firm_phone}

{'=' * 70}
                    CONFIDENTIAL - ATTORNEY WORK PRODUCT
{'=' * 70}
"""
        return report


def create_report_generator(firm_config=None) -> ReportGenerator:
    """Factory function to create report generator"""
    if firm_config:
        return ReportGenerator(
            firm_name=firm_config.firm_name,
            firm_phone=firm_config.phone,
            firm_address=firm_config.address
        )
    return ReportGenerator()
