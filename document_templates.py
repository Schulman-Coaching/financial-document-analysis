#!/usr/bin/env python3
"""
Legal Document Templates for NY Family Law Practice
Based on official NY State Unified Court System forms

Templates for:
- Net Worth Statement (DRL 236)
- Verified Complaint for Divorce
- Child Support Worksheet (CSSA)
- Family Offense Petition
- Custody/Visitation Petition
- Stipulation of Settlement
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PartyInfo:
    """Information about a party in the case"""
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: str = ""
    dob: str = ""
    ssn_last4: str = ""
    employer: str = ""
    employer_address: str = ""
    occupation: str = ""


@dataclass
class ChildInfo:
    """Information about a child"""
    name: str
    dob: str
    age: int
    residence: str
    school: str = ""
    special_needs: bool = False
    special_needs_desc: str = ""


class DocumentTemplates:
    """Generate NY Family Law document templates"""

    def __init__(self, firm_name: str = "The White Law Group",
                 firm_address: str = "4 Brower Ave Suite 3, Woodmere, NY 11598",
                 firm_phone: str = "(347) 628-5440"):
        self.firm_name = firm_name
        self.firm_address = firm_address
        self.firm_phone = firm_phone

    def generate_net_worth_statement(self,
                                     party: PartyInfo,
                                     spouse: PartyInfo,
                                     county: str,
                                     index_number: str,
                                     income_data: Dict,
                                     assets: Dict,
                                     liabilities: Dict,
                                     expenses: Dict) -> str:
        """
        Generate Net Worth Statement per DRL 236 and 22 NYCRR 202.16(b)
        """
        today = datetime.now().strftime("%B %d, %Y")

        template = f"""
{'=' * 75}
                    SUPREME COURT OF THE STATE OF NEW YORK
                           COUNTY OF {county.upper()}
{'=' * 75}

{party.name},
                                                    Plaintiff,
        -against-                                   Index No.: {index_number}

{spouse.name},
                                                    Defendant.
{'=' * 75}

                         SWORN STATEMENT OF NET WORTH
                    Pursuant to DRL 236(B) and 22 NYCRR 202.16(b)

{'=' * 75}

STATE OF NEW YORK    )
                     ) ss.:
COUNTY OF {county.upper()}    )

I, {party.name}, being duly sworn, depose and say:

{'=' * 75}
                           PART I - BACKGROUND
{'=' * 75}

1. DATE OF COMMENCEMENT OF ACTION: _______________

2. DATE OF MARRIAGE: _______________

3. DATE OF SEPARATION: _______________

4. GROUNDS FOR DIVORCE:
   [ ] Irretrievable Breakdown (DRL 170(7))
   [ ] Other: _______________

5. NUMBER OF DEPENDENT CHILDREN: _______________

6. CUSTODY REQUESTED BY:
   [ ] Plaintiff  [ ] Defendant  [ ] Joint  [ ] Other

{'=' * 75}
                        PART II - PARTY INFORMATION
{'=' * 75}

DEPONENT'S INFORMATION:

Name: {party.name}
Address: {party.address}
         {party.city}, {party.state} {party.zip_code}
Telephone: {party.phone}
Email: {party.email}
Date of Birth: {party.dob}
Social Security Number (last 4): XXX-XX-{party.ssn_last4}

Employer: {party.employer}
Employer Address: {party.employer_address}
Occupation: {party.occupation}

SPOUSE'S INFORMATION:

Name: {spouse.name}
Address: {spouse.address}
         {spouse.city}, {spouse.state} {spouse.zip_code}
Date of Birth: {spouse.dob}
Social Security Number (last 4): XXX-XX-{spouse.ssn_last4}
Employer: {spouse.employer}

{'=' * 75}
                           PART III - GROSS INCOME
                    (From all sources for prior calendar year)
{'=' * 75}

                                        HUSBAND         WIFE
                                        --------        --------
1. Salary/Wages                         $________       $________
2. Bonus/Commission                     $________       $________
3. Self-Employment Income               $________       $________
4. Investment Income                    $________       $________
5. Rental Income                        $________       $________
6. Pension/Retirement Income            $________       $________
7. Social Security                      $________       $________
8. Disability Benefits                  $________       $________
9. Public Assistance                    $________       $________
10. Other Income (specify):             $________       $________

TOTAL GROSS INCOME:                     $________       $________

{'=' * 75}
                              SCHEDULE A - ASSETS
{'=' * 75}

A. REAL PROPERTY
   ---------------------------------------------------------------------------
   Address                          Title      Date Acquired    Current Value
   ---------------------------------------------------------------------------
   ________________________________ __________ _______________ $______________
   ________________________________ __________ _______________ $______________

B. BANK ACCOUNTS
   ---------------------------------------------------------------------------
   Institution          Account Type    Account #        Balance
   ---------------------------------------------------------------------------
   ____________________ _______________ ______________ $______________
   ____________________ _______________ ______________ $______________
   ____________________ _______________ ______________ $______________

