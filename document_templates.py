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


    def generate_engagement_letter(self,
                                   client: PartyInfo,
                                   case_type: str,
                                   retainer_amount: float,
                                   hourly_rate: float,
                                   scope_of_representation: List[str]) -> str:
        """
        Generate Attorney-Client Engagement Letter / Retainer Agreement
        """
        today = datetime.now().strftime("%B %d, %Y")

        scope_text = "\n".join([f"        • {item}" for item in scope_of_representation])

        template = f"""
{'=' * 75}
                        {self.firm_name.upper()}
                        ATTORNEYS AT LAW
{'=' * 75}

{self.firm_address}
{self.firm_phone}

{today}

VIA HAND DELIVERY / EMAIL

{client.name}
{client.address}
{client.city}, {client.state} {client.zip_code}

        RE: Engagement Letter and Retainer Agreement
            Matter: {case_type}

Dear {client.name.split()[0]}:

Thank you for selecting {self.firm_name} to represent you in connection with
the above-referenced matter. This letter will confirm the terms of our
engagement and serves as our written retainer agreement as required by
22 NYCRR Part 1215.

{'=' * 75}
                    1. SCOPE OF REPRESENTATION
{'=' * 75}

You have retained this firm to represent you in connection with:

{scope_text}

This representation does NOT include:
        • Appeals
        • Enforcement proceedings after final judgment
        • Modifications after final judgment
        • Criminal matters
        • Bankruptcy proceedings
        • Any matters not specifically listed above

{'=' * 75}
                    2. LEGAL FEES AND BILLING
{'=' * 75}

A. RETAINER:
   You agree to pay a retainer in the amount of ${retainer_amount:,.2f}.
   This retainer is due upon signing this agreement and is required before
   we can begin work on your matter.

   The retainer will be deposited into our Attorney Trust Account (IOLA)
   and will be applied against legal fees and disbursements as they are
   incurred. You will receive monthly statements showing charges against
   the retainer.

   If the retainer is exhausted, you agree to replenish it upon request.
   Any unused portion of the retainer will be refunded to you at the
   conclusion of the representation.

B. HOURLY RATES:
   Our current hourly rates are as follows:

   Partners:                    ${hourly_rate:,.2f} per hour
   Associates:                  ${hourly_rate * 0.75:,.2f} per hour
   Paralegals:                  ${hourly_rate * 0.40:,.2f} per hour
   Law Clerks:                  ${hourly_rate * 0.35:,.2f} per hour

   These rates are subject to change with 30 days' written notice.

C. BILLING INCREMENTS:
   Time is recorded and billed in increments of one-tenth (0.1) of an hour
   (6 minutes).

D. DISBURSEMENTS:
   In addition to legal fees, you will be responsible for all costs and
   disbursements incurred in connection with your matter, including but
   not limited to:

        • Court filing fees
        • Process server fees
        • Deposition transcript costs
        • Expert witness fees
        • Photocopying ($.25 per page)
        • Postage and overnight delivery
        • Travel expenses
        • Court reporter fees
        • Investigation costs

E. BILLING STATEMENTS:
   You will receive monthly billing statements. Payment is due within
   30 days of the statement date. Accounts more than 60 days past due
   may accrue interest at the rate of 1% per month.

{'=' * 75}
                    3. CLIENT RESPONSIBILITIES
{'=' * 75}

To enable us to represent you effectively, you agree to:

        • Provide complete and accurate information
        • Respond promptly to our requests for information or documents
        • Keep us informed of any changes in your contact information
        • Attend all court appearances and meetings as required
        • Pay all fees and costs in a timely manner
        • Cooperate fully in the preparation of your case

{'=' * 75}
                    4. COMMUNICATION
{'=' * 75}

We will keep you informed of significant developments in your case. You
may contact us by telephone or email during regular business hours.
We will endeavor to return all calls and emails within 24-48 business hours.

Emergency contact information will be provided for urgent matters that
arise outside of business hours.

{'=' * 75}
                    5. NO GUARANTEE OF OUTCOME
{'=' * 75}

While we will use our best efforts to achieve a favorable outcome, we
cannot and do not guarantee any particular result. The outcome of any
legal matter depends on many factors beyond our control, including the
facts, the law, the judge assigned to the case, and the actions of
opposing parties.

{'=' * 75}
                    6. TERMINATION
{'=' * 75}

Either party may terminate this agreement at any time upon written notice.
If you terminate our representation, you will remain responsible for all
fees and costs incurred through the date of termination.

If we determine that we must withdraw from the representation, we will
give you reasonable notice and take steps to protect your interests,
including returning your file and assisting in the transfer to new counsel.

{'=' * 75}
                    7. FILE RETENTION
{'=' * 75}

Upon conclusion of the matter, your file will be retained for a period
of seven (7) years, after which it may be destroyed. Original documents
will be returned to you upon request.

{'=' * 75}
                    8. ACKNOWLEDGMENT
{'=' * 75}

By signing below, you acknowledge that:

        • You have read and understand this agreement
        • You have had the opportunity to ask questions
        • You agree to the terms set forth herein
        • You have received a copy of this signed agreement

If these terms are acceptable, please sign and date both copies of this
letter, retain one copy for your records, and return the other copy to
us along with your retainer check.

We look forward to working with you and will do everything we can to
achieve the best possible outcome in your case.

Very truly yours,

{self.firm_name}


_________________________________
Attorney Name, Esq.


{'=' * 75}
                    ACKNOWLEDGMENT AND AGREEMENT
{'=' * 75}

I, {client.name}, have read and understand this Engagement Letter and
Retainer Agreement. I agree to the terms set forth herein and acknowledge
receipt of a copy of this agreement.


_________________________________          _______________
{client.name}                              Date


Retainer Amount Enclosed: $_______________

Check Number: _______________

{'=' * 75}

                    22 NYCRR PART 1215 NOTICE

        This law firm is required to provide you with this
        written letter of engagement pursuant to the rules
        of the Appellate Division of the Supreme Court.

{'=' * 75}
"""
        return template

    def generate_initial_client_letter(self,
                                       client: PartyInfo,
                                       case_type: str,
                                       next_steps: List[str],
                                       documents_needed: List[str]) -> str:
        """
        Generate Initial Client Letter / Welcome Letter
        """
        today = datetime.now().strftime("%B %d, %Y")

        next_steps_text = "\n".join([f"        {i+1}. {step}" for i, step in enumerate(next_steps)])
        docs_text = "\n".join([f"        □ {doc}" for doc in documents_needed])

        template = f"""
{'=' * 75}
                        {self.firm_name.upper()}
                        ATTORNEYS AT LAW
{'=' * 75}

{self.firm_address}
{self.firm_phone}

{today}

{client.name}
{client.address}
{client.city}, {client.state} {client.zip_code}

        RE: {case_type}
            Our File No.: _______________

Dear {client.name.split()[0]}:

Welcome to {self.firm_name}. We are pleased to have you as a client and
are committed to providing you with excellent legal representation.

This letter provides important information about your case and outlines
the next steps in the process.

{'=' * 75}
                    YOUR LEGAL TEAM
{'=' * 75}

Your matter has been assigned to:

        Attorney:           _____________________________, Esq.
        Paralegal:          _____________________________
        Direct Line:        _____________________________
        Email:              _____________________________

Please feel free to contact us with any questions or concerns.

{'=' * 75}
                    CASE OVERVIEW
{'=' * 75}

Matter Type:            {case_type}
Date Opened:            {today}
Court:                  To be determined
Index/Docket Number:    To be assigned upon filing

{'=' * 75}
                    NEXT STEPS
{'=' * 75}

The following steps will be taken in your matter:

{next_steps_text}

{'=' * 75}
                    DOCUMENTS NEEDED
{'=' * 75}

To proceed effectively with your case, we will need the following
documents. Please provide these at your earliest convenience:

{docs_text}

Please bring original documents if available; we will make copies and
return the originals to you.

{'=' * 75}
                    IMPORTANT REMINDERS
{'=' * 75}

1. COMMUNICATION:
   • Notify us immediately of any changes to your address, phone number,
     or email address
   • Do not communicate with the opposing party about your case
   • Forward any legal documents you receive to us immediately
   • Do not post about your case on social media

2. COURT APPEARANCES:
   • We will notify you of all court dates well in advance
   • You MUST appear at all scheduled court appearances
   • Dress professionally and arrive 30 minutes early
   • Failure to appear may result in default judgment against you

3. FINANCIAL MATTERS:
   • Do not make major financial decisions without consulting us first
   • Do not hide, transfer, or dissipate marital assets
   • Maintain all joint accounts and credit cards as they currently exist
   • Continue to pay all regular household bills and expenses

4. CHILDREN:
   • Maintain stability and routine for your children
   • Do not disparage the other parent in front of the children
   • Do not interfere with the other parent's time with the children
   • Document any concerns about the children's welfare

{'=' * 75}
                    WHAT TO EXPECT
{'=' * 75}

Depending on the complexity of your case, the process typically takes:

        Uncontested Divorce:        3-6 months
        Contested Divorce:          9-18 months
        Custody/Visitation:         6-12 months
        Child Support:              3-6 months
        Order of Protection:        Temporary order within days;
                                    Final hearing within weeks

These are estimates only. Every case is unique, and actual timeframes
may vary based on court schedules, the cooperation of the parties, and
other factors.

{'=' * 75}
                    OUR COMMITMENT TO YOU
{'=' * 75}

We understand that this is a difficult time for you and your family.
Our firm is committed to:

        • Treating you with respect and compassion
        • Keeping you informed about your case
        • Responding to your calls and emails promptly
        • Advocating zealously on your behalf
        • Working toward the best possible outcome

{'=' * 75}

If you have any questions about this letter or your case, please do not
hesitate to contact us. We look forward to working with you.

Very truly yours,

{self.firm_name}


_________________________________
Attorney Name, Esq.


Enclosures:
        □ Engagement Letter and Retainer Agreement
        □ Client Intake Form
        □ Authorization for Release of Information
        □ Fee Schedule

{'=' * 75}
"""
        return template

    def generate_demand_letter(self,
                               client: PartyInfo,
                               opposing_party: PartyInfo,
                               case_type: str,
                               demands: List[str],
                               deadline_days: int = 20) -> str:
        """
        Generate Initial Demand Letter to Opposing Party
        """
        today = datetime.now().strftime("%B %d, %Y")

        demands_text = "\n".join([f"        {i+1}. {demand}" for i, demand in enumerate(demands)])

        template = f"""
{'=' * 75}
                        {self.firm_name.upper()}
                        ATTORNEYS AT LAW
{'=' * 75}

{self.firm_address}
{self.firm_phone}

{today}

VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED

{opposing_party.name}
{opposing_party.address}
{opposing_party.city}, {opposing_party.state} {opposing_party.zip_code}

        RE: {case_type}
            Our Client: {client.name}

Dear {opposing_party.name.split()[-1]}:

Please be advised that this firm represents {client.name} in connection
with the above-referenced matter. All future communications regarding
this matter should be directed to this office. Please do not contact
our client directly.

{'=' * 75}
                    STATEMENT OF FACTS
{'=' * 75}

[Insert relevant facts of the case]

{'=' * 75}
                    DEMANDS
{'=' * 75}

On behalf of our client, we hereby demand the following:

{demands_text}

{'=' * 75}
                    RESPONSE REQUIRED
{'=' * 75}

Please respond to this letter within {deadline_days} days of receipt.
If we do not receive a satisfactory response by that time, we are
authorized to commence legal proceedings without further notice.

We believe it is in both parties' best interest to resolve this matter
amicably and without the expense and uncertainty of litigation. To that
end, we invite you or your attorney to contact us to discuss settlement
options.

{'=' * 75}
                    PRESERVATION OF EVIDENCE
{'=' * 75}

You are hereby placed on notice to preserve all documents, records,
communications, and other evidence related to this matter. This includes,
but is not limited to:

        • Financial records (bank statements, tax returns, pay stubs)
        • Communications (emails, text messages, letters)
        • Photographs and videos
        • Social media posts
        • Electronic data

Destruction or spoliation of evidence may result in sanctions and
adverse inferences in any legal proceedings.

{'=' * 75}
                    STATUTE OF LIMITATIONS
{'=' * 75}

Please be advised that various statutes of limitations may apply to
claims arising from this matter. This letter is not intended to waive
or extend any applicable limitation periods. All rights are expressly
reserved.

{'=' * 75}

This letter is written in an effort to resolve this dispute without
litigation. It is not intended to be a complete recitation of all facts,
claims, or defenses, all of which are expressly reserved.

We look forward to your prompt response.

Very truly yours,

{self.firm_name}


_________________________________
Attorney Name, Esq.

cc: {client.name} (via email)

{'=' * 75}
"""
        return template

    def generate_opposing_counsel_letter(self,
                                         client: PartyInfo,
                                         opposing_party: PartyInfo,
                                         opposing_attorney: str,
                                         opposing_firm: str,
                                         opposing_address: str,
                                         case_type: str,
                                         index_number: str = "") -> str:
        """
        Generate Letter to Opposing Counsel
        """
        today = datetime.now().strftime("%B %d, %Y")

        template = f"""
{'=' * 75}
                        {self.firm_name.upper()}
                        ATTORNEYS AT LAW
{'=' * 75}

{self.firm_address}
{self.firm_phone}

{today}

VIA EMAIL AND FIRST CLASS MAIL

{opposing_attorney}, Esq.
{opposing_firm}
{opposing_address}

        RE: {client.name} v. {opposing_party.name}
            Index No.: {index_number if index_number else "Not Yet Assigned"}

Dear Counselor:

Please be advised that this firm has been retained to represent
{client.name} in connection with the above-referenced matter.

Kindly direct all future communications regarding this case to my
attention. Please confirm your representation of {opposing_party.name}
at your earliest convenience.

{'=' * 75}
                    PRELIMINARY CONFERENCE
{'=' * 75}

[ ] We have not yet filed the action. We would like to explore the
    possibility of settlement before commencing litigation.

[ ] We have filed the action. A Preliminary Conference has been
    scheduled for _____________ at _____________.

[ ] The Preliminary Conference is yet to be scheduled. We will
    notify you once we receive a date from the court.

{'=' * 75}
                    DISCOVERY
{'=' * 75}

[ ] Enclosed please find our client's Statement of Net Worth and
    supporting documentation. Please provide your client's Net Worth
    Statement and supporting documentation within 20 days.

[ ] We request that you provide us with your client's Statement of
    Net Worth and supporting documentation pursuant to 22 NYCRR 202.16(b).

[ ] We are preparing discovery demands and will forward them to you
    shortly.

{'=' * 75}
                    TEMPORARY RELIEF
{'=' * 75}

[ ] Our client intends to file a motion for pendente lite relief,
    including [child support / maintenance / counsel fees / exclusive
    occupancy]. We would prefer to reach a temporary agreement without
    motion practice if possible.

[ ] We are open to discussing temporary arrangements to maintain the
    status quo during the pendency of this action.

{'=' * 75}
                    SETTLEMENT
{'=' * 75}

[ ] Our client is interested in exploring settlement. Please let us
    know if your client is amenable to a four-way conference.

[ ] We believe this matter is appropriate for mediation. Please advise
    if your client would be willing to participate in mediation.

[ ] Our client is prepared to proceed to trial if a fair settlement
    cannot be reached.

{'=' * 75}

Please contact me at your earliest convenience to discuss how we can
move this matter forward efficiently.

Very truly yours,

{self.firm_name}


_________________________________
Attorney Name, Esq.

cc: {client.name} (via email)

Enclosures: [ ] Statement of Net Worth
            [ ] Supporting Documentation
            [ ] ______________

{'=' * 75}
"""
        return template

    def generate_notice_of_appearance(self,
                                      client: PartyInfo,
                                      opposing_party: PartyInfo,
                                      county: str,
                                      index_number: str,
                                      attorney_name: str) -> str:
        """
        Generate Notice of Appearance
        """
        today = datetime.now().strftime("%B %d, %Y")

        template = f"""
{'=' * 75}
                    SUPREME COURT OF THE STATE OF NEW YORK
                           COUNTY OF {county.upper()}
{'=' * 75}

{client.name},
                                                    Plaintiff,
        -against-                                   Index No.: {index_number}

{opposing_party.name},
                                                    Defendant.
{'=' * 75}

                         NOTICE OF APPEARANCE

{'=' * 75}

PLEASE TAKE NOTICE that the undersigned attorney hereby appears on
behalf of the [Plaintiff / Defendant], {client.name}, in the
above-entitled action.

All papers and pleadings in this action may be served upon the
undersigned at the address set forth below.


Dated: {today}

                                        {self.firm_name}
                                        Attorneys for [Plaintiff/Defendant]


                                        By: _________________________
                                            {attorney_name}, Esq.

                                        {self.firm_address}
                                        {self.firm_phone}


TO:     [Opposing Counsel Name], Esq.
        [Opposing Firm Name]
        [Opposing Firm Address]
        Attorneys for [Plaintiff/Defendant]

{'=' * 75}
"""
        return template

    def generate_summons_with_notice(self,
                                    plaintiff: PartyInfo,
                                    defendant: PartyInfo,
                                    county: str,
                                    relief_requested: List[str]) -> str:
        """
        Generate Summons with Notice for Divorce
        """
        today = datetime.now().strftime("%B %d, %Y")

        relief_text = "\n".join([f"        [ ] {relief}" for relief in relief_requested])

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

                         SUMMONS WITH NOTICE

