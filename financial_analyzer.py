#!/usr/bin/env python3
"""
Financial Document Analysis Tool
For New York Family Law Practice
Analyzes: Net Worth Statements, Tax Returns, Bank Statements, Pay Stubs
Identifies: Inconsistencies, Hidden Income, Support Calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import re
import json
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# For PDF parsing (optional)
try:
    import PyPDF2
    from pdf2image import convert_from_path
    import pytesseract
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class SupportType(Enum):
    """Types of support calculations per NY law"""
    CHILD_SUPPORT = "child_support"
    SPOUSAL_SUPPORT = "spousal_support"
    MAINTENANCE = "maintenance"
    TEMPORARY_MAINTENANCE = "pendente_lite"

@dataclass
class FinancialDocument:
    """Base class for financial documents"""
    document_type: str
    source_file: str
    extraction_date: datetime
    raw_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NetWorthStatement:
    """NY Uniform Rule 202.16(b) Net Worth Statement"""
    party_name: str
    preparation_date: str
    assets: Dict[str, float]
    liabilities: Dict[str, float]
    income_sources: Dict[str, float]
    expenses: Dict[str, float]
    marital_property_flag: Dict[str, bool]
    separate_property_flag: Dict[str, bool]

class TaxReturnAnalyzer:
    """Analyzes IRS Form 1040 and related schedules"""

    def __init__(self, tax_year: int):
        self.tax_year = tax_year
        self.income_discrepancy_threshold = 0.10  # 10% variance threshold

    def analyze_1040(self, form_1040: Dict) -> Dict:
        """Analyze Form 1040 for income inconsistencies"""

        analysis = {
            'total_income': 0,
            'adjusted_gross_income': 0,
            'taxable_income': 0,
            'income_sources': {},
            'deductions': {},
            'credits': {},
            'red_flags': []
        }

        # Map common 1040 lines
        line_mapping = {
            'wages': ['1', '7'],  # W-2 income
            'business_income': ['12'],  # Schedule C
            'rental_income': ['17'],  # Schedule E
            'capital_gains': ['13'],  # Schedule D
            'other_income': ['21'],  # Other income
            'adjusted_gross_income': ['37'],
            'taxable_income': ['43']
        }

        # Extract values
        for category, lines in line_mapping.items():
            for line in lines:
                if line in form_1040:
                    value = self._parse_currency(form_1040[line])
                    if value > 0:
                        analysis['income_sources'][f"Line {line}"] = value

        # Check for common red flags
        self._check_for_red_flags(form_1040, analysis)

        return analysis

    def _check_for_red_flags(self, form_1040: Dict, analysis: Dict):
        """Identify potential issues in tax return"""

        # Check for significant business losses
        if '12' in form_1040:
            biz_income = self._parse_currency(form_1040['12'])
            if biz_income < -10000:  # Large business loss
                analysis['red_flags'].append({
                    'type': 'LARGE_BUSINESS_LOSS',
                    'description': f"Significant Schedule C loss: ${abs(biz_income):,.0f}",
                    'concern': 'Potential income shifting or hobby loss'
                })

        # Check for rental real estate losses
        if '17' in form_1040:
            rental_income = self._parse_currency(form_1040['17'])
            if rental_income < -5000:
                analysis['red_flags'].append({
                    'type': 'RENTAL_LOSSES',
                    'description': f"Rental property losses: ${abs(rental_income):,.0f}",
                    'concern': 'May indicate income sheltering'
                })

        # Check for significant "other income" with no explanation
        if '21' in form_1040:
            other_income = self._parse_currency(form_1040['21'])
            if other_income > 5000:
                analysis['red_flags'].append({
                    'type': 'UNEXPLAINED_OTHER_INCOME',
                    'description': f"Significant 'other income': ${other_income:,.0f}",
                    'concern': 'Requires further investigation - source unknown'
                })

    def _parse_currency(self, value: Any) -> float:
        """Parse various currency formats"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove $, commas, parentheses for negatives
            value = value.replace('$', '').replace(',', '').replace('(', '-').replace(')', '')
            try:
                return float(value)
            except:
                return 0.0
        return 0.0