C. RETIREMENT ACCOUNTS
   ---------------------------------------------------------------------------
   Type (401k/IRA/Pension)    Institution         Balance
   ---------------------------------------------------------------------------
   __________________________ __________________ $______________
   __________________________ __________________ $______________

D. INVESTMENTS (Stocks, Bonds, Mutual Funds)
   ---------------------------------------------------------------------------
   Description                 Institution         Value
   ---------------------------------------------------------------------------
   __________________________ __________________ $______________
   __________________________ __________________ $______________

E. VEHICLES
   ---------------------------------------------------------------------------
   Year/Make/Model              Title In Name Of     Value
   ---------------------------------------------------------------------------
   __________________________ __________________ $______________
   __________________________ __________________ $______________

F. LIFE INSURANCE
   ---------------------------------------------------------------------------
   Company          Policy #          Face Value       Cash Value
   ---------------------------------------------------------------------------
   ______________ ________________ $______________ $______________

G. BUSINESS INTERESTS
   ---------------------------------------------------------------------------
   Business Name        Type              Ownership %      Value
   ---------------------------------------------------------------------------
   __________________ ________________ ______________ $______________

H. OTHER ASSETS (jewelry, art, collectibles, etc.)
   ---------------------------------------------------------------------------
   Description                                      Value
   ---------------------------------------------------------------------------
   ______________________________________________ $______________
   ______________________________________________ $______________

TOTAL ASSETS:                                      $______________

{'=' * 75}
                           SCHEDULE B - LIABILITIES
{'=' * 75}

A. MORTGAGE(S)
   ---------------------------------------------------------------------------
   Property Address          Lender              Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________

B. HOME EQUITY LOANS/LINES OF CREDIT
   ---------------------------------------------------------------------------
   Lender                   Purpose             Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________

C. CREDIT CARDS
   ---------------------------------------------------------------------------
   Creditor                 Account #           Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________
   ________________________ __________________ $______________
   ________________________ __________________ $______________

D. AUTOMOBILE LOANS
   ---------------------------------------------------------------------------
   Vehicle                  Lender              Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________

E. STUDENT LOANS
   ---------------------------------------------------------------------------
   Lender                   Original Amount     Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________

F. PERSONAL LOANS
   ---------------------------------------------------------------------------
   Creditor                 Purpose             Balance
   ---------------------------------------------------------------------------
   ________________________ __________________ $______________

G. OTHER LIABILITIES
   ---------------------------------------------------------------------------
   Description                                  Balance
   ---------------------------------------------------------------------------
   ____________________________________________ $______________

TOTAL LIABILITIES:                              $______________

{'=' * 75}
                              NET WORTH SUMMARY
{'=' * 75}

TOTAL ASSETS:                                   $______________
LESS: TOTAL LIABILITIES:                        $______________
                                                ---------------
NET WORTH:                                      $______________

{'=' * 75}
                         SCHEDULE C - MONTHLY EXPENSES
{'=' * 75}

HOUSING:
  Mortgage/Rent                                 $______________
  Real Estate Taxes                             $______________
  Homeowner's Insurance                         $______________
  Utilities (electric, gas, water)              $______________
  Telephone/Internet/Cable                      $______________
  Maintenance/Repairs                           $______________

TRANSPORTATION:
  Car Payment                                   $______________
  Auto Insurance                                $______________
  Gas/Oil                                       $______________
  Maintenance/Repairs                           $______________
  Parking/Tolls                                 $______________
  Public Transportation                         $______________

INSURANCE:
  Life Insurance                                $______________
  Health Insurance                              $______________
  Disability Insurance                          $______________

CHILDREN'S EXPENSES:
  Child Care/Day Care                           $______________
  Education/Tuition                             $______________
  School Supplies                               $______________
  Activities/Lessons                            $______________
  Clothing                                      $______________
  Medical/Dental (unreimbursed)                 $______________

PERSONAL EXPENSES:
  Food/Groceries                                $______________
  Clothing                                      $______________
  Medical/Dental (unreimbursed)                 $______________
  Personal Care                                 $______________
  Recreation/Entertainment                      $______________

OTHER EXPENSES:
  Credit Card Payments (minimum)                $______________
  Loan Payments                                 $______________
  Professional Dues                             $______________
  Charitable Contributions                      $______________
  Other: ____________________                   $______________

TOTAL MONTHLY EXPENSES:                         $______________

{'=' * 75}
                              VERIFICATION
{'=' * 75}

I, {party.name}, affirm under the penalties of perjury under the
laws of New York, which may include a fine or imprisonment, that the
foregoing is true and correct to the best of my knowledge, information
and belief.

I understand that willful false statements made herein are punishable
as a Class A misdemeanor pursuant to Section 210.45 of the New York
State Penal Law.

I have attached hereto my W-2 or 1099 statements for the previous
year, or if not available, my most recent Federal and State Income
Tax Returns as required by 22 NYCRR 202.16(b).