{'=' * 75}

ACTION FOR DIVORCE

To the above-named Defendant:

YOU ARE HEREBY SUMMONED to serve a notice of appearance on the
Plaintiff's attorney within twenty (20) days after the service of
this summons, exclusive of the day of service (or within thirty (30)
days after the service is complete if this summons is not personally
delivered to you within the State of New York); and in case of your
failure to appear, judgment will be taken against you by default for
the relief demanded in the notice set forth below.

Dated: {today}

                                        {self.firm_name}
                                        Attorneys for Plaintiff

                                        By: _________________________

                                        {self.firm_address}
                                        {self.firm_phone}


{'=' * 75}
                              NOTICE
{'=' * 75}

The nature of this action is to dissolve the marriage between the
parties on the grounds of:

        [X] The relationship between husband and wife has broken down
            irretrievably for a period of at least six months
            (DRL §170(7) - Irretrievable Breakdown)

        [ ] Other grounds: _________________________________

The relief sought is:

{relief_text}

        [ ] A judgment of absolute divorce in favor of the Plaintiff
            dissolving the marriage between the parties

        [ ] Equitable distribution of marital property pursuant to
            DRL §236(B)(5)

        [ ] Maintenance/Spousal Support pursuant to DRL §236(B)(6)

        [ ] Child custody and visitation

        [ ] Child support pursuant to DRL §240

        [ ] Counsel fees and expenses

        [ ] Exclusive use and occupancy of the marital residence

        [ ] Such other and further relief as the Court deems just
            and proper