class SupportCalculatorNY:
    """Calculates support amounts per NY Domestic Relations Law and CSSA"""

    def __init__(self):
        # NY Child Support Standards Act percentages (2023)
        self.cssa_percentages = {
            1: 0.17,  # 17%
            2: 0.25,  # 25%
            3: 0.29,  # 29%
            4: 0.31,  # 31%
            5: 0.35   # 35% for 5 or more
        }

        # NY Maintenance (Spousal Support) Guidelines (2023)
        self.maintenance_cap = 203_000  # Income cap for maintenance calculation
        self.maintenance_percentages = {
            'payer': 0.30,  # 30% of payer's income
            'payee': 0.40   # minus 40% of payee's income
        }

    def calculate_child_support(self,
                               payer_income: float,
                               payee_income: float,
                               num_children: int,
                               special_needs: bool = False,
                               health_insurance_cost: float = 0,
                               childcare_cost: float = 0,
                               education_cost: float = 0) -> Dict:
        """
        Calculate child support per NY Child Support Standards Act
        DRL §240(1-b)
        """

        # Apply CSSA percentages
        if num_children >= 5:
            percentage = self.cssa_percentages[5]
        else:
            percentage = self.cssa_percentages.get(num_children, 0.17)

        # Combined parental income (capped at $163,000 for 2023, but court can exceed)
        combined_income = payer_income + payee_income
        basic_support_amount = combined_income * percentage

        # Pro rata share based on income
        payer_share = payer_income / combined_income if combined_income > 0 else 0
        payee_share = payee_income / combined_income if combined_income > 0 else 0

        payer_obligation = basic_support_amount * payer_share

        # Add add-ons (health insurance, childcare, education)
        add_ons = {
            'health_insurance': health_insurance_cost * payer_share,
            'childcare': childcare_cost * payer_share,
            'education': education_cost * payer_share
        }

        total_add_ons = sum(add_ons.values())
        total_obligation = payer_obligation + total_add_ons

        # Apply special needs adjustment (20% increase)
        if special_needs:
            total_obligation *= 1.20

        return {
            'basic_support_amount': round(basic_support_amount, 2),
            'payer_obligation': round(payer_obligation, 2),
            'payee_obligation': round(basic_support_amount - payer_obligation, 2),
            'add_ons': {k: round(v, 2) for k, v in add_ons.items()},
            'total_obligation': round(total_obligation, 2),
            'combined_parental_income': round(combined_income, 2),
            'payer_income_share': round(payer_share * 100, 1),
            'cssa_percentage': percentage,
            'calculation_method': 'NY CSSA'
        }

    def calculate_maintenance(self,
                            payer_income: float,
                            payee_income: float,
                            duration_years: int,
                            pendente_lite: bool = False) -> Dict:
        """
        Calculate maintenance (spousal support) per NY DRL §236
        Applies to cases filed after January 25, 2016
        """

        # Cap income for calculation
        payer_capped = min(payer_income, self.maintenance_cap)
        payee_capped = min(payee_income, self.maintenance_cap)

        # Apply formula: (30% of payer's income) - (40% of payee's income)
        maintenance_amount = (payer_capped * self.maintenance_percentages['payer'] -
                            payee_capped * self.maintenance_percentages['payee'])

        # Ensure non-negative amount
        maintenance_amount = max(0, maintenance_amount)

        # Apply 40% of combined income cap
        combined_capped = payer_capped + payee_capped
        forty_percent_cap = combined_capped * 0.40

        # Final amount is lesser of calculation or 40% cap
        if maintenance_amount + payee_capped > forty_percent_cap:
            maintenance_amount = max(0, forty_percent_cap - payee_capped)

        # Determine duration (per NY guidelines)
        if pendente_lite:
            duration = "Case duration"
        else:
            duration_months = self._calculate_maintenance_duration(duration_years)
            duration = f"{duration_months} months"

        return {
            'maintenance_amount': round(maintenance_amount, 2),
            'duration': duration,
            'payer_income_used': round(payer_capped, 2),
            'payee_income_used': round(payee_capped, 2),
            'calculation_method': 'NY Maintenance Guidelines',
            'income_cap_applied': payer_income > self.maintenance_cap,
            'formula_used': f"({payer_capped} * 30%) - ({payee_capped} * 40%)"
        }

    def _calculate_maintenance_duration(self, marriage_years: int) -> int:
        """Calculate maintenance duration based on length of marriage"""
        if marriage_years <= 15:
            return min(15, marriage_years) * 12  # 15-30% of marriage years
        elif marriage_years <= 20:
            return int(marriage_years * 0.30 * 12)
        elif marriage_years <= 30:
            return int(marriage_years * 0.40 * 12)
        else:
            return int(marriage_years * 0.50 * 12)  # Long-term marriages

