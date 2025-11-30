# Life Admin Concierge Agent 🛎️

> Kaggle Agents Intensive Capstone Project - Concierge Track
> **Built with Google Agent Development Kit (ADK)**

A multi-agent system that automates personal life administration tasks, provides smart task prioritization, and serves as your personal data vault.

## 🎯 Problem Statement

Managing personal life admin is tedious:
- Forgetting renewal deadlines (licenses, insurance, subscriptions)
- Scattered personal information across documents
- Inefficient task prioritization
- Time wasted on repetitive admin tasks

## 💡 Solution

An intelligent **Life Admin Concierge Agent** powered by Google ADK that:
1. **Tracks & Reminds** - Monitors renewal dates and sends proactive reminders
2. **Automates Tasks** - Drafts emails, creates calendar events
3. **Prioritizes Smartly** - Uses Eisenhower Matrix based on your energy level
4. **Stores Profile Data** - Instant access to personal info (license #, insurance, etc.)

## 🏗️ Architecture (ADK Multi-Agent System)

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│            ROOT AGENT (life_admin_concierge)                │
│    Model: gemini-2.0-flash | LLM-based delegation           │
│    Delegates to sub_agents based on query intent            │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────────────┐   ┌───────────────────────┐
│    ADMIN AGENT        │   │  PRODUCTIVITY AGENT   │
│   (admin_agent)       │   │ (productivity_agent)  │
│                       │   │                       │
│ Tools:                │   │ Tools:                │
│ • get_profile_info    │   │ • prioritize_tasks_   │
│ • get_renewal_        │   │   eisenhower          │
│   deadlines           │   │ • get_current_        │
│ • create_calendar_    │   │   datetime            │
│   event               │   │ • create_calendar_    │
│ • create_gmail_draft  │   │   event               │
│ • get_current_        │   │                       │
│   datetime            │   │                       │
└───────────────────────┘   └───────────────────────┘
        │                           │
        └───────────┬───────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT INJECTION LAYER                         │
│  USER_PROFILE + RENEWAL_REMINDERS (In-Memory)               │
│  Injected directly into agent instructions                  │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Kaggle Capstone Criteria (6/9 Concepts)

| # | Concept | Implementation |
|---|---------|---------------|
| 1 | **Multi-agent systems** | Root agent + 2 sub-agents with LLM delegation |
| 2 | **Tools** | 6 tools: profile, renewals, calendar, email, prioritize, datetime |
| 3 | **Sessions & Memory** | InMemorySessionService for conversation state |
| 4 | **Context Engineering** | USER_PROFILE + RENEWAL_REMINDERS injection |
| 5 | **Observability** | Python logging in all tool calls |
| 6 | **Agent Evaluation** | pytest suite with 20+ test cases |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google API Key (from [AI Studio](https://aistudio.google.com/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/life-admin-concierge.git
cd life-admin-concierge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
```

### Configuration

1. Get your Google API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Copy `.env.example` to `.env`
3. Add your `GOOGLE_API_KEY` to `.env`

### Running the Agent (ADK)

```bash
# Start ADK Web UI (recommended for demo)
adk web life_admin_agent

# Or run in terminal
adk run life_admin_agent

# Run evaluation tests
pytest evaluation/test_agent_adk.py -v
```
# Interactive mode
python main.py

# Run evaluation tests
python -m pytest evaluation/test_agent.py -v
```

## 📁 Project Structure (ADK Layout)

```
life-admin-concierge/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── PROJECT_PLAN.md          # Sprint plan
│
├── life_admin_agent/        # ⭐ ADK Agent Package
│   ├── __init__.py          # Exports root_agent
│   └── agent.py             # Main agent definition
│                            #   - root_agent (coordinator)
│                            #   - admin_agent (life admin)
│                            #   - productivity_agent (Eisenhower)
│                            #   - All tools defined here
│
├── evaluation/              # Agent Evaluation
│   └── test_agent_adk.py    # pytest test suite
│
├── agents/                  # (Legacy - non-ADK)
├── tools/                   # (Legacy - non-ADK)
├── data/                    # (Legacy - non-ADK)
└── session/                 # (Legacy - non-ADK)
```

## 💬 Example Queries

Try these with `adk web life_admin_agent`:

```
# Profile lookups
"What's my driver's license number?"
"What's my auto insurance policy number?"

# Renewal tracking
"What renewals do I have coming up?"
"Is any of my insurance expiring soon?"

# Task creation
"Schedule a DMV appointment for next Tuesday at 2pm"
"Draft an email to Geico about renewing my auto insurance"

# Productivity
"Help me prioritize these tasks: [list tasks]"
"I'm feeling low energy today, what should I work on?"
```

## 🎬 Demo

[Link to YouTube demo video - Under 3 minutes]

## 👥 Team

- Member A - Core Logic & Evaluation
- Member B - Google API Integration  
- Member C - Orchestration & Submission

## 📄 License

CC-BY-SA 4.0

## 🙏 Acknowledgments

- Google AI & Kaggle for the Agents Intensive course
- Google ADK team for the Agent Development Kit
- Gemini API for powering our agent