{'=' * 75}
                    NOTICE OF AUTOMATIC ORDERS
                      (DRL §236(B)(2)(b))
{'=' * 75}

PURSUANT TO DOMESTIC RELATIONS LAW §236(B)(2)(b), UPON SERVICE OF
THIS SUMMONS, THE FOLLOWING AUTOMATIC ORDERS SHALL BE IN EFFECT
AGAINST BOTH PARTIES UNTIL THE FINAL JUDGMENT IS ENTERED OR THE
ACTION IS DISMISSED:

(1) Neither party shall sell, transfer, encumber, conceal, assign,
    remove or in any way dispose of, without the consent of the
    other party in writing, or by order of the court, any property
    (including, but not limited to, real estate, personal property,
    cash accounts, stocks, mutual funds, bank accounts, cars and
    boats) individually or jointly held by the parties, except in
    the usual course of business, for customary and usual household
    expenses or for reasonable attorney's fees in connection with
    this action.

(2) Neither party shall transfer, encumber, assign, remove, withdraw
    or in any way dispose of any tax deferred funds, stocks or other
    assets held in any individual retirement accounts, 401K accounts,
    profit sharing plans, Keogh accounts, or any other pension or
    retirement account, and the parties shall further refrain from
    applying for or requesting the payment of retirement benefits or
    annuity payments of any kind, without the consent of the other
    party in writing, or upon further order of the court.