class FinancialConsistencyAnalyzer:
    """Analyzes consistency across multiple financial documents"""

    def __init__(self):
        self.discrepancy_threshold = 0.15  # 15% variance
        self.findings = []

    def compare_documents(self,
                         net_worth: NetWorthStatement,
                         tax_return: Dict,
                         pay_stubs: List[Dict],
                         bank_statements: List[Dict]) -> Dict:
        """
        Compare financial information across multiple documents
        to identify inconsistencies
        """

        analysis = {
            'income_comparison': self._compare_income_sources(net_worth, tax_return, pay_stubs),
            'asset_comparison': self._compare_assets(net_worth, bank_statements),
            'expense_analysis': self._analyze_expenses(net_worth, bank_statements),
            'lifestyle_analysis': self._analyze_lifestyle(net_worth, bank_statements),
            'hidden_income_indicators': self._find_hidden_income_indicators(
                net_worth, tax_return, bank_statements
            )
        }

        # Generate overall consistency score
        analysis['consistency_score'] = self._calculate_consistency_score(analysis)
        analysis['recommended_investigations'] = self._generate_investigation_list(analysis)

        return analysis

    def _compare_income_sources(self,
                              net_worth: NetWorthStatement,
                              tax_return: Dict,
                              pay_stubs: List[Dict]) -> Dict:
        """Compare reported income across documents"""

        comparison = {
            'w2_income': {},
            'business_income': {},
            'rental_income': {},
            'other_income': {},
            'discrepancies': []
        }

        # Extract W-2 income from pay stubs
        if pay_stubs:
            annualized_from_stubs = self._annualize_paystubs(pay_stubs)
            comparison['w2_income']['pay_stubs'] = annualized_from_stubs

            # Compare with tax return
            if 'wages' in tax_return.get('income_sources', {}):
                tax_wages = tax_return['income_sources']['wages']
                variance = abs(annualized_from_stubs - tax_wages) / max(tax_wages, 1)

                if variance > self.discrepancy_threshold:
                    comparison['discrepancies'].append({
                        'type': 'WAGE_DISCREPANCY',
                        'source1': f"Pay stubs: ${annualized_from_stubs:,.2f}",
                        'source2': f"Tax return: ${tax_wages:,.2f}",
                        'variance': f"{variance:.1%}",
                        'explanation': 'Reported wages differ significantly'
                    })

        # Check business income consistency
        biz_income_nw = net_worth.income_sources.get('business', 0)
        biz_income_tax = tax_return.get('business_income', 0)

        if biz_income_nw and biz_income_tax:
            variance = abs(biz_income_nw - biz_income_tax) / max(biz_income_tax, 1)
            if variance > self.discrepancy_threshold:
                comparison['discrepancies'].append({
                    'type': 'BUSINESS_INCOME_DISCREPANCY',
                    'source1': f"Net Worth: ${biz_income_nw:,.2f}",
                    'source2': f"Tax return: ${biz_income_tax:,.2f}",
                    'variance': f"{variance:.1%}",
                    'explanation': 'Business income reported differently'
                })

        return comparison

    def _compare_assets(self,
                       net_worth: NetWorthStatement,
                       bank_statements: List[Dict]) -> Dict:
        """Compare reported assets with bank statement evidence"""

        comparison = {
            'reported_assets': {},
            'bank_evidence': {},
            'discrepancies': []
        }

        # Analyze bank account balances
        total_bank_assets = 0
        for statement in bank_statements:
            account_type = statement.get('account_type', 'checking')
            ending_balance = statement.get('ending_balance', 0)
            total_bank_assets += ending_balance

            comparison['bank_evidence'][statement.get('account_name', 'Unknown')] = ending_balance

        # Compare with reported liquid assets
        reported_liquid = sum(
            v for k, v in net_worth.assets.items()
            if any(word in k.lower() for word in ['checking', 'savings', 'cash', 'bank'])
        )

        variance = abs(reported_liquid - total_bank_assets) / max(total_bank_assets, 1)
        if variance > self.discrepancy_threshold and total_bank_assets > 1000:
            comparison['discrepancies'].append({
                'type': 'ASSET_UNDERSTATEMENT',
                'reported': f"${reported_liquid:,.2f}",
                'evidence': f"${total_bank_assets:,.2f}",
                'variance': f"{variance:.1%}",
                'explanation': 'Bank assets exceed reported liquid assets'
            })

        return comparison

    def _analyze_expenses(self,
                         net_worth: NetWorthStatement,
                         bank_statements: List[Dict]) -> Dict:
        """Analyze expenses for lifestyle analysis"""

        analysis = {
            'reported_expenses': net_worth.expenses,
            'actual_spending': {},
            'lifestyle_indicators': [],
            'discrepancies': []
        }

        # Analyze bank statement transactions
        if bank_statements:
            spending_categories = self._categorize_bank_spending(bank_statements)
            analysis['actual_spending'] = spending_categories

            # Compare with reported expenses
            for category, reported_amount in net_worth.expenses.items():
                actual_amount = spending_categories.get(category, 0)
                if reported_amount > 0 and actual_amount > 0:
                    variance = abs(reported_amount - actual_amount) / max(reported_amount, 1)
                    if variance > 0.50:  # 50% variance threshold for expenses
                        analysis['discrepancies'].append({
                            'category': category,
                            'reported': reported_amount,
                            'actual': actual_amount,
                            'variance': f"{variance:.1%}"
                        })

        # Identify luxury spending
        luxury_spending = self._identify_luxury_spending(bank_statements)
        if luxury_spending:
            analysis['lifestyle_indicators'] = luxury_spending

        return analysis

    def _analyze_lifestyle(self,
                          net_worth: NetWorthStatement,
                          bank_statements: List[Dict]) -> Dict:
        """Analyze lifestyle indicators from spending patterns"""

        lifestyle = {
            'luxury_spending': [],
            'recurring_expenses': [],
            'lifestyle_indicators': []
        }

        luxury_spending = self._identify_luxury_spending(bank_statements)
        if luxury_spending:
            lifestyle['luxury_spending'] = luxury_spending

        return lifestyle

    def _find_hidden_income_indicators(self,
                                      net_worth: NetWorthStatement,
                                      tax_return: Dict,
                                      bank_statements: List[Dict]) -> List[Dict]:
        """Look for indicators of hidden income"""

        indicators = []

        # 1. Check for consistent deposits not matching reported income
        if bank_statements:
            regular_deposits = self._analyze_deposit_patterns(bank_statements)
            reported_monthly_income = sum(net_worth.income_sources.values()) / 12

            for deposit_pattern in regular_deposits:
                if deposit_pattern['avg_amount'] * deposit_pattern['frequency'] > reported_monthly_income * 1.2:
                    indicators.append({
                        'type': 'UNEXPLAINED_REGULAR_DEPOSITS',
                        'description': f"Regular deposits of ${deposit_pattern['avg_amount']:,.2f} {deposit_pattern['frequency']} times monthly",
                        'reported_monthly_income': f"${reported_monthly_income:,.2f}",
                        'concern': 'Possible unreported income source'
                    })

        # 2. Check for cash withdrawals that could indicate cash business
        large_cash_withdrawals = self._find_large_cash_withdrawals(bank_statements)
        if large_cash_withdrawals:
            indicators.append({
                'type': 'LARGE_CASH_WITHDRAWALS',
                'description': f"{len(large_cash_withdrawals)} large cash withdrawals totaling ${sum(large_cash_withdrawals):,.2f}",
                'concern': 'Could indicate cash business or hidden assets'
            })

        # 3. Check for transfers to unknown accounts
        unknown_transfers = self._find_unknown_transfers(bank_statements)
        if unknown_transfers:
            indicators.append({
                'type': 'TRANSFERS_TO_UNKNOWN_ACCOUNTS',
                'description': f"Transfers to {len(unknown_transfers)} different unverified accounts",
                'total_amount': f"${sum(t['amount'] for t in unknown_transfers):,.2f}",
                'concern': 'Could be hiding assets in other accounts'
            })

        return indicators

    def _annualize_paystubs(self, pay_stubs: List[Dict]) -> float:
        """Annualize income from pay stub samples"""
        if not pay_stubs:
            return 0

        # Use the most recent pay stub
        latest_stub = max(pay_stubs, key=lambda x: x.get('pay_date', datetime.min))

        gross_pay = latest_stub.get('gross_pay', 0)
        pay_frequency = latest_stub.get('pay_frequency', 'bi-weekly').lower()

        frequency_multipliers = {
            'weekly': 52,
            'bi-weekly': 26,
            'semi-monthly': 24,
            'monthly': 12
        }

        multiplier = frequency_multipliers.get(pay_frequency, 26)  # Default to bi-weekly
        return gross_pay * multiplier

    def _categorize_bank_spending(self, bank_statements: List[Dict]) -> Dict[str, float]:
        """Categorize spending from bank transactions"""
        categories = {
            'housing': 0,
            'transportation': 0,
            'food': 0,
            'entertainment': 0,
            'luxury': 0,
            'utilities': 0,
            'insurance': 0,
            'medical': 0
        }

        # Keywords for categorization
        category_keywords = {
            'housing': ['mortgage', 'rent', 'property tax', 'hoa', 'homeowner'],
            'transportation': ['gas', 'auto', 'car payment', 'insurance', 'repair'],
            'food': ['grocery', 'restaurant', 'dining', 'supermarket'],
            'entertainment': ['netflix', 'spotify', 'movie', 'concert', 'golf'],
            'luxury': ['jewelry', 'designer', 'spa', 'country club', 'vacation'],
            'utilities': ['electric', 'water', 'gas company', 'internet', 'cable'],
            'insurance': ['health insurance', 'life insurance', 'disability'],
            'medical': ['doctor', 'hospital', 'pharmacy', 'dental']
        }

        for statement in bank_statements:
            transactions = statement.get('transactions', [])
            for transaction in transactions:
                description = transaction.get('description', '').lower()
                amount = abs(transaction.get('amount', 0))

                for category, keywords in category_keywords.items():
                    if any(keyword in description for keyword in keywords):
                        categories[category] += amount
                        break

        return categories

    def _identify_luxury_spending(self, bank_statements: List[Dict]) -> List[Dict]:
        """Identify luxury lifestyle indicators"""
        luxury_indicators = []
        luxury_keywords = {
            'high_end_retail': ['tiffany', 'cartier', 'rolex', 'louis vuitton', 'gucci'],
            'luxury_travel': ['first class', 'business class', 'ritz-carlton', 'four seasons'],
            'fine_dining': ['michelin', 'steakhouse', 'fine dining', 'sommelier'],
            'country_clubs': ['country club', 'golf club', 'yacht club', 'tennis club']
        }

        for statement in bank_statements:
            transactions = statement.get('transactions', [])
            for transaction in transactions:
                description = transaction.get('description', '').lower()
                amount = abs(transaction.get('amount', 0))

                for category, keywords in luxury_keywords.items():
                    if any(keyword in description for keyword in keywords) and amount > 500:
                        luxury_indicators.append({
                            'category': category.replace('_', ' ').title(),
                            'description': description[:50],
                            'amount': amount,
                            'date': transaction.get('date', 'Unknown')
                        })

        return luxury_indicators

    def _analyze_deposit_patterns(self, bank_statements: List[Dict]) -> List[Dict]:
        """Analyze deposit patterns for regular income sources"""
        deposits_by_source = {}

        for statement in bank_statements:
            transactions = statement.get('transactions', [])
            for transaction in transactions:
                if transaction.get('amount', 0) > 0:  # Deposits
                    description = transaction.get('description', '').lower()
                    amount = transaction.get('amount', 0)

                    # Categorize deposit source
                    source = 'unknown'
                    if any(word in description for word in ['payroll', 'salary', 'direct deposit']):
                        source = 'payroll'
                    elif any(word in description for word in ['transfer', 'venmo', 'zelle', 'paypal']):
                        source = 'transfer'
                    elif any(word in description for word in ['deposit', 'cash']):
                        source = 'cash_deposit'

                    if source not in deposits_by_source:
                        deposits_by_source[source] = []
                    deposits_by_source[source].append({
                        'amount': amount,
                        'date': transaction.get('date'),
                        'description': description
                    })

        # Analyze patterns
        patterns = []
        for source, deposits in deposits_by_source.items():
            if len(deposits) >= 3:  # Need multiple deposits to establish pattern
                amounts = [d['amount'] for d in deposits]
                avg_amount = np.mean(amounts)
                std_amount = np.std(amounts)

                # If amounts are relatively consistent, it's a pattern
                if std_amount / avg_amount < 0.3:  # Less than 30% variation
                    patterns.append({
                        'source': source,
                        'avg_amount': avg_amount,
                        'frequency': len(deposits) / 3,  # Approx monthly frequency
                        'consistency': f"{(1 - (std_amount / avg_amount)):.1%}"
                    })

        return patterns

    def _find_large_cash_withdrawals(self, bank_statements: List[Dict]) -> List[float]:
        """Find large cash withdrawals (potential for cash hoarding)"""
        large_withdrawals = []
        for statement in bank_statements:
            transactions = statement.get('transactions', [])
            for transaction in transactions:
                amount = transaction.get('amount', 0)
                description = transaction.get('description', '').lower()

                # Look for cash withdrawals over $500
                if amount < -500 and any(word in description for word in ['cash', 'withdrawal', 'atm']):
                    large_withdrawals.append(abs(amount))

        return large_withdrawals

    def _find_unknown_transfers(self, bank_statements: List[Dict]) -> List[Dict]:
        """Find transfers to accounts not disclosed in net worth statement"""
        unknown_transfers = []
        known_accounts = ['chase', 'bank of america', 'citibank', 'wells fargo']  # Would come from net worth

        for statement in bank_statements:
            transactions = statement.get('transactions', [])
            for transaction in transactions:
                amount = transaction.get('amount', 0)
                description = transaction.get('description', '').lower()

                # Look for transfers
                if amount < 0 and any(word in description for word in ['transfer', 'to account']):
                    # Check if transfer is to known account
                    if not any(known in description for known in known_accounts):
                        unknown_transfers.append({
                            'amount': abs(amount),
                            'description': description,
                            'date': transaction.get('date', 'Unknown')
                        })

        return unknown_transfers

    def _calculate_consistency_score(self, analysis: Dict) -> float:
        """Calculate overall consistency score (0-100)"""
        base_score = 100

        # Deduct for discrepancies
        for category in ['income_comparison', 'asset_comparison', 'expense_analysis']:
            discrepancies = analysis.get(category, {}).get('discrepancies', [])
            base_score -= len(discrepancies) * 5

        # Deduct for hidden income indicators
        hidden_indicators = analysis.get('hidden_income_indicators', [])
        base_score -= len(hidden_indicators) * 10

        return max(0, min(100, base_score))

    def _generate_investigation_list(self, analysis: Dict) -> List[str]:
        """Generate list of recommended investigations"""
        investigations = []

        # Based on discrepancies
        for category in ['income_comparison', 'asset_comparison', 'expense_analysis']:
            for discrepancy in analysis.get(category, {}).get('discrepancies', []):
                investigations.append(
                    f"Investigate {discrepancy['type'].replace('_', ' ').lower()}: "
                    f"{discrepancy.get('explanation', '')}"
                )

        # Based on hidden income indicators
        for indicator in analysis.get('hidden_income_indicators', []):
            investigations.append(
                f"Follow up on {indicator['type'].replace('_', ' ').lower()}: "
                f"{indicator.get('concern', '')}"
            )

        # Standard investigations
        if analysis.get('lifestyle_analysis', {}).get('lifestyle_indicators'):
            investigations.append(
                "Conduct lifestyle analysis to compare reported income with actual spending"
            )

        if analysis.get('consistency_score', 100) < 70:
            investigations.append(
                "Consider forensic accounting due to significant inconsistencies"
            )

        return investigations[:10]  # Limit to top 10