_________________________________          _______________
{party.name}                               Date


Sworn to before me this
_____ day of _____________, 20___

_________________________________
Notary Public

{'=' * 75}

PREPARED BY:

{self.firm_name}
{self.firm_address}
{self.firm_phone}

Attorney for: [ ] Plaintiff  [ ] Defendant

{'=' * 75}
"""
        return template

    def generate_verified_complaint(self,
                                   plaintiff: PartyInfo,
                                   defendant: PartyInfo,
                                   county: str,
                                   marriage_date: str,
                                   marriage_place: str,
                                   separation_date: str,
                                   children: List[ChildInfo],
                                   grounds: str = "Irretrievable Breakdown") -> str:
        """
        Generate Verified Complaint for Divorce (Form UD-2)
        """
        today = datetime.now().strftime("%B %d, %Y")

        children_section = ""
        if children:
            children_section = """
FIFTH: The following child(ren) were born of this marriage:

"""
            for i, child in enumerate(children, 1):
                children_section += f"""
    Child {i}:
    Name: {child.name}
    Date of Birth: {child.dob}
    Age: {child.age}
    Currently Residing With: {child.residence}
"""
        else:
            children_section = """
FIFTH: There are no children born of this marriage.
"""

        template = f"""
{'=' * 75}
                    SUPREME COURT OF THE STATE OF NEW YORK
                           COUNTY OF {county.upper()}
{'=' * 75}

{plaintiff.name},
                                                    Plaintiff,
        -against-                                   Index No.: _______________

{defendant.name},
                                                    Defendant.
{'=' * 75}

                           VERIFIED COMPLAINT FOR DIVORCE
                              (DRL Section 170)

{'=' * 75}

Plaintiff, by his/her attorneys, {self.firm_name}, complaining of the
Defendant, respectfully alleges upon information and belief:

FIRST: The Plaintiff has resided in the State of New York for a
continuous period of at least two years immediately preceding the
commencement of this action.

[ ] OR

FIRST: The Plaintiff has resided in the State of New York for a
continuous period of at least one year immediately preceding the
commencement of this action, AND:

    [ ] The parties were married in New York State; OR
    [ ] The parties have resided as husband and wife in New York State; OR
    [ ] The cause of action arose in New York State.

SECOND: The Plaintiff and the Defendant were married on {marriage_date}
in {marriage_place}.

THIRD: The marriage between the parties was NOT performed by a clergyman,
minister, or by a leader of the Society for Ethical Culture, or other
officiator, OR if it was, it was NOT followed by a religious annulment,
divorce, or dissolution.

FOURTH: There is no judgment, decree, or order of separation or divorce
or other order annulling or dissolving this marriage.
{children_section}
SIXTH: GROUNDS FOR DIVORCE

[ ] DRL §170(7) - IRRETRIEVABLE BREAKDOWN

The relationship between husband and wife has broken down irretrievably
for a period of at least six months. This sworn statement is made by
the Plaintiff.

All issues of equitable distribution of marital property, the payment
or waiver of spousal support, the payment of child support, the payment
of counsel and experts' fees and expenses, and the custody and visitation
of the minor children of the marriage have been:

    [ ] resolved by written agreement signed by the parties; OR
    [ ] will be determined by the court.

[ ] DRL §170(1) - CRUEL AND INHUMAN TREATMENT

The Defendant has engaged in cruel and inhuman treatment of the Plaintiff
for a period of five years or more immediately preceding the commencement
of this action, which so endangers the physical or mental well-being of
the Plaintiff as to render it unsafe or improper to continue to cohabit
with the Defendant.

[ ] DRL §170(2) - ABANDONMENT

The Defendant abandoned the Plaintiff for a period of one or more years.

[ ] DRL §170(3) - IMPRISONMENT

After the marriage, the Defendant was confined in prison for a period of
three or more consecutive years.

[ ] DRL §170(4) - ADULTERY

The Defendant committed adultery.

SEVENTH: RELIEF REQUESTED

WHEREFORE, Plaintiff demands judgment against the Defendant:

(a) Dissolving the marriage between the parties;

(b) Awarding custody of the minor child(ren) to: [ ] Plaintiff [ ] Defendant
    [ ] Joint custody;

(c) Awarding child support pursuant to the Child Support Standards Act
    (DRL §240);

(d) Awarding maintenance to the Plaintiff;

(e) Equitably distributing the marital property;

(f) Awarding counsel fees;

(g) Granting such other and further relief as the Court deems just
    and proper.


                                        {self.firm_name}
                                        Attorneys for Plaintiff

                                        By: _________________________

                                        {self.firm_address}
                                        {self.firm_phone}

{'=' * 75}
                              VERIFICATION
{'=' * 75}

STATE OF NEW YORK    )
                     ) ss.:
COUNTY OF {county.upper()}    )

{plaintiff.name}, being duly sworn, deposes and says:

I am the Plaintiff in the above-entitled action. I have read the
foregoing Verified Complaint and know the contents thereof. The same
is true to my own knowledge, except as to those matters therein stated
to be alleged upon information and belief, and as to those matters I
believe it to be true.

I affirm this statement to be true under the penalties of perjury.


_________________________________          _______________
{plaintiff.name}                           Date


Sworn to before me this
_____ day of _____________, 20___

_________________________________
Notary Public

{'=' * 75}
"""
        return template

    def generate_child_support_worksheet(self,
                                        custodial_parent: PartyInfo,
                                        non_custodial_parent: PartyInfo,
                                        county: str,
                                        children: List[ChildInfo],
                                        custodial_income: float,
                                        non_custodial_income: float,
                                        childcare_cost: float = 0,
                                        health_insurance: float = 0,
                                        education_cost: float = 0) -> str:
        """
        Generate Child Support Standards Act (CSSA) Worksheet
        """
        num_children = len(children)

        # CSSA percentages
        cssa_rates = {1: 0.17, 2: 0.25, 3: 0.29, 4: 0.31, 5: 0.35}
        cssa_pct = cssa_rates.get(num_children, 0.35)

        combined_income = custodial_income + non_custodial_income
        cssa_cap = 183000  # 2024 cap

        # Calculate shares
        if combined_income > 0:
            custodial_share = custodial_income / combined_income
            non_custodial_share = non_custodial_income / combined_income
        else:
            custodial_share = 0.5
            non_custodial_share = 0.5

        # Basic support calculation
        income_for_calc = min(combined_income, cssa_cap)
        basic_support = income_for_calc * cssa_pct
        ncp_basic_support = basic_support * non_custodial_share

        # Add-ons (pro rata share)
        total_addons = childcare_cost + health_insurance + education_cost
        ncp_addons = total_addons * non_custodial_share

        total_support = ncp_basic_support + ncp_addons

        children_list = "\n".join([
            f"    {i+1}. {c.name}, DOB: {c.dob}, Age: {c.age}"
            for i, c in enumerate(children)
        ])

        template = f"""
{'=' * 75}
                    CHILD SUPPORT STANDARDS ACT WORKSHEET
                         (DRL §240(1-b); FCA §413)
{'=' * 75}

COURT: Supreme Court / Family Court
COUNTY: {county}
INDEX/DOCKET NO.: _______________

CUSTODIAL PARENT:      {custodial_parent.name}
NON-CUSTODIAL PARENT:  {non_custodial_parent.name}

CHILD(REN) SUBJECT TO THIS ORDER:
{children_list}

NUMBER OF CHILDREN: {num_children}

{'=' * 75}
                         PART I - INCOME CALCULATION
{'=' * 75}

                                    CUSTODIAL       NON-CUSTODIAL
                                    PARENT          PARENT
                                    -----------     -----------
1. Gross Income                     ${custodial_income:>12,.2f}    ${non_custodial_income:>12,.2f}

2. Less: FICA (Social Security)     $____________    $____________

3. Less: NYC Income Tax             $____________    $____________
   (if applicable)

4. ADJUSTED GROSS INCOME            $____________    $____________

5. COMBINED PARENTAL INCOME:        ${combined_income:>12,.2f}

{'=' * 75}
                      PART II - BASIC CHILD SUPPORT
{'=' * 75}

6. Combined Parental Income (Line 5):           ${combined_income:>12,.2f}

7. CSSA Income Cap (2024):                      ${cssa_cap:>12,.2f}

8. Income Subject to CSSA Calculation:          ${income_for_calc:>12,.2f}
   (Lesser of Line 6 or Line 7)

9. CSSA Percentage for {num_children} child(ren):              {cssa_pct * 100:.0f}%

   (1 child = 17%, 2 children = 25%, 3 children = 29%,
    4 children = 31%, 5+ children = 35%)

10. Combined Basic Child Support (Line 8 x Line 9):  ${basic_support:>12,.2f}

11. Pro Rata Shares:
    Custodial Parent:     {custodial_share * 100:>6.1f}%
    Non-Custodial Parent: {non_custodial_share * 100:>6.1f}%

12. NON-CUSTODIAL PARENT'S BASIC SUPPORT:       ${ncp_basic_support:>12,.2f}
    (Line 10 x Non-Custodial Share)

{'=' * 75}
                        PART III - ADD-ON EXPENSES
              (Pro Rata Share Paid by Non-Custodial Parent)
{'=' * 75}

13. Child Care Expenses
    (work-related, reasonable)                  ${childcare_cost:>12,.2f}
    Non-Custodial Share ({non_custodial_share * 100:.1f}%):         ${childcare_cost * non_custodial_share:>12,.2f}

14. Health Insurance Premium
    (for child(ren))                            ${health_insurance:>12,.2f}
    Non-Custodial Share ({non_custodial_share * 100:.1f}%):         ${health_insurance * non_custodial_share:>12,.2f}

15. Unreimbursed Health Care Expenses
    (reasonable, necessary)                     $____________
    Non-Custodial Share ({non_custodial_share * 100:.1f}%):         $____________

