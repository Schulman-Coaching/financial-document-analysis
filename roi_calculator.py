#!/usr/bin/env python3
"""
ROI Calculator and Business Case for Family Law Practice Automation
Demonstrates cost savings and efficiency gains from the platform
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class ParalegalCosts:
    """Industry standard paralegal costs in NY"""
    hourly_rate: float = 35.0  # Average paralegal hourly wage in NY
    billing_rate: float = 150.0  # What firm bills clients for paralegal time
    benefits_multiplier: float = 1.3  # Benefits add ~30% to base wage
    annual_hours: int = 2080  # Full-time hours

    @property
    def fully_loaded_hourly(self) -> float:
        """Total cost per hour including benefits"""
        return self.hourly_rate * self.benefits_multiplier

    @property
    def annual_cost(self) -> float:
        """Total annual cost for one paralegal"""
        return self.fully_loaded_hourly * self.annual_hours


@dataclass
class TaskTimeEstimates:
    """Time estimates for common paralegal tasks (in minutes)"""
    # Document Preparation
    net_worth_statement_manual: int = 180  # 3 hours to prepare from scratch
    net_worth_statement_automated: int = 30  # 30 min with platform

    verified_complaint_manual: int = 120  # 2 hours
    verified_complaint_automated: int = 20  # 20 min

    child_support_worksheet_manual: int = 90  # 1.5 hours
    child_support_worksheet_automated: int = 10  # 10 min (auto-calculated)

    stipulation_settlement_manual: int = 240  # 4 hours
    stipulation_settlement_automated: int = 45  # 45 min

    family_offense_petition_manual: int = 90  # 1.5 hours
    family_offense_petition_automated: int = 20  # 20 min

    # Financial Analysis
    tax_return_analysis_manual: int = 120  # 2 hours per return
    tax_return_analysis_automated: int = 15  # 15 min with OCR + analysis

    bank_statement_review_manual: int = 60  # 1 hour per 3-month period
    bank_statement_review_automated: int = 10  # 10 min

    income_verification_manual: int = 90  # 1.5 hours
    income_verification_automated: int = 15  # 15 min

    hidden_income_detection_manual: int = 180  # 3 hours (often missed)
    hidden_income_detection_automated: int = 20  # 20 min with algorithms

    # Case Management
    case_intake_manual: int = 45  # 45 min per new case
    case_intake_automated: int = 15  # 15 min with guided workflow

    document_organization_manual: int = 30  # 30 min per case update
    document_organization_automated: int = 5  # 5 min with auto-filing

    deadline_tracking_manual: int = 15  # 15 min daily checking
    deadline_tracking_automated: int = 2  # 2 min reviewing alerts

    # Support Calculations
    child_support_calculation_manual: int = 45  # 45 min
    child_support_calculation_automated: int = 5  # 5 min

    maintenance_calculation_manual: int = 45  # 45 min
    maintenance_calculation_automated: int = 5  # 5 min


@dataclass
class CaseVolume:
    """Typical case volumes for a small family law practice"""
    new_cases_per_month: int = 8
    active_cases: int = 45
    documents_per_case: int = 12
    financial_docs_per_case: int = 8
    court_filings_per_case: int = 6


@dataclass
class ROIAnalysis:
    """Complete ROI analysis results"""
    monthly_time_saved_hours: float
    monthly_cost_saved: float
    annual_cost_saved: float
    paralegal_fte_equivalent: float
    roi_percentage: float
    payback_period_months: float
    efficiency_gain_percentage: float
    tasks_automated: Dict[str, Dict]


class ROICalculator:
    """Calculate ROI for law firm automation platform"""

    def __init__(self):
        self.paralegal_costs = ParalegalCosts()
        self.task_times = TaskTimeEstimates()
        self.case_volume = CaseVolume()

    def calculate_monthly_time_savings(self) -> Dict[str, Dict]:
        """Calculate time savings per task category"""

        tasks = {}

        # Document Preparation (per case, multiplied by new cases)
        new_cases = self.case_volume.new_cases_per_month

        tasks['Net Worth Statements'] = {
            'manual_minutes': self.task_times.net_worth_statement_manual * new_cases,
            'automated_minutes': self.task_times.net_worth_statement_automated * new_cases,
            'savings_minutes': (self.task_times.net_worth_statement_manual -
                              self.task_times.net_worth_statement_automated) * new_cases,
            'frequency': f'{new_cases} per month'
        }

        tasks['Verified Complaints'] = {
            'manual_minutes': self.task_times.verified_complaint_manual * new_cases,
            'automated_minutes': self.task_times.verified_complaint_automated * new_cases,
            'savings_minutes': (self.task_times.verified_complaint_manual -
                              self.task_times.verified_complaint_automated) * new_cases,
            'frequency': f'{new_cases} per month'
        }

        tasks['Child Support Worksheets'] = {
            'manual_minutes': self.task_times.child_support_worksheet_manual * new_cases,
            'automated_minutes': self.task_times.child_support_worksheet_automated * new_cases,
            'savings_minutes': (self.task_times.child_support_worksheet_manual -
                              self.task_times.child_support_worksheet_automated) * new_cases,
            'frequency': f'{new_cases} per month'
        }

        # Financial Analysis (per case with financial docs)
        financial_reviews = new_cases * 2  # Assume 2 reviews per new case

        tasks['Tax Return Analysis'] = {
            'manual_minutes': self.task_times.tax_return_analysis_manual * financial_reviews,
            'automated_minutes': self.task_times.tax_return_analysis_automated * financial_reviews,
            'savings_minutes': (self.task_times.tax_return_analysis_manual -
                              self.task_times.tax_return_analysis_automated) * financial_reviews,
            'frequency': f'{financial_reviews} per month'
        }

        tasks['Bank Statement Review'] = {
            'manual_minutes': self.task_times.bank_statement_review_manual * financial_reviews * 2,
            'automated_minutes': self.task_times.bank_statement_review_automated * financial_reviews * 2,
            'savings_minutes': (self.task_times.bank_statement_review_manual -
                              self.task_times.bank_statement_review_automated) * financial_reviews * 2,
            'frequency': f'{financial_reviews * 2} per month'
        }

        tasks['Hidden Income Detection'] = {
            'manual_minutes': self.task_times.hidden_income_detection_manual * new_cases,
            'automated_minutes': self.task_times.hidden_income_detection_automated * new_cases,
            'savings_minutes': (self.task_times.hidden_income_detection_manual -
                              self.task_times.hidden_income_detection_automated) * new_cases,
            'frequency': f'{new_cases} per month'
        }

        # Support Calculations
        support_calcs = new_cases * 3  # Multiple iterations per case

        tasks['Support Calculations'] = {
            'manual_minutes': (self.task_times.child_support_calculation_manual +
                             self.task_times.maintenance_calculation_manual) * support_calcs,
            'automated_minutes': (self.task_times.child_support_calculation_automated +
                                self.task_times.maintenance_calculation_automated) * support_calcs,
            'savings_minutes': ((self.task_times.child_support_calculation_manual +
                               self.task_times.maintenance_calculation_manual) -
                              (self.task_times.child_support_calculation_automated +
                               self.task_times.maintenance_calculation_automated)) * support_calcs,
            'frequency': f'{support_calcs} per month'
        }

        # Case Management (ongoing for all active cases)
        active = self.case_volume.active_cases
        work_days = 22  # Per month

        tasks['Case Intake'] = {
            'manual_minutes': self.task_times.case_intake_manual * new_cases,
            'automated_minutes': self.task_times.case_intake_automated * new_cases,
            'savings_minutes': (self.task_times.case_intake_manual -
                              self.task_times.case_intake_automated) * new_cases,
            'frequency': f'{new_cases} per month'
        }

        tasks['Document Organization'] = {
            'manual_minutes': self.task_times.document_organization_manual * active,
            'automated_minutes': self.task_times.document_organization_automated * active,
            'savings_minutes': (self.task_times.document_organization_manual -
                              self.task_times.document_organization_automated) * active,
            'frequency': f'{active} cases/month'
        }

        tasks['Deadline Tracking'] = {
            'manual_minutes': self.task_times.deadline_tracking_manual * work_days,
            'automated_minutes': self.task_times.deadline_tracking_automated * work_days,
            'savings_minutes': (self.task_times.deadline_tracking_manual -
                              self.task_times.deadline_tracking_automated) * work_days,
            'frequency': f'{work_days} days/month'
        }

        return tasks

    def calculate_full_roi(self, platform_monthly_cost: float = 1500) -> ROIAnalysis:
        """Calculate complete ROI analysis"""

        tasks = self.calculate_monthly_time_savings()

        # Total time savings
        total_savings_minutes = sum(t['savings_minutes'] for t in tasks.values())
        total_savings_hours = total_savings_minutes / 60

        # Cost savings
        hourly_cost = self.paralegal_costs.fully_loaded_hourly
        monthly_cost_saved = total_savings_hours * hourly_cost
        annual_cost_saved = monthly_cost_saved * 12

        # FTE equivalent
        monthly_work_hours = self.paralegal_costs.annual_hours / 12
        fte_equivalent = total_savings_hours / monthly_work_hours

        # ROI calculation
        annual_platform_cost = platform_monthly_cost * 12
        net_annual_savings = annual_cost_saved - annual_platform_cost
        roi_percentage = (net_annual_savings / annual_platform_cost) * 100

        # Payback period
        if monthly_cost_saved > platform_monthly_cost:
            payback_months = platform_monthly_cost / (monthly_cost_saved - platform_monthly_cost)
        else:
            payback_months = float('inf')

        # Efficiency gain
        total_manual_minutes = sum(t['manual_minutes'] for t in tasks.values())
        total_automated_minutes = sum(t['automated_minutes'] for t in tasks.values())
        efficiency_gain = ((total_manual_minutes - total_automated_minutes) /
                          total_manual_minutes) * 100

        return ROIAnalysis(
            monthly_time_saved_hours=total_savings_hours,
            monthly_cost_saved=monthly_cost_saved,
            annual_cost_saved=annual_cost_saved,
            paralegal_fte_equivalent=fte_equivalent,
            roi_percentage=roi_percentage,
            payback_period_months=payback_months,
            efficiency_gain_percentage=efficiency_gain,
            tasks_automated=tasks
        )

    def generate_pricing_recommendation(self) -> Dict:
        """Generate pricing recommendation based on value delivered"""

        roi_at_1000 = self.calculate_full_roi(1000)
        roi_at_1500 = self.calculate_full_roi(1500)
        roi_at_2000 = self.calculate_full_roi(2000)

        # Value-based pricing: capture 20-30% of value created
        annual_value = roi_at_1500.annual_cost_saved

        recommended_monthly = annual_value * 0.25 / 12  # 25% of annual savings

        return {
            'recommended_monthly_price': round(recommended_monthly, -1),  # Round to nearest $10
            'value_delivered_annually': annual_value,
            'recommended_capture_rate': '25%',
            'pricing_tiers': {
                'starter': {
                    'price': 999,
                    'roi_percentage': roi_at_1000.roi_percentage,
                    'payback_months': roi_at_1000.payback_period_months,
                    'features': ['Document Templates', 'Support Calculator', 'Basic Reports']
                },
                'professional': {
                    'price': 1499,
                    'roi_percentage': roi_at_1500.roi_percentage,
                    'payback_months': roi_at_1500.payback_period_months,
                    'features': ['All Starter features', 'OCR Document Scanning',
                               'Google Drive Integration', 'Financial Analysis']
                },
                'enterprise': {
                    'price': 2499,
                    'roi_percentage': roi_at_2000.roi_percentage,
                    'payback_months': roi_at_2000.payback_period_months,
                    'features': ['All Professional features', 'Case Management',
                               'Deadline Tracking', 'Custom Branding', 'Priority Support']
                }
            },
            'one_time_alternative': {
                'setup_fee': 5000,
                'monthly_support': 299,
                'total_year_1': 5000 + (299 * 12),
                'note': 'Lower ongoing cost but higher upfront investment'
            }
        }

    def generate_comparison_table(self) -> str:
        """Generate before/after comparison for sales pitch"""

        tasks = self.calculate_monthly_time_savings()

        table = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    PARALEGAL TIME COMPARISON (MONTHLY)                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Task                        │ Manual Time │ With Platform │ Time Saved │ %    ║
╠═════════════════════════════╪═════════════╪═══════════════╪════════════╪══════╣
"""

        for task_name, data in tasks.items():
            manual_hrs = data['manual_minutes'] / 60
            auto_hrs = data['automated_minutes'] / 60
            saved_hrs = data['savings_minutes'] / 60
            pct = (data['savings_minutes'] / data['manual_minutes']) * 100 if data['manual_minutes'] > 0 else 0

            table += f"║ {task_name:<27} │ {manual_hrs:>6.1f} hrs  │ {auto_hrs:>8.1f} hrs  │ {saved_hrs:>6.1f} hrs │ {pct:>3.0f}% ║\n"

        # Totals
        total_manual = sum(t['manual_minutes'] for t in tasks.values()) / 60
        total_auto = sum(t['automated_minutes'] for t in tasks.values()) / 60
        total_saved = sum(t['savings_minutes'] for t in tasks.values()) / 60
        total_pct = (total_saved / total_manual) * 100

        table += """╠═════════════════════════════╪═════════════╪═══════════════╪════════════╪══════╣
"""
        table += f"║ {'TOTAL':<27} │ {total_manual:>6.1f} hrs  │ {total_auto:>8.1f} hrs  │ {total_saved:>6.1f} hrs │ {total_pct:>3.0f}% ║\n"
        table += """╚═══════════════════════════════════════════════════════════════════════════════╝
"""

        return table