(3) Neither party shall incur unreasonable debts hereafter, including,
    but not limited to, further borrowing against any credit line
    secured by the family residence, further ## encumbering any assets,
    or unreasonably using credit cards or cash advances against credit
    cards, except in the usual course of business or for customary or
    usual household expenses, or for reasonable attorney's fees in
    connection with this action.

(4) Neither party shall cause the other party or the children of the
    marriage to be removed from any existing medical, hospital and
    dental insurance coverage, and each party shall maintain the
    existing medical, hospital and dental insurance coverage in full
    force and effect.

(5) Neither party shall change the beneficiaries of any existing life
    insurance policies, and each party shall maintain the existing life
    insurance, automobile insurance, homeowner's and renter's insurance
    policies in full force and effect.

{'=' * 75}
                    NOTICE OF GUIDELINE MAINTENANCE
                        (DRL §236(B)(6))
{'=' * 75}

The maintenance guideline obligation is computed pursuant to a formula
set forth in Domestic Relations Law §236(B)(6). For more information,
visit: www.nycourts.gov/divorce

{'=' * 75}
                    NOTICE CONCERNING CONTINUATION
                    OF HEALTH CARE COVERAGE
{'=' * 75}

Pursuant to DRL §255, please take notice that upon the entry of a
judgment of divorce, the non-titled spouse may no longer be allowed to
receive health coverage under the titled spouse's employer-provided
group insurance. The non-titled spouse may be entitled to purchase
COBRA continuation coverage at the group rate for a limited period.

{'=' * 75}

                                        {self.firm_name}
                                        Attorneys for Plaintiff

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