16. Educational Expenses
    (special needs, private school if agreed)   ${education_cost:>12,.2f}
    Non-Custodial Share ({non_custodial_share * 100:.1f}%):         ${education_cost * non_custodial_share:>12,.2f}

17. TOTAL ADD-ON EXPENSES:                      ${total_addons:>12,.2f}
    NON-CUSTODIAL PARENT'S SHARE:               ${ncp_addons:>12,.2f}

{'=' * 75}
                         PART IV - TOTAL SUPPORT
{'=' * 75}

18. Non-Custodial Parent's Basic Support
    (Line 12):                                  ${ncp_basic_support:>12,.2f}

19. Non-Custodial Parent's Add-On Share
    (Line 17):                                  ${ncp_addons:>12,.2f}

20. TOTAL CHILD SUPPORT OBLIGATION:             ${total_support:>12,.2f}
                                                ===============

    MONTHLY PAYMENT:                            ${total_support / 12:>12,.2f}

    BI-WEEKLY PAYMENT:                          ${total_support / 26:>12,.2f}

    WEEKLY PAYMENT:                             ${total_support / 52:>12,.2f}

{'=' * 75}
                    PART V - ABOVE-CAP INCOME (If Applicable)
{'=' * 75}

21. Combined Income Above Cap
    (Line 6 minus Line 7, if positive):         ${max(0, combined_income - cssa_cap):>12,.2f}

22. Additional Support for Above-Cap Income
    (Court's discretion based on factors
    in DRL 240(1-b)(f)):                        $____________

{'=' * 75}
                          DEVIATION FACTORS
                    (DRL §240(1-b)(f) - Court may consider)
{'=' * 75}

[ ] Financial resources of custodial parent
[ ] Physical and emotional health of child
[ ] Child's standard of living prior to divorce
[ ] Tax consequences to the parties
[ ] Non-monetary contributions of parents
[ ] Educational needs of either parent
[ ] Gross income disparity between parents
[ ] Needs of other children non-custodial parent supports
[ ] Extraordinary visitation expenses
[ ] Other factors court finds relevant

DEVIATION REQUESTED:    [ ] Yes    [ ] No

If yes, explain: ___________________________________________________
____________________________________________________________________

{'=' * 75}
                              SIGNATURES
{'=' * 75}

_________________________________          _______________
{custodial_parent.name}                    Date
Custodial Parent


_________________________________          _______________
{non_custodial_parent.name}                Date
Non-Custodial Parent


_________________________________          _______________
Attorney for Custodial Parent              Date


_________________________________          _______________
Attorney for Non-Custodial Parent          Date

{'=' * 75}

PREPARED BY:
{self.firm_name}
{self.firm_address}
{self.firm_phone}

{'=' * 75}
"""
        return template

    def generate_family_offense_petition(self,
                                        petitioner: PartyInfo,
                                        respondent: PartyInfo,
                                        county: str,
                                        relationship: str,
                                        incidents: List[Dict],
                                        relief_requested: List[str]) -> str:
        """
        Generate Family Offense Petition for Order of Protection
        """
        today = datetime.now().strftime("%B %d, %Y")

        incidents_text = ""
        for i, incident in enumerate(incidents, 1):
            incidents_text += f"""
INCIDENT {i}:
Date: {incident.get('date', '_______________')}
Time: {incident.get('time', '_______________')}
Location: {incident.get('location', '_______________')}

Description of what happened:
{incident.get('description', '_' * 60)}

Injuries sustained (if any):
{incident.get('injuries', 'None' if not incident.get('injuries') else incident.get('injuries'))}

Witnesses (if any):
{incident.get('witnesses', 'None' if not incident.get('witnesses') else incident.get('witnesses'))}

Police called: [ ] Yes  [ ] No
If yes, precinct/report number: {incident.get('police_report', '_______________')}

"""

        relief_text = "\n".join([f"    [X] {r}" for r in relief_requested])

        template = f"""
{'=' * 75}
                         FAMILY COURT OF THE STATE OF NEW YORK
                                COUNTY OF {county.upper()}
{'=' * 75}

In the Matter of a Proceeding Under
Article 8 of the Family Court Act

{petitioner.name},                              Docket No.: _______________
                    Petitioner,
        -against-

{respondent.name},
                    Respondent.
{'=' * 75}

                           FAMILY OFFENSE PETITION
                  (Pursuant to Article 8, Family Court Act)

{'=' * 75}

TO THE FAMILY COURT:

The undersigned Petitioner respectfully alleges:

1. PETITIONER INFORMATION:

   Name: {petitioner.name}
   Address: {petitioner.address}
            {petitioner.city}, {petitioner.state} {petitioner.zip_code}
   Telephone: {petitioner.phone}
   Date of Birth: {petitioner.dob}

   [ ] I request that my address be kept CONFIDENTIAL pursuant to
       FCA §154-b (Address Confidentiality Program)