@dataclass
class TimeEntry:
    """Track time spent on tasks for ROI demonstration"""
    task_id: str
    task_type: str
    case_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    automated: bool = True
    notes: str = ""


class TimeTracker:
    """Track actual time spent to demonstrate ROI"""

    def __init__(self):
        self.entries: List[TimeEntry] = []
        self.manual_benchmarks = TaskTimeEstimates()

    def start_task(self, task_type: str, case_id: str, notes: str = "") -> str:
        """Start tracking a new task"""
        task_id = f"{task_type}_{case_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        entry = TimeEntry(
            task_id=task_id,
            task_type=task_type,
            case_id=case_id,
            start_time=datetime.now(),
            notes=notes
        )

        self.entries.append(entry)
        return task_id

    def end_task(self, task_id: str) -> Optional[TimeEntry]:
        """End tracking for a task"""
        for entry in self.entries:
            if entry.task_id == task_id and entry.end_time is None:
                entry.end_time = datetime.now()
                entry.duration_minutes = int(
                    (entry.end_time - entry.start_time).total_seconds() / 60
                )
                return entry
        return None

    def get_time_saved_report(self) -> Dict:
        """Generate report showing time saved vs manual methods"""

        completed = [e for e in self.entries if e.duration_minutes is not None]

        if not completed:
            return {'error': 'No completed tasks to analyze'}

        task_summaries = {}

        for entry in completed:
            if entry.task_type not in task_summaries:
                task_summaries[entry.task_type] = {
                    'count': 0,
                    'total_automated_minutes': 0,
                    'total_manual_estimate': 0
                }

            task_summaries[entry.task_type]['count'] += 1
            task_summaries[entry.task_type]['total_automated_minutes'] += entry.duration_minutes

            # Get manual benchmark
            manual_time = getattr(self.manual_benchmarks,
                                 f"{entry.task_type}_manual", 60)
            task_summaries[entry.task_type]['total_manual_estimate'] += manual_time

        # Calculate savings
        total_automated = sum(t['total_automated_minutes'] for t in task_summaries.values())
        total_manual = sum(t['total_manual_estimate'] for t in task_summaries.values())
        total_saved = total_manual - total_automated

        return {
            'tasks_completed': len(completed),
            'total_automated_time_minutes': total_automated,
            'estimated_manual_time_minutes': total_manual,
            'time_saved_minutes': total_saved,
            'time_saved_hours': total_saved / 60,
            'efficiency_improvement': f"{(total_saved / total_manual) * 100:.1f}%",
            'task_breakdown': task_summaries
        }


def create_roi_calculator() -> ROICalculator:
    """Factory function"""
    return ROICalculator()


def create_time_tracker() -> TimeTracker:
    """Factory function"""
    return TimeTracker()
