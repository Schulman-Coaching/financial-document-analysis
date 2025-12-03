#!/usr/bin/env python3
"""
Case Management System for Family Law Practice
Tracks cases, deadlines, documents, and tasks
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class CaseStatus(Enum):
    INTAKE = "Intake"
    ACTIVE = "Active"
    DISCOVERY = "Discovery"
    NEGOTIATION = "Negotiation"
    TRIAL_PREP = "Trial Preparation"
    TRIAL = "Trial"
    SETTLEMENT = "Settlement"
    CLOSED = "Closed"
    ON_HOLD = "On Hold"


class CaseType(Enum):
    CONTESTED_DIVORCE = "Contested Divorce"
    UNCONTESTED_DIVORCE = "Uncontested Divorce"
    CUSTODY = "Custody/Visitation"
    CHILD_SUPPORT = "Child Support"
    MODIFICATION = "Modification"
    ENFORCEMENT = "Enforcement"
    DOMESTIC_VIOLENCE = "Domestic Violence/Order of Protection"
    PATERNITY = "Paternity"


class DeadlineType(Enum):
    COURT_DATE = "Court Date"
    FILING_DEADLINE = "Filing Deadline"
    DISCOVERY_DUE = "Discovery Due"
    RESPONSE_DUE = "Response Due"
    MOTION_RETURN = "Motion Return Date"
    CONFERENCE = "Conference"
    DEPOSITION = "Deposition"
    STATUTE_OF_LIMITATIONS = "Statute of Limitations"
    INTERNAL = "Internal Deadline"


class TaskPriority(Enum):
    URGENT = "Urgent"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"


@dataclass
class Deadline:
    """A deadline or court date"""
    id: str
    case_id: str
    title: str
    deadline_type: str
    due_date: str
    due_time: str = ""
    location: str = ""
    notes: str = ""
    reminder_days: List[int] = field(default_factory=lambda: [7, 3, 1])
    completed: bool = False
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def days_until_due(self) -> int:
        """Calculate days until deadline"""
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        return (due - datetime.now()).days

    @property
    def is_overdue(self) -> bool:
        """Check if deadline is past"""
        return self.days_until_due < 0 and not self.completed

    @property
    def urgency_level(self) -> str:
        """Get urgency level based on days remaining"""
        days = self.days_until_due
        if days < 0:
            return "OVERDUE"
        elif days <= 1:
            return "CRITICAL"
        elif days <= 3:
            return "URGENT"
        elif days <= 7:
            return "APPROACHING"
        else:
            return "SCHEDULED"


@dataclass
class Task:
    """A task to be completed"""
    id: str
    case_id: str
    title: str
    description: str = ""
    priority: str = "Medium"
    status: str = "Pending"
    assigned_to: str = ""
    due_date: str = ""
    estimated_minutes: int = 30
    actual_minutes: int = 0
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_date: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class CaseNote:
    """A note or update on a case"""
    id: str
    case_id: str
    content: str
    author: str
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    note_type: str = "General"  # General, Phone Call, Email, Court, Meeting
    is_privileged: bool = False


@dataclass
class Case:
    """A family law case"""
    id: str
    case_number: str  # Court index number
    client_name: str
    opposing_party: str
    case_type: str
    status: str
    court: str
    county: str
    judge: str = ""
    attorney: str = ""
    paralegal: str = ""
    open_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    close_date: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    deadlines: List[str] = field(default_factory=list)  # List of deadline IDs
    tasks: List[str] = field(default_factory=list)  # List of task IDs
    documents: List[str] = field(default_factory=list)  # List of document IDs
    notes: List[str] = field(default_factory=list)  # List of note IDs
    related_cases: List[str] = field(default_factory=list)

    # Financial summary
    retainer_amount: float = 0.0
    retainer_balance: float = 0.0
    total_billed: float = 0.0

    # Key dates
    marriage_date: str = ""
    separation_date: str = ""
    filing_date: str = ""

    # Children
    children: List[Dict] = field(default_factory=list)


class CaseManager:
    """Manage all cases, deadlines, and tasks"""

    def __init__(self, data_file: str = "case_data.json"):
        self.data_file = data_file
        self.cases: Dict[str, Case] = {}
        self.deadlines: Dict[str, Deadline] = {}
        self.tasks: Dict[str, Task] = {}
        self.notes: Dict[str, CaseNote] = {}
        self._load_data()

    def _load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)

                for case_id, case_data in data.get('cases', {}).items():
                    self.cases[case_id] = Case(**case_data)

                for dl_id, dl_data in data.get('deadlines', {}).items():
                    self.deadlines[dl_id] = Deadline(**dl_data)

                for task_id, task_data in data.get('tasks', {}).items():
                    self.tasks[task_id] = Task(**task_data)

                for note_id, note_data in data.get('notes', {}).items():
                    self.notes[note_id] = CaseNote(**note_data)

            except Exception as e:
                print(f"Error loading case data: {e}")

    def _save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                'cases': {k: asdict(v) for k, v in self.cases.items()},
                'deadlines': {k: asdict(v) for k, v in self.deadlines.items()},
                'tasks': {k: asdict(v) for k, v in self.tasks.items()},
                'notes': {k: asdict(v) for k, v in self.notes.items()},
                'last_updated': datetime.now().isoformat()
            }

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving case data: {e}")

    def _generate_id(self, prefix: str) -> str:
        """Generate a unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}"

    # Case Management
    def create_case(self, case_data: Dict) -> Case:
        """Create a new case"""
        case_id = self._generate_id("CASE")

        case = Case(
            id=case_id,
            case_number=case_data.get('case_number', ''),
            client_name=case_data['client_name'],
            opposing_party=case_data.get('opposing_party', ''),
            case_type=case_data.get('case_type', CaseType.CONTESTED_DIVORCE.value),
            status=case_data.get('status', CaseStatus.INTAKE.value),
            court=case_data.get('court', 'Nassau County Supreme Court'),
            county=case_data.get('county', 'Nassau'),
            judge=case_data.get('judge', ''),
            attorney=case_data.get('attorney', ''),
            paralegal=case_data.get('paralegal', ''),
            description=case_data.get('description', ''),
            retainer_amount=case_data.get('retainer_amount', 0),
            retainer_balance=case_data.get('retainer_balance', 0),
            marriage_date=case_data.get('marriage_date', ''),
            separation_date=case_data.get('separation_date', ''),
            children=case_data.get('children', [])
        )

        self.cases[case_id] = case

        # Create default tasks for new case
        self._create_intake_tasks(case_id)

        self._save_data()
        return case

    def _create_intake_tasks(self, case_id: str):
        """Create standard intake tasks for a new case"""
        intake_tasks = [
            ("Obtain retainer agreement", "High", 30),
            ("Collect client identification documents", "High", 15),
            ("Gather marriage certificate", "Medium", 15),
            ("Request tax returns (3 years)", "High", 20),
            ("Request pay stubs (3 months)", "Medium", 15),
            ("Request bank statements (12 months)", "High", 20),
            ("Request retirement account statements", "Medium", 15),
            ("Complete client intake form", "High", 45),
            ("Prepare initial Net Worth Statement", "High", 60),
            ("Draft Summons with Notice / Complaint", "High", 45),
            ("Schedule initial client meeting", "High", 15),
        ]

        for title, priority, minutes in intake_tasks:
            self.create_task({
                'case_id': case_id,
                'title': title,
                'priority': priority,
                'estimated_minutes': minutes,
                'tags': ['intake']
            })

    def get_case(self, case_id: str) -> Optional[Case]:
        """Get a case by ID"""
        return self.cases.get(case_id)

    def update_case(self, case_id: str, updates: Dict) -> Optional[Case]:
        """Update a case"""
        if case_id not in self.cases:
            return None

        case = self.cases[case_id]
        for key, value in updates.items():
            if hasattr(case, key):
                setattr(case, key, value)

        self._save_data()
        return case

    def get_all_cases(self, status_filter: str = None) -> List[Case]:
        """Get all cases, optionally filtered by status"""
        cases = list(self.cases.values())

        if status_filter:
            cases = [c for c in cases if c.status == status_filter]

        return sorted(cases, key=lambda c: c.open_date, reverse=True)

    def get_case_summary(self, case_id: str) -> Dict:
        """Get a summary of a case with related items"""
        case = self.get_case(case_id)
        if not case:
            return {}

        deadlines = [self.deadlines[d] for d in case.deadlines if d in self.deadlines]
        tasks = [self.tasks[t] for t in case.tasks if t in self.tasks]

        upcoming_deadlines = sorted(
            [d for d in deadlines if not d.completed],
            key=lambda d: d.due_date
        )[:5]

        pending_tasks = [t for t in tasks if t.status in ['Pending', 'In Progress']]

        return {
            'case': case,
            'upcoming_deadlines': upcoming_deadlines,
            'pending_tasks': pending_tasks,
            'total_deadlines': len(deadlines),
            'completed_deadlines': len([d for d in deadlines if d.completed]),
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.status == 'Completed']),
            'overdue_items': len([d for d in deadlines if d.is_overdue])
        }

    # Deadline Management
    def create_deadline(self, deadline_data: Dict) -> Deadline:
        """Create a new deadline"""
        dl_id = self._generate_id("DL")

        deadline = Deadline(
            id=dl_id,
            case_id=deadline_data['case_id'],
            title=deadline_data['title'],
            deadline_type=deadline_data.get('deadline_type', DeadlineType.FILING_DEADLINE.value),
            due_date=deadline_data['due_date'],
            due_time=deadline_data.get('due_time', ''),
            location=deadline_data.get('location', ''),
            notes=deadline_data.get('notes', ''),
            reminder_days=deadline_data.get('reminder_days', [7, 3, 1])
        )

        self.deadlines[dl_id] = deadline

        # Add to case
        if deadline.case_id in self.cases:
            self.cases[deadline.case_id].deadlines.append(dl_id)

        self._save_data()
        return deadline

    def get_upcoming_deadlines(self, days: int = 14) -> List[Deadline]:
        """Get all deadlines within the next N days"""
        cutoff = datetime.now() + timedelta(days=days)

        upcoming = []
        for deadline in self.deadlines.values():
            if deadline.completed:
                continue

            try:
                due = datetime.strptime(deadline.due_date, "%Y-%m-%d")
                if due <= cutoff:
                    upcoming.append(deadline)
            except:
                pass

        return sorted(upcoming, key=lambda d: d.due_date)

    def get_overdue_deadlines(self) -> List[Deadline]:
        """Get all overdue deadlines"""
        return [d for d in self.deadlines.values() if d.is_overdue]

    def complete_deadline(self, deadline_id: str) -> Optional[Deadline]:
        """Mark a deadline as completed"""
        if deadline_id in self.deadlines:
            self.deadlines[deadline_id].completed = True
            self._save_data()
            return self.deadlines[deadline_id]
        return None

    # Task Management
    def create_task(self, task_data: Dict) -> Task:
        """Create a new task"""
        task_id = self._generate_id("TASK")

        task = Task(
            id=task_id,
            case_id=task_data['case_id'],
            title=task_data['title'],
            description=task_data.get('description', ''),
            priority=task_data.get('priority', 'Medium'),
            status=task_data.get('status', 'Pending'),
            assigned_to=task_data.get('assigned_to', ''),
            due_date=task_data.get('due_date', ''),
            estimated_minutes=task_data.get('estimated_minutes', 30),
            tags=task_data.get('tags', [])
        )

        self.tasks[task_id] = task

        # Add to case
        if task.case_id in self.cases:
            self.cases[task.case_id].tasks.append(task_id)

        self._save_data()
        return task

    def update_task(self, task_id: str, updates: Dict) -> Optional[Task]:
        """Update a task"""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)

        if updates.get('status') == 'Completed':
            task.completed_date = datetime.now().isoformat()

        self._save_data()
        return task

    def get_pending_tasks(self, case_id: str = None) -> List[Task]:
        """Get pending tasks, optionally for a specific case"""
        tasks = list(self.tasks.values())

        if case_id:
            tasks = [t for t in tasks if t.case_id == case_id]

        pending = [t for t in tasks if t.status in ['Pending', 'In Progress']]

        # Sort by priority and due date
        priority_order = {'Urgent': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        return sorted(pending, key=lambda t: (priority_order.get(t.priority, 2), t.due_date or '9999'))

    # Notes
    def add_note(self, note_data: Dict) -> CaseNote:
        """Add a note to a case"""
        note_id = self._generate_id("NOTE")

        note = CaseNote(
            id=note_id,
            case_id=note_data['case_id'],
            content=note_data['content'],
            author=note_data.get('author', 'System'),
            note_type=note_data.get('note_type', 'General'),
            is_privileged=note_data.get('is_privileged', False)
        )

        self.notes[note_id] = note

        # Add to case
        if note.case_id in self.cases:
            self.cases[note.case_id].notes.append(note_id)

        self._save_data()
        return note

    # Dashboard / Reports
    def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        active_cases = [c for c in self.cases.values()
                       if c.status not in ['Closed', 'On Hold']]

        overdue = self.get_overdue_deadlines()
        upcoming = self.get_upcoming_deadlines(7)  # Next 7 days
        pending_tasks = self.get_pending_tasks()

        # Calculate workload
        urgent_tasks = [t for t in pending_tasks if t.priority == 'Urgent']
        high_tasks = [t for t in pending_tasks if t.priority == 'High']

        # Cases by status
        status_counts = {}
        for case in self.cases.values():
            status_counts[case.status] = status_counts.get(case.status, 0) + 1

        # Cases by type
        type_counts = {}
        for case in self.cases.values():
            type_counts[case.case_type] = type_counts.get(case.case_type, 0) + 1

        return {
            'total_cases': len(self.cases),
            'active_cases': len(active_cases),
            'overdue_deadlines': len(overdue),
            'upcoming_deadlines': len(upcoming),
            'pending_tasks': len(pending_tasks),
            'urgent_tasks': len(urgent_tasks),
            'high_priority_tasks': len(high_tasks),
            'status_breakdown': status_counts,
            'type_breakdown': type_counts,
            'overdue_list': overdue[:5],
            'upcoming_list': upcoming[:5],
            'urgent_task_list': urgent_tasks[:5]
        }

    def generate_weekly_report(self) -> str:
        """Generate a weekly status report"""
        dashboard = self.get_dashboard_data()

        report = f"""
{'=' * 60}
            WEEKLY CASE STATUS REPORT
            Generated: {datetime.now().strftime("%B %d, %Y")}
{'=' * 60}

OVERVIEW
--------
Total Active Cases: {dashboard['active_cases']}
Overdue Deadlines: {dashboard['overdue_deadlines']}
Upcoming Deadlines (7 days): {dashboard['upcoming_deadlines']}
Pending Tasks: {dashboard['pending_tasks']}
  - Urgent: {dashboard['urgent_tasks']}
  - High Priority: {dashboard['high_priority_tasks']}

CASES BY STATUS
---------------
"""
        for status, count in dashboard['status_breakdown'].items():
            report += f"  {status}: {count}\n"

        report += """
CASES BY TYPE
-------------
"""
        for case_type, count in dashboard['type_breakdown'].items():
            report += f"  {case_type}: {count}\n"

        if dashboard['overdue_list']:
            report += """
OVERDUE DEADLINES (Action Required)
-----------------------------------
"""
            for dl in dashboard['overdue_list']:
                case = self.cases.get(dl.case_id)
                client = case.client_name if case else "Unknown"
                report += f"  ⚠️ {dl.title} - {client}\n"
                report += f"     Due: {dl.due_date} ({abs(dl.days_until_due)} days overdue)\n"

        if dashboard['upcoming_list']:
            report += """
UPCOMING DEADLINES (Next 7 Days)
--------------------------------
"""
            for dl in dashboard['upcoming_list']:
                case = self.cases.get(dl.case_id)
                client = case.client_name if case else "Unknown"
                report += f"  📅 {dl.title} - {client}\n"
                report += f"     Due: {dl.due_date} ({dl.days_until_due} days)\n"

        report += f"""
{'=' * 60}
"""
        return report


def create_case_manager() -> CaseManager:
    """Factory function"""
    return CaseManager()