class FinancialDocumentReportGenerator:
    """Generates comprehensive analysis reports"""

    def generate_report(self,
                       party_name: str,
                       net_worth: NetWorthStatement,
                       support_calculations: Dict,
                       consistency_analysis: Dict,
                       hidden_income_indicators: List[Dict]) -> str:
        """Generate a detailed financial analysis report"""

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(f"FINANCIAL DOCUMENT ANALYSIS REPORT")
        report_lines.append(f"Party: {party_name}")
        report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append("=" * 80)
        report_lines.append("")

        # Executive Summary
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 40)

        consistency_score = consistency_analysis.get('consistency_score', 0)
        if consistency_score >= 80:
            rating = "HIGH"
        elif consistency_score >= 60:
            rating = "MODERATE"
        else:
            rating = "LOW"

        report_lines.append(f"Document Consistency: {rating} ({consistency_score}/100)")

        num_discrepancies = sum(
            len(consistency_analysis.get(cat, {}).get('discrepancies', []))
            for cat in ['income_comparison', 'asset_comparison', 'expense_analysis']
        )
        report_lines.append(f"Financial Discrepancies Found: {num_discrepancies}")
        report_lines.append(f"Hidden Income Indicators: {len(hidden_income_indicators)}")
        report_lines.append("")

        # Support Calculations
        if support_calculations:
            report_lines.append("SUPPORT CALCULATIONS")
            report_lines.append("-" * 40)

            for support_type, calc in support_calculations.items():
                report_lines.append(f"\n{support_type.replace('_', ' ').upper()}:")
                for key, value in calc.items():
                    if isinstance(value, (int, float)) and key != 'cssa_percentage':
                        report_lines.append(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")
                    elif key == 'cssa_percentage':
                        report_lines.append(f"  CSSA Percentage: {value:.1%}")
                    elif key == 'duration':
                        report_lines.append(f"  Duration: {value}")
                    elif isinstance(value, str):
                        report_lines.append(f"  {key.replace('_', ' ').title()}: {value}")

            report_lines.append("")

        # Financial Discrepancies
        report_lines.append("FINANCIAL DISCREPANCIES")
        report_lines.append("-" * 40)

        for category in ['income_comparison', 'asset_comparison', 'expense_analysis']:
            discrepancies = consistency_analysis.get(category, {}).get('discrepancies', [])
            if discrepancies:
                report_lines.append(f"\n{category.replace('_', ' ').title()}:")
                for disc in discrepancies:
                    report_lines.append(f"  • {disc.get('type', 'Unknown')}:")
                    report_lines.append(f"    {disc.get('explanation', '')}")
                    if 'variance' in disc:
                        report_lines.append(f"    Variance: {disc['variance']}")

        if not any(consistency_analysis.get(cat, {}).get('discrepancies') for cat in
                  ['income_comparison', 'asset_comparison', 'expense_analysis']):
            report_lines.append("No significant discrepancies found.")

        report_lines.append("")

        # Hidden Income Analysis
        if hidden_income_indicators:
            report_lines.append("HIDDEN INCOME INDICATORS")
            report_lines.append("-" * 40)

            for indicator in hidden_income_indicators:
                report_lines.append(f"\n• {indicator.get('type', 'Unknown').replace('_', ' ').title()}:")
                report_lines.append(f"  {indicator.get('description', '')}")
                report_lines.append(f"  Concern: {indicator.get('concern', '')}")

        # Recommended Actions
        report_lines.append("\nRECOMMENDED ACTIONS")
        report_lines.append("-" * 40)

        investigations = consistency_analysis.get('recommended_investigations', [])
        if investigations:
            for i, investigation in enumerate(investigations[:5], 1):
                report_lines.append(f"{i}. {investigation}")
        else:
            report_lines.append("No specific investigations recommended at this time.")

        # Legal Considerations
        report_lines.append("\nLEGAL CONSIDERATIONS (NY SPECIFIC)")
        report_lines.append("-" * 40)

        if consistency_score < 70:
            report_lines.append("• Consider filing motion to compel more complete discovery")
            report_lines.append("• May need forensic accountant for asset tracing")
            report_lines.append("• Document all inconsistencies for potential impeachment at trial")

        if hidden_income_indicators:
            report_lines.append("• Subpoena additional bank/business records")
            report_lines.append("• Consider deposition of accountant/business manager")
            report_lines.append("• Request authorization for asset search services")

        # Net Worth Summary
        report_lines.append("\nNET WORTH SUMMARY")
        report_lines.append("-" * 40)

        total_assets = sum(net_worth.assets.values())
        total_liabilities = sum(net_worth.liabilities.values())
        net_worth_value = total_assets - total_liabilities

        report_lines.append(f"Total Assets: ${total_assets:,.2f}")
        report_lines.append(f"Total Liabilities: ${total_liabilities:,.2f}")
        report_lines.append(f"Net Worth: ${net_worth_value:,.2f}")
        report_lines.append(f"Annual Income: ${sum(net_worth.income_sources.values()):,.2f}")

        # Addendum with calculation details
        report_lines.append("\n" + "=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)

def main():
    """Demo the financial document analysis tool"""

    print("=" * 80)
    print("FINANCIAL DOCUMENT ANALYSIS TOOL - NEW YORK FAMILY LAW")
    print("=" * 80)

    # Create sample net worth statement
    sample_net_worth = NetWorthStatement(
        party_name="John Smith",
        preparation_date="2023-11-01",
        assets={
            'checking_account': 15000,
            'savings_account': 50000,
            'retirement_401k': 250000,
            'home_equity': 200000,
            'vehicle': 35000,
            'investment_accounts': 100000
        },
        liabilities={
            'mortgage': 350000,
            'auto_loan': 25000,
            'credit_cards': 8000,
            'student_loans': 45000
        },
        income_sources={
            'salary': 150000,
            'bonus': 25000,
            'rental': 12000,
            'business': 0
        },
        expenses={
            'housing': 3500,
            'transportation': 800,
            'food': 1200,
            'utilities': 400,
            'entertainment': 500,
            'medical': 200,
            'insurance': 600
        },
        marital_property_flag={
            'checking_account': True,
            'savings_account': True,
            'retirement_401k': True,
            'home_equity': True
        },
        separate_property_flag={
            'investment_accounts': True  # Pre-marital inheritance
        }
    )

    # Sample tax return data
    sample_tax_return = {
        '1': 155000,  # Wages
        '12': -5000,  # Business loss
        '17': 12000,  # Rental income
        '21': 8000,   # Other income
        'income_sources': {
            'wages': 155000,
            'business': -5000,
            'rental': 12000,
            'other': 8000
        }
    }

    # Sample pay stubs
    sample_pay_stubs = [
        {
            'pay_date': datetime(2023, 10, 15),
            'gross_pay': 5769.23,
            'net_pay': 4100.00,
            'pay_frequency': 'bi-weekly',
            'employer': 'ABC Corporation'
        },
        {
            'pay_date': datetime(2023, 10, 1),
            'gross_pay': 5769.23,
            'net_pay': 4100.00,
            'pay_frequency': 'bi-weekly',
            'employer': 'ABC Corporation'
        }
    ]

    # Sample bank statements
    sample_bank_statements = [
        {
            'account_name': 'Chase Checking',
            'account_type': 'checking',
            'statement_date': datetime(2023, 10, 31),
            'beginning_balance': 12000,
            'ending_balance': 18500,
            'transactions': [
                {'date': '2023-10-15', 'description': 'Direct Deposit - ABC Corp', 'amount': 4100},
                {'date': '2023-10-01', 'description': 'Direct Deposit - ABC Corp', 'amount': 4100},
                {'date': '2023-10-05', 'description': 'Zelle Transfer Received', 'amount': 2500},
                {'date': '2023-10-10', 'description': 'Mortgage Payment', 'amount': -3500},
                {'date': '2023-10-12', 'description': 'ATM Cash Withdrawal', 'amount': -800},
                {'date': '2023-10-18', 'description': 'Country Club Dues', 'amount': -750},
                {'date': '2023-10-20', 'description': 'Louis Vuitton', 'amount': -1200},
                {'date': '2023-10-25', 'description': 'Transfer to External Account', 'amount': -3000}
            ]
        }
    ]

    print("\n1. ANALYZING NET WORTH STATEMENT...")
    print("-" * 40)

    # Initialize analyzers
    tax_analyzer = TaxReturnAnalyzer(2023)
    support_calculator = SupportCalculatorNY()
    consistency_analyzer = FinancialConsistencyAnalyzer()
    report_generator = FinancialDocumentReportGenerator()

    # Analyze tax return
    print("\n2. ANALYZING TAX RETURN...")
    print("-" * 40)
    tax_analysis = tax_analyzer.analyze_1040(sample_tax_return)

    if tax_analysis['red_flags']:
        print("RED FLAGS IDENTIFIED:")
        for flag in tax_analysis['red_flags']:
            print(f"  • {flag['type']}: {flag['description']}")
            print(f"    Concern: {flag['concern']}")

    # Calculate support
    print("\n3. CALCULATING SUPPORT AMOUNTS...")
    print("-" * 40)

    child_support = support_calculator.calculate_child_support(
        payer_income=175000,  # Total income
        payee_income=65000,
        num_children=2,
        health_insurance_cost=6000,
        childcare_cost=18000
    )

    print(f"Child Support Calculation (2 children):")
    print(f"  Combined Parental Income: ${child_support['combined_parental_income']:,.2f}")
    print(f"  CSSA Percentage: {child_support['cssa_percentage']:.0%}")
    print(f"  Payer's Income Share: {child_support['payer_income_share']:.1f}%")
    print(f"  Basic Support Amount: ${child_support['basic_support_amount']:,.2f}")
    print(f"  Payer's Obligation: ${child_support['payer_obligation']:,.2f}")
    print(f"  Add-ons (health, childcare): ${sum(child_support['add_ons'].values()):,.2f}")
    print(f"  TOTAL MONTHLY OBLIGATION: ${child_support['total_obligation']:,.2f}")

    maintenance = support_calculator.calculate_maintenance(
        payer_income=175000,
        payee_income=65000,
        duration_years=15
    )

    print(f"\nMaintenance Calculation (15-year marriage):")
    print(f"  Monthly Amount: ${maintenance['maintenance_amount']:,.2f}")
    print(f"  Duration: {maintenance['duration']}")
    print(f"  Formula: {maintenance['formula_used']}")

    # Cross-document consistency analysis
    print("\n4. CROSS-DOCUMENT CONSISTENCY ANALYSIS...")
    print("-" * 40)

    consistency_results = consistency_analyzer.compare_documents(
        net_worth=sample_net_worth,
        tax_return=tax_analysis,
        pay_stubs=sample_pay_stubs,
        bank_statements=sample_bank_statements
    )

    print(f"Consistency Score: {consistency_results['consistency_score']}/100")

    if consistency_results.get('hidden_income_indicators'):
        print("\nHIDDEN INCOME INDICATORS:")
        for indicator in consistency_results['hidden_income_indicators']:
            print(f"  • {indicator['type']}")
            print(f"    {indicator['description']}")
            print(f"    Concern: {indicator['concern']}")

    # Generate full report
    print("\n5. GENERATING COMPREHENSIVE REPORT...")
    print("-" * 40)

    full_report = report_generator.generate_report(
        party_name="John Smith",
        net_worth=sample_net_worth,
        support_calculations={
            'child_support': child_support,
            'maintenance': maintenance
        },
        consistency_analysis=consistency_results,
        hidden_income_indicators=consistency_results.get('hidden_income_indicators', [])
    )

    print(full_report)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
