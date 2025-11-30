"""
User Profile Data - Context Injection for Life Admin Concierge Agent.

This module contains hardcoded user profile information that gets injected
into the agent's context. This approach eliminates the need for vector databases
while still demonstrating effective context engineering.

MEMBER A: Customize this with realistic sample data.
"""

# Main user profile - Contains identity documents and personal info
USER_PROFILE = """
=== IDENTITY DOCUMENTS ===

DRIVER'S LICENSE:
  - License Number: D99887766
  - State: California (CA)
  - Issue Date: 2021-12-15
  - Expiration Date: 2025-12-15
  - Class: C (Standard)
  - Address on file: 123 Main Street, San Francisco, CA 94102

PASSPORT:
  - Passport Number: P11223344
  - Country: United States
  - Issue Date: 2019-05-20
  - Expiration Date: 2029-05-20
  - Place of Issue: San Francisco Passport Agency

SOCIAL SECURITY:
  - Last 4 digits: XXX-XX-4567 (full number secured)

=== INSURANCE POLICIES ===

AUTO INSURANCE:
  - Provider: Geico
  - Policy Number: 999-000-1234
  - Coverage: Full Coverage
  - Premium: $150/month
  - Expiration Date: 2024-12-01 (NEEDS RENEWAL!)
  - Vehicles Covered: 2020 Toyota Camry (VIN: 1HGBH41JXMN109186)

HEALTH INSURANCE:
  - Provider: Blue Shield of California
  - Policy Number: BSC-789456
  - Plan: PPO Gold
  - Premium: $450/month (employer subsidized)
  - Member ID: 123456789

RENTERS INSURANCE:
  - Provider: Lemonade
  - Policy Number: LEM-2024-5678
  - Coverage: $30,000 personal property
  - Premium: $15/month
  - Expiration Date: 2025-03-15

=== PERSONAL INFORMATION ===

NAME: John Michael Doe
DATE OF BIRTH: May 15, 1990
EMAIL: johndoe@email.com
PHONE: +1 (555) 123-4567
ADDRESS: 
  123 Main Street, Apt 4B
  San Francisco, CA 94102

EMERGENCY CONTACT:
  - Name: Jane Doe (Sister)
  - Phone: +1 (555) 987-6543
  - Relationship: Sibling

=== PREFERENCES ===

WORK SCHEDULE:
  - Work Hours: 9:00 AM - 5:00 PM PST
  - Work Days: Monday - Friday
  - Lunch Break: 12:00 PM - 1:00 PM

ENERGY PATTERNS:
  - Morning (6-10 AM): LOW energy - prefer easy tasks
  - Mid-day (10 AM - 2 PM): HIGH energy - good for deep work
  - Afternoon (2-6 PM): MEDIUM energy - meetings okay
  - Evening (6+ PM): LOW energy - wind down

COMMUNICATION PREFERENCES:
  - Preferred: Email
  - Secondary: Text message
  - Do not disturb: 10 PM - 7 AM
"""

# Renewal reminders and upcoming deadlines
RENEWAL_REMINDERS = """
=== UPCOMING RENEWALS & DEADLINES ===

🔴 URGENT (Within 7 days):
  1. Car Insurance (Geico)
     - Expires: December 01, 2024
     - Status: OVERDUE - Needs immediate attention!
     - Action: Call Geico at 1-800-861-8380 or renew online
     - Estimated cost: $1,800/year

🟡 SOON (Within 30 days):
  2. Driver's License
     - Expires: December 15, 2025
     - Status: 15 days remaining
     - Action: Schedule DMV appointment or renew online at dmv.ca.gov
     - Fee: ~$38

  3. Netflix Subscription
     - Renews: December 05, 2025
     - Status: Auto-renewal ON
     - Monthly cost: $15.49

🟢 UPCOMING (30-90 days):
  4. Gym Membership (24 Hour Fitness)
     - Renews: January 01, 2026
     - Status: Annual renewal
     - Cost: $500/year
     - Note: Consider negotiating rate or switching gyms

  5. Renters Insurance (Lemonade)
     - Expires: March 15, 2025
     - Status: 105 days remaining
     - Action: Review coverage before renewal

✅ FAR OUT (90+ days):
  6. Passport
     - Expires: May 20, 2029
     - Status: Good for 4+ years
     - No action needed

=== RECURRING BILLS ===

MONTHLY:
  - Rent: $2,500 (due 1st of month)
  - Utilities: ~$150 (auto-pay)
  - Phone: $85 (T-Mobile, auto-pay)
  - Internet: $60 (Comcast, auto-pay)
  - Spotify: $10.99 (auto-pay)
  - iCloud: $2.99 (auto-pay)

ANNUAL:
  - Amazon Prime: $139 (renews July)
  - Domain renewal: $15 (renews September)
"""

# Task templates for common life admin tasks
TASK_TEMPLATES = {
    "license_renewal": {
        "title": "Renew Driver's License",
        "steps": [
            "Check if eligible for online renewal at dmv.ca.gov",
            "If not, schedule DMV appointment",
            "Gather required documents (current license, proof of residency)",
            "Pay renewal fee (~$38)",
            "Receive temporary license, wait for permanent"
        ],
        "estimated_time": "1-2 hours (online) or 2-4 hours (in-person)"
    },
    "insurance_renewal": {
        "title": "Renew Auto Insurance",
        "steps": [
            "Review current coverage and premium",
            "Get quotes from 2-3 competitors",
            "Decide to renew or switch",
            "Complete renewal/new policy online or by phone",
            "Update payment method if needed",
            "Print new insurance card for car"
        ],
        "estimated_time": "1-2 hours"
    },
    "travel_prep": {
        "title": "Travel Preparation Checklist",
        "steps": [
            "Check passport expiration (6+ months validity required)",
            "Book flights and accommodation",
            "Arrange pet/plant care if needed",
            "Set up mail hold with USPS",
            "Notify bank of travel dates",
            "Check health insurance coverage abroad",
            "Pack essentials and medications",
            "Share itinerary with emergency contact"
        ],
        "estimated_time": "2-4 hours"
    },
    "doctor_visit": {
        "title": "Doctor Visit Preparation",
        "steps": [
            "Confirm appointment date and time",
            "Review and update symptoms list",
            "List current medications",
            "Prepare questions for doctor",
            "Bring insurance card and ID",
            "Arrange transportation if needed"
        ],
        "estimated_time": "30 minutes prep"
    }
}


def get_profile_summary() -> str:
    """Returns a condensed summary of user profile for quick reference."""
    return """
    Quick Profile Summary:
    - Name: John Doe
    - License #: D99887766 (exp: Dec 15, 2025)
    - Passport #: P11223344 (exp: May 20, 2029)
    - Auto Insurance: Geico #999-000-1234 (EXPIRED - needs renewal!)
    - Email: johndoe@email.com
    - Phone: +1 (555) 123-4567
    """


def get_urgent_items() -> list:
    """Returns list of items needing immediate attention."""
    return [
        {
            "item": "Car Insurance",
            "status": "OVERDUE",
            "action": "Renew immediately",
            "priority": "CRITICAL"
        },
        {
            "item": "Driver's License", 
            "status": "Expires in 15 days",
            "action": "Schedule renewal",
            "priority": "HIGH"
        }
    ]