2. RESPONDENT INFORMATION:

   Name: {respondent.name}
   Address: {respondent.address}
            {respondent.city}, {respondent.state} {respondent.zip_code}
   Telephone: {respondent.phone}
   Date of Birth: {respondent.dob}

3. RELATIONSHIP BETWEEN PARTIES:

   The Petitioner and Respondent are related or have the following
   relationship (check all that apply):

   [ ] Legally married
   [ ] Formerly married
   [ ] Related by blood or marriage
   [ ] Have a child in common
   [ ] Currently in an intimate relationship
   [ ] Formerly in an intimate relationship
   [ ] Members of the same household

   Specific relationship: {relationship}

4. FAMILY OFFENSES ALLEGED:

   The Respondent has committed the following family offense(s) against
   the Petitioner (check all that apply):

   [ ] Disorderly Conduct (PL §240.20)
   [ ] Harassment in the First Degree (PL §240.25)
   [ ] Harassment in the Second Degree (PL §240.26)
   [ ] Aggravated Harassment in the Second Degree (PL §240.30)
   [ ] Menacing in the Second Degree (PL §120.14)
   [ ] Menacing in the Third Degree (PL §120.15)
   [ ] Reckless Endangerment (PL §120.20)
   [ ] Assault in the Second Degree (PL §120.05)
   [ ] Assault in the Third Degree (PL §120.00)
   [ ] Attempted Assault (PL §110/120.00)
   [ ] Stalking in the First Degree (PL §120.60)
   [ ] Stalking in the Second Degree (PL §120.55)
   [ ] Stalking in the Third Degree (PL §120.50)
   [ ] Stalking in the Fourth Degree (PL §120.45)
   [ ] Criminal Mischief (PL §145.00-145.12)
   [ ] Strangulation in the First Degree (PL §121.13)
   [ ] Strangulation in the Second Degree (PL §121.12)
   [ ] Criminal Obstruction of Breathing (PL §121.11)
   [ ] Identity Theft (PL §190.78-190.80)
   [ ] Grand Larceny (PL §155.30-155.42)
   [ ] Coercion (PL §135.60-135.65)
   [ ] Other: _______________

5. DESCRIPTION OF INCIDENTS:
{incidents_text}
6. PRIOR ORDERS OF PROTECTION:

   [ ] No prior orders of protection have been issued
   [ ] Prior order(s) of protection have been issued:

   Court: _______________  Date: _______________  Expiration: _______________
   Court: _______________  Date: _______________  Expiration: _______________

7. PENDING CRIMINAL PROCEEDINGS:

   [ ] No criminal charges pending
   [ ] Criminal charges are pending:

   Court: _______________  Docket No.: _______________
   Charges: _______________

8. CHILDREN:

   [ ] There are no children in common or residing with either party
   [ ] The following children are in common or reside with either party:

   Name: _________________________  DOB: ___________  Resides with: _________
   Name: _________________________  DOB: ___________  Resides with: _________
   Name: _________________________  DOB: ___________  Resides with: _________

9. RELIEF REQUESTED:

   Petitioner respectfully requests that the Court issue an Order of
   Protection directing the Respondent to:

{relief_text}

   [ ] Stay away from Petitioner
   [ ] Stay away from Petitioner's home at: _______________
   [ ] Stay away from Petitioner's place of employment at: _______________
   [ ] Stay away from Petitioner's school at: _______________
   [ ] Stay away from the children at: _______________
   [ ] Refrain from committing any family offense
   [ ] Refrain from harassing, intimidating, or threatening Petitioner
   [ ] Refrain from contacting Petitioner by telephone, email, text, or
       social media
   [ ] Surrender firearms and firearms license
   [ ] Pay restitution in the amount of: $_______________
   [ ] Participate in a batterer's intervention program
   [ ] Other: _______________

   Duration requested:
   [ ] Temporary Order of Protection (until hearing)
   [ ] Final Order of Protection for _____ years (maximum 2 years,
       or 5 years with aggravating circumstances)

{'=' * 75}
                              VERIFICATION
{'=' * 75}

STATE OF NEW YORK    )
                     ) ss.:
COUNTY OF {county.upper()}    )

I, {petitioner.name}, being duly sworn, state that I have read the
foregoing petition and that the contents are true to the best of my
knowledge.

I am aware that if any of the foregoing statements are willfully false,
I am subject to punishment for perjury.


_________________________________          _______________
{petitioner.name}                          Date
Petitioner


Sworn to before me this
_____ day of _____________, 20___

_________________________________
Notary Public

{'=' * 75}

                         SAFETY PLANNING NOTICE

If you are in immediate danger, call 911.

National Domestic Violence Hotline: 1-800-799-7233
NYS Domestic Violence Hotline: 1-800-942-6906
NYC Domestic Violence Hotline: 1-800-621-HOPE (4673)

{'=' * 75}

PREPARED BY:
{self.firm_name}
{self.firm_address}
{self.firm_phone}

