# 🛎️ Life Admin Concierge Agent - Sprint Plan

> **Kaggle Agents Intensive Capstone Project**  
> **Track:** Concierge Agents (Personal Life)  
> **Deadline:** December 1, 2025 11:59 AM PT (~2 days)  
> **Team Size:** 2-3 active members

---

## 🎯 Project Pitch

### Problem Statement
Managing personal life admin tasks is tedious and time-consuming. People forget license renewals, insurance deadlines, and struggle to prioritize daily tasks effectively. Important personal data (license numbers, insurance policies) is scattered across documents.

### Solution: Life Admin Concierge Agent
An intelligent multi-agent system that:
1. **Life Admin Automator** - Handles renewals, drafts emails, creates calendar events
2. **Personal Productivity Dashboard** - Daily task prioritization using Eisenhower Matrix
3. **Personal Profile Vault** - Instant access to personal metadata (license #, insurance, etc.)

### Value Proposition
- Reduces time spent on life admin by 5+ hours/week
- Never miss a renewal deadline again
- Smart task prioritization based on energy levels
- One-stop access to all personal documents/info

---

## ✅ Requirements Checklist (Need 3+, Targeting 6)

| # | Feature | Status | Implementation |
|---|---------|--------|----------------|
| 1 | **Multi-agent system** | 🎯 Target | Router + AdminAgent + ProductivityAgent |
| 2 | **Tools** | 🎯 Target | Google Calendar, Gmail Draft, Custom Tools |
| 3 | **Sessions & Memory** | 🎯 Target | InMemorySessionService / InMemoryChatMessageHistory |
| 4 | **Context Engineering** | 🎯 Target | USER_PROFILE injection (no Vector DB needed) |
| 5 | **Observability** | 🎯 Target | Logging/print statements in tools |
| 6 | **Agent Evaluation** | 🎯 Target | Test script with 5+ test cases |
| 7 | A2A Protocol | ⏭️ Skip | Too complex for timeline |
| 8 | Agent Deployment | ⏭️ Optional | Bonus points if time permits |
| 9 | Long-running ops | ⏭️ Skip | Too complex for timeline |

**Bonus Points Targets:**
- [x] Use Gemini (+5 pts)
- [ ] Deployment (+5 pts) - Optional
- [ ] YouTube Video (+10 pts) - Recommended

---

## 👥 Task Assignments

### 🏗️ MEMBER A: "The Architect" (Core Logic & Context)

**Focus:** Profile Data + Eisenhower Logic + Evaluation Script

#### Task A1: Profile Data System (2-3 hours)
Create `profile_data.py` with user context injection:
```python
# profile_data.py
USER_PROFILE = """
--- IDENTITY DOCUMENTS ---
Driver's License: ID #D99887766, Exp: 2025-12-15, State: CA
Passport: ID #P11223344, Exp: 2029-05-20
Insurance: Geico Policy #999-000, Exp: 2024-12-01, Premium: $150/month

--- PERSONAL INFO ---
Name: John Doe
DOB: 1990-05-15
Address: 123 Main St, San Francisco, CA 94102
Emergency Contact: Jane Doe, +1-555-123-4567

--- PREFERENCES ---
Energy Level: Variable (LOW in mornings, HIGH afternoons)
Work Hours: 9 AM - 5 PM PST
Preferred Communication: Email
"""

RENEWAL_REMINDERS = """
--- UPCOMING RENEWALS ---
1. Driver's License - Expires: Dec 15, 2025 (15 days away!)
2. Car Insurance - Expires: Dec 01, 2024 (OVERDUE - needs attention)
3. Passport - Expires: May 20, 2029 (OK)
4. Netflix Subscription - Renews: Dec 05, 2025
5. Gym Membership - Renews: Jan 01, 2026
"""
```

#### Task A2: Eisenhower Matrix Logic (2 hours)
Create prompt template for task prioritization:
```python
EISENHOWER_PROMPT = """
You are a productivity expert using the Eisenhower Matrix.
User's current energy level: {energy_level}
Current time: {current_time}
Task list: {task_list}

Categorize each task:
- Q1 (Do First): Urgent AND Important
- Q2 (Schedule): Important NOT Urgent  
- Q3 (Delegate): Urgent NOT Important
- Q4 (Eliminate): NOT Urgent NOT Important

IF energy is LOW: Recommend Q3/Q4 tasks (easy wins)
IF energy is HIGH: Recommend Q1/Q2 tasks (deep work)

Return JSON: {{"prioritized_tasks": [...], "recommended_schedule": [...]}}
"""
```

#### Task A3: Evaluation Script (2-3 hours)
Create `test_agent.py`:
```python
TEST_CASES = [
    {"query": "What's my driver's license number?", "expected_contains": ["D99887766"]},
    {"query": "What renewals are coming up?", "expected_contains": ["Driver's License", "Dec"]},
    {"query": "Draft an email to remind me about insurance", "expected_contains": ["insurance", "renew"]},
    {"query": "I'm tired, what should I do today?", "expected_contains": ["easy", "low energy"]},
    {"query": "Create a calendar event for license renewal", "expected_contains": ["calendar", "event"]},
]
```

---

### 🔌 MEMBER B: "The Integrator" (Google API Tools)

**Focus:** Google Calendar + Gmail Draft Functions

#### Task B1: Google Cloud Setup (1-2 hours)
1. Go to Google Cloud Console
2. Create new project or use existing
3. Enable APIs:
   - Google Calendar API
   - Gmail API
4. Create OAuth 2.0 credentials OR Service Account
5. Download `credentials.json`
6. Add to Kaggle Secrets (if using Kaggle Notebook)

#### Task B2: Calendar Tool (2-3 hours)
```python
# tools/calendar_tool.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def create_calendar_event(title: str, start_time: str, duration_hours: int = 1, description: str = ""):
    """
    Creates a Google Calendar event.
    
    Args:
        title: Event title
        start_time: ISO format datetime string
        duration_hours: Event duration in hours
        description: Event description
    
    Returns:
        dict with event details or error
    """
    print(f"[TOOL LOG] Creating calendar event: {title} at {start_time}")
    
    # Implementation with google-api-python-client
    # Return event link on success
    pass
```

#### Task B3: Gmail Draft Tool (2-3 hours)
```python
# tools/gmail_tool.py
def create_gmail_draft(to: str, subject: str, body: str):
    """
    Creates a Gmail draft (does NOT send).
    
    Args:
        to: Recipient email
        subject: Email subject
        body: Email body text
    
    Returns:
        dict with draft ID or error
    """
    print(f"[TOOL LOG] Creating draft to: {to}, subject: {subject}")
    
    # Implementation with google-api-python-client
    pass
```

**⚠️ Important:** For demo purposes, if Google Auth is too complex, create MOCK versions that return simulated responses. This still demonstrates the tool architecture!

---

### 🎮 MEMBER C: "The Driver" (Orchestration & Assembly)

**Focus:** Main Agent, Integration, Demo, Submission

#### Task C1: Main Agent Setup (3-4 hours)
```python
# main_agent.py
from google import genai
from google.genai import types

# Import from teammates
from profile_data import USER_PROFILE, RENEWAL_REMINDERS
from tools.calendar_tool import create_calendar_event
from tools.gmail_tool import create_gmail_draft
from eisenhower import prioritize_tasks

# Initialize Gemini
client = genai.Client(api_key="YOUR_API_KEY")

# Define tools for the agent
tools = [
    create_calendar_event,
    create_gmail_draft,
    prioritize_tasks,
    get_profile_info,
    get_renewal_reminders,
]

# System instruction with context injection
SYSTEM_INSTRUCTION = f"""
You are a Life Admin Concierge Agent helping users manage their personal life.

USER PROFILE (Always available):
{USER_PROFILE}

RENEWAL CALENDAR:
{RENEWAL_REMINDERS}

Your capabilities:
1. Answer questions about user's personal information
2. Create calendar events for reminders
3. Draft emails for renewals or other tasks
4. Prioritize tasks using Eisenhower Matrix
5. Suggest daily schedules based on energy level

Always be helpful, proactive about upcoming deadlines, and suggest actions.
"""
```

#### Task C2: Multi-Agent Router (2-3 hours)
```python
# agents/router.py
class RouterAgent:
    """Routes queries to appropriate sub-agent"""
    
    def route(self, query: str) -> str:
        """Determine which agent should handle this query"""
        if any(word in query.lower() for word in ["calendar", "event", "schedule", "remind"]):
            return "admin_agent"
        elif any(word in query.lower() for word in ["task", "priority", "eisenhower", "energy", "todo"]):
            return "productivity_agent"
        elif any(word in query.lower() for word in ["license", "passport", "insurance", "profile"]):
            return "profile_agent"
        else:
            return "general_agent"

class AdminAgent:
    """Handles life admin tasks: calendar, emails, reminders"""
    pass

class ProductivityAgent:
    """Handles task prioritization and scheduling"""
    pass
```

#### Task C3: Session Management (1-2 hours)
```python
# session/memory.py
from datetime import datetime

class InMemorySession:
    """Simple in-memory session for conversation history"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = []
        self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_history(self) -> list:
        return self.history
    
    def clear(self):
        self.history = []
```

#### Task C4: Observability (1 hour)
Add logging to all tools:
```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ConciergeAgent")

def log_tool_call(tool_name: str, args: dict, result: any):
    logger.info(f"[{datetime.now().isoformat()}] Tool: {tool_name}")
    logger.info(f"  Args: {args}")
    logger.info(f"  Result: {result}")
```

#### Task C5: Demo & Video (2-3 hours)
1. Screen record the agent working
2. Show: Query → Agent thinks → Tool called → Result
3. Demonstrate all 3+ features
4. Keep under 3 minutes

#### Task C6: Writeup & Submission (2-3 hours)
- Title & Subtitle
- Problem/Solution description (<1500 words)
- Architecture diagram
- Link to GitHub/Kaggle Notebook

---

## 📁 Project Structure

```
life-admin-concierge/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── main.py                   # Entry point
├── config.py                 # Configuration & API keys
│
├── agents/
│   ├── __init__.py
│   ├── router.py            # Router agent
│   ├── admin_agent.py       # Life admin agent
│   └── productivity_agent.py # Productivity agent
│
├── tools/
│   ├── __init__.py
│   ├── calendar_tool.py     # Google Calendar integration
│   ├── gmail_tool.py        # Gmail draft tool
│   └── profile_tool.py      # Profile lookup tool
│
├── data/
│   ├── profile_data.py      # User profile context
│   └── eisenhower.py        # Eisenhower matrix logic
│
├── session/
│   ├── __init__.py
│   └── memory.py            # In-memory session management
│
├── evaluation/
│   ├── __init__.py
│   └── test_agent.py        # Evaluation test cases
│
└── notebooks/
    └── demo.ipynb           # Kaggle notebook for submission
```

---

## ⏰ Timeline (48 Hours)

### Day 1 (Today - Nov 30)

| Time | Member A | Member B | Member C |
|------|----------|----------|----------|
| Morning | Profile data system | Google Cloud setup | Project structure setup |
| Afternoon | Eisenhower logic | Calendar tool | Main agent skeleton |
| Evening | Evaluation script | Gmail tool | Router + Integration |

### Day 2 (Dec 1 - DEADLINE DAY)

| Time | Member A | Member B | Member C |
|------|----------|----------|----------|
| Morning (Early) | Testing & fixes | Tool testing | Full integration |
| Mid-Morning | Documentation | Mock fallbacks | Demo recording |
| Before Noon | Review | Review | SUBMIT by 11:59 AM PT |

---

## 🚀 Quick Start Commands

```bash
# Clone/setup
cd /Users/shouryaangrish/Documents/Work/AI\ Capstone\ Kaggle

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install google-generativeai google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Run main agent
python main.py

# Run tests
python -m pytest evaluation/test_agent.py -v
```

---

## 📋 Submission Checklist

- [ ] Code complete and tested
- [ ] README.md with clear instructions
- [ ] All 6 features documented
- [ ] Demo video recorded (optional but recommended)
- [ ] Kaggle writeup drafted
- [ ] GitHub repo public / Kaggle notebook ready
- [ ] **SUBMIT before Dec 1, 11:59 AM PT**

---

## 🔗 Resources

- [ADK Docs](https://google.github.io/adk-docs/)
- [Gemini API](https://ai.google.dev/docs)
- [Google Calendar API](https://developers.google.com/calendar/api)
- [Gmail API](https://developers.google.com/gmail/api)
- [Kaggle Competition Page](https://www.kaggle.com/competitions/agents-intensive-capstone-project)

---

## 💡 Tips for Success

1. **Start with mocks** - Get the agent logic working before real API integration
2. **Context injection > Vector DB** - Simpler and works for small profile data
3. **Print statements = Observability** - Easy win for the requirements
4. **Test early** - Don't wait until the last hour to test
5. **Video is 10 bonus points** - Worth the effort if you have time

Good luck! 🚀
