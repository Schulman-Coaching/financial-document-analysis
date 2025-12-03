#!/usr/bin/env python3
"""
Firm Configuration Module
White-label settings for law firm customization
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class FirmConfig:
    """Configuration for law firm branding and settings"""

    # Firm Identity
    firm_name: str = "The White Law Group"
    firm_tagline: str = "Seeking Justice Is Our Mission"
    firm_logo_url: Optional[str] = None

    # Contact Information
    address: str = "4 Brower Ave Suite 3, Woodmere, NY 11598"
    phone: str = "(347) 628-5440"
    email: str = "lawyer@wwlgny.com"
    website: str = "https://wwlgny.com"

    # Practice Areas
    practice_areas: List[str] = field(default_factory=lambda: [
        "Family Law",
        "Divorce",
        "Child Custody",
        "Child Support",
        "Spousal Maintenance",
        "Domestic Violence",
        "Criminal Defense"
    ])

    # Team Members
    attorneys: List[Dict] = field(default_factory=lambda: [
        {"name": "Attorney", "title": "Partner", "email": "lawyer@wwlgny.com"}
    ])

    office_manager: str = "Ivy Gabel"

    # Jurisdiction Settings
    primary_jurisdiction: str = "Nassau County"
    courts: List[str] = field(default_factory=lambda: [
        "Nassau County Supreme Court",
        "Nassau County Family Court",
        "Queens County Supreme Court",
        "Queens County Family Court",
        "Kings County Supreme Court",
        "Kings County Family Court",
        "New York County Supreme Court",
        "Suffolk County Supreme Court",
        "Suffolk County Family Court"
    ])

    # Document Settings
    report_header: str = "CONFIDENTIAL - ATTORNEY WORK PRODUCT"
    report_footer: str = "Prepared by The White Law Group | (347) 628-5440"

    # Theme Colors (hex)
    primary_color: str = "#1a365d"  # Navy blue
    secondary_color: str = "#c9a227"  # Gold
    accent_color: str = "#2d3748"  # Dark gray

    # Feature Flags
    enable_domestic_violence_module: bool = True
    enable_criminal_crossover: bool = True  # For cases with criminal aspects
    enable_client_portal: bool = True


# Nassau County specific settings
NASSAU_COUNTY_CONFIG = {
    "courthouse_address": "100 Supreme Court Drive, Mineola, NY 11501",
    "family_court_address": "1200 Old Country Road, Westbury, NY 11590",
    "filing_fees": {
        "divorce_index": 210,
        "motion": 45,
        "rji": 95,
        "note_of_issue": 30
    },
    "judges": [
        "Hon. Jeffrey A. Goodstein",
        "Hon. Hope Schwartz Zimmerman",
        "Hon. Stacy D. Bennett",
        "Hon. Edmund M. Dane"
    ],
    "support_magistrates": [
        "Support Magistrate - Nassau Family Court"
    ]
}


# Case type configurations
CASE_TYPES = {
    "contested_divorce": {
        "name": "Contested Divorce",
        "typical_documents": [
            "Summons with Notice / Summons and Complaint",
            "Net Worth Statement",
            "Statement of Proposed Disposition",
            "Retainer Agreement",
            "Client Intake Form"
        ],
        "discovery_items": [
            "Demand for Discovery and Inspection",
            "Interrogatories",
            "Notice to Produce",
            "Subpoenas Duces Tecum"
        ]
    },
    "uncontested_divorce": {
        "name": "Uncontested Divorce",
        "typical_documents": [
            "Summons with Notice",
            "Verified Complaint",
            "Affidavit of Plaintiff",
            "Affidavit of Defendant",
            "Settlement Agreement",
            "Child Support Worksheet (if children)",
            "Findings of Fact and Conclusions of Law",
            "Judgment of Divorce"
        ]
    },
    "custody_modification": {
        "name": "Custody Modification",
        "typical_documents": [
            "Petition for Modification",
            "Affidavit in Support",
            "Proposed Parenting Plan"
        ]
    },
    "child_support": {
        "name": "Child Support",
        "typical_documents": [
            "Petition for Child Support",
            "Financial Disclosure Affidavit",
            "Child Support Worksheet"
        ]
    },
    "domestic_violence": {
        "name": "Domestic Violence / Order of Protection",
        "typical_documents": [
            "Family Offense Petition",
            "Affidavit in Support",
            "Temporary Order of Protection",
            "Final Order of Protection"
        ],
        "safety_considerations": True,
        "criminal_crossover": True
    }
}


# Report templates
REPORT_TEMPLATES = {
    "support_analysis": {
        "title": "Child Support & Maintenance Analysis",
        "sections": [
            "Executive Summary",
            "Income Analysis",
            "Child Support Calculation (CSSA)",
            "Maintenance Calculation",
            "Deviation Factors",
            "Recommendations"
        ]
    },
    "financial_summary": {
        "title": "Financial Document Summary",
        "sections": [
            "Document Overview",
            "Income Sources",
            "Assets Summary",
            "Liabilities Summary",
            "Discrepancies Identified",
            "Red Flags"
        ]
    },
    "case_summary": {
        "title": "Case Financial Summary",
        "sections": [
            "Case Information",
            "Party Information",
            "Financial Overview",
            "Support Calculations",
            "Asset Distribution Analysis",
            "Settlement Recommendations"
        ]
    }
}


def get_default_config() -> FirmConfig:
    """Get default firm configuration"""
    return FirmConfig()


def load_firm_config(config_path: str = None) -> FirmConfig:
    """Load firm configuration from file or return default"""
    # In production, this would load from a JSON/YAML file
    return get_default_config()