{'=' * 75}
"""
        return template

    def generate_stipulation_of_settlement(self,
                                          plaintiff: PartyInfo,
                                          defendant: PartyInfo,
                                          county: str,
                                          index_number: str,
                                          marriage_date: str,
                                          children: List[ChildInfo],
                                          custody_arrangement: str,
                                          child_support_monthly: float,
                                          maintenance_monthly: float,
                                          maintenance_duration: str,
                                          property_division: Dict) -> str:
        """
        Generate Stipulation of Settlement for divorce
        """
        today = datetime.now().strftime("%B %d, %Y")

        children_section = ""
        if children:
            children_section = f"""
ARTICLE III - CHILDREN

3.1 The parties are the parents of the following minor child(ren):

"""
            for i, child in enumerate(children, 1):
                children_section += f"    {child.name}, born {child.dob}\n"

            children_section += f"""
3.2 CUSTODY:
    {custody_arrangement}

3.3 PARENTING TIME/VISITATION:
    The non-custodial parent shall have parenting time as follows:
    [To be specified]

3.4 DECISION-MAKING:
    [ ] Joint decision-making on major decisions (education, health, religion)
    [ ] Sole decision-making to: _______________
"""
        else:
            children_section = """
ARTICLE III - CHILDREN

3.1 There are no minor children of this marriage.
"""

        template = f"""
{'=' * 75}
                    SUPREME COURT OF THE STATE OF NEW YORK
                           COUNTY OF {county.upper()}
{'=' * 75}

{plaintiff.name},
                                                    Plaintiff,
        -against-                                   Index No.: {index_number}

{defendant.name},
                                                    Defendant.
{'=' * 75}

                        STIPULATION OF SETTLEMENT

{'=' * 75}

This STIPULATION OF SETTLEMENT ("Agreement") is entered into this
_____ day of _____________, 20___, by and between:

{plaintiff.name} ("Plaintiff" or "Wife/Husband")
Residing at: {plaintiff.address}, {plaintiff.city}, {plaintiff.state} {plaintiff.zip_code}

AND

{defendant.name} ("Defendant" or "Wife/Husband")
Residing at: {defendant.address}, {defendant.city}, {defendant.state} {defendant.zip_code}

{'=' * 75}
                              RECITALS
{'=' * 75}

WHEREAS, the parties were lawfully married on {marriage_date}; and

WHEREAS, the parties have agreed to live separate and apart and to
settle all issues arising from their marriage, including but not limited
to equitable distribution, maintenance, child support, custody, and
visitation; and

WHEREAS, each party has had the opportunity to consult with independent
legal counsel and has done so or has voluntarily waived such right; and

WHEREAS, each party has made full and complete financial disclosure to
the other party through the exchange of Sworn Statements of Net Worth;

NOW, THEREFORE, in consideration of the mutual promises and covenants
contained herein, the parties agree as follows:

{'=' * 75}
                    ARTICLE I - GENERAL PROVISIONS
{'=' * 75}

1.1 SEPARATION: The parties shall live separate and apart from each
    other, free from interference, authority, and control by the other.

1.2 NON-MOLESTATION: Neither party shall molest, annoy, harass, or
    interfere with the other.

1.3 DEBTS: Except as otherwise provided herein, each party shall be
    responsible for his/her own debts incurred after the date of this
    Agreement.

{'=' * 75}
                    ARTICLE II - GROUNDS FOR DIVORCE
{'=' * 75}

2.1 The parties consent to the entry of a Judgment of Divorce based
    upon DRL §170(7), the irretrievable breakdown of the marriage for
    a period of at least six months.

2.2 All ancillary issues shall be resolved by this Agreement and
    incorporated but not merged into the Judgment of Divorce.

{children_section}

{'=' * 75}
                    ARTICLE IV - CHILD SUPPORT
{'=' * 75}

4.1 BASIC CHILD SUPPORT:
    _________________ shall pay to _________________ as child support
    the sum of ${child_support_monthly:,.2f} per month, payable on the
    _____ day of each month.

4.2 This amount represents the parties' agreement based upon the Child
    Support Standards Act (DRL §240(1-b)).

4.3 ADD-ON EXPENSES: The parties shall share the following expenses
    pro rata based on their respective incomes:
    (a) Unreimbursed medical/dental expenses
    (b) Child care expenses (work-related)
    (c) Extracurricular activities (as mutually agreed)
    (d) Educational expenses (as mutually agreed)

4.4 HEALTH INSURANCE: _________________ shall maintain health insurance
    coverage for the child(ren).

4.5 LIFE INSURANCE: Each party shall maintain life insurance in the
    amount of $____________ naming the child(ren) as beneficiaries
    until the youngest child reaches age 21.

4.6 TERMINATION: Child support shall terminate upon the child attaining
    age 21, or upon the earlier occurrence of marriage, death,
    emancipation, or permanent residence away from the custodial parent.

{'=' * 75}
                    ARTICLE V - MAINTENANCE/SPOUSAL SUPPORT
{'=' * 75}

5.1 _________________ shall pay to _________________ as maintenance
    the sum of ${maintenance_monthly:,.2f} per month, payable on the
    _____ day of each month.

5.2 DURATION: Maintenance shall continue for {maintenance_duration},
    or until the earlier occurrence of:
    (a) Death of either party
    (b) Remarriage of the recipient
    (c) Cohabitation of the recipient (as defined by law)
    (d) [Other termination events]

5.3 [ ] Maintenance is NON-MODIFIABLE
    [ ] Maintenance is MODIFIABLE upon substantial change of circumstances

5.4 TAX TREATMENT: The parties acknowledge that under current tax law
    (post-2018), maintenance is neither deductible by the payor nor
    includable in the income of the recipient.

{'=' * 75}
                    ARTICLE VI - EQUITABLE DISTRIBUTION
{'=' * 75}

6.1 MARITAL RESIDENCE:
    Property Address: _______________________________________________

    [ ] The property shall be sold and proceeds divided _____% / _____%.
    [ ] _________________ shall retain the property and buy out the
        other party's interest for $____________.
    [ ] _________________ shall have exclusive occupancy until _________.

6.2 RETIREMENT ACCOUNTS:
    _________________ shall receive _____% of the marital portion of
    _________________'s retirement account(s) by Qualified Domestic
    Relations Order (QDRO).

6.3 BANK ACCOUNTS:
    Each party shall retain the accounts currently titled in his/her name.
    Joint accounts shall be divided as follows: ________________________

6.4 VEHICLES:
    Plaintiff shall retain: __________________________________________
    Defendant shall retain: __________________________________________

6.5 PERSONAL PROPERTY:
    The parties have divided their personal property to their mutual
    satisfaction.

6.6 DEBTS:
    The following debts shall be paid by Plaintiff: ___________________
    The following debts shall be paid by Defendant: ___________________

{'=' * 75}
                    ARTICLE VII - COUNSEL FEES
{'=' * 75}

7.1 [ ] Each party shall be responsible for his/her own attorney's fees.
    [ ] _________________ shall pay $____________ toward _________________'s
        attorney's fees.

{'=' * 75}
                    ARTICLE VIII - GENERAL PROVISIONS
{'=' * 75}

8.1 FULL DISCLOSURE: Each party represents that he/she has made full
    and complete disclosure of all assets and liabilities.

8.2 ENTIRE AGREEMENT: This Agreement constitutes the entire agreement
    between the parties and supersedes all prior agreements.

8.3 MODIFICATIONS: This Agreement may only be modified in writing
    signed by both parties.

8.4 GOVERNING LAW: This Agreement shall be governed by the laws of
    the State of New York.

8.5 INCORPORATION: This Agreement shall be incorporated but not merged
    into the Judgment of Divorce.

8.6 EXECUTION: This Agreement may be executed in counterparts.

{'=' * 75}
                    ACKNOWLEDGMENT AND SIGNATURES
{'=' * 75}

IN WITNESS WHEREOF, the parties have executed this Agreement on the
date first written above.


_________________________________          _______________
{plaintiff.name}                           Date


_________________________________          _______________
{defendant.name}                           Date


{'=' * 75}
                         ATTORNEY CERTIFICATION
{'=' * 75}

I, _________________________, Esq., attorney for {plaintiff.name},
certify that I have reviewed this Agreement with my client and that
my client understands its terms and signs it voluntarily.

_________________________________          _______________
Attorney for Plaintiff                     Date


I, _________________________, Esq., attorney for {defendant.name},
certify that I have reviewed this Agreement with my client and that
my client understands its terms and signs it voluntarily.

_________________________________          _______________
Attorney for Defendant                     Date


{'=' * 75}
                           ACKNOWLEDGMENT
{'=' * 75}

STATE OF NEW YORK    )
                     ) ss.:
COUNTY OF {county.upper()}    )

On this _____ day of _____________, 20___, before me personally appeared
{plaintiff.name}, to me known and known to me to be the individual
described in and who executed the foregoing instrument, and duly
acknowledged to me that he/she executed the same.

_________________________________
Notary Public


STATE OF NEW YORK    )
                     ) ss.:
COUNTY OF {county.upper()}    )

On this _____ day of _____________, 20___, before me personally appeared
{defendant.name}, to me known and known to me to be the individual
described in and who executed the foregoing instrument, and duly
acknowledged to me that he/she executed the same.

_________________________________
Notary Public

{'=' * 75}

PREPARED BY:
{self.firm_name}
{self.firm_address}
{self.firm_phone}

{'=' * 75}
"""
        return template


def create_document_templates(firm_config=None) -> DocumentTemplates:
    """Factory function to create document templates"""
    if firm_config:
        return DocumentTemplates(
            firm_name=firm_config.firm_name,
            firm_address=firm_config.address,
            firm_phone=firm_config.phone
        )
    return DocumentTemplates()
