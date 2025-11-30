# Life Admin Concierge Agent 🛎️

> Kaggle Agents Intensive Capstone Project - Concierge Track

A multi-agent system that automates personal life administration tasks, provides smart task prioritization, and serves as your personal data vault.

## 🎯 Problem Statement

Managing personal life admin is tedious:
- Forgetting renewal deadlines (licenses, insurance, subscriptions)
- Scattered personal information across documents
- Inefficient task prioritization
- Time wasted on repetitive admin tasks

## 💡 Solution

An intelligent **Life Admin Concierge Agent** that:
1. **Tracks & Reminds** - Monitors renewal dates and sends proactive reminders
2. **Automates Tasks** - Drafts emails, creates calendar events
3. **Prioritizes Smartly** - Uses Eisenhower Matrix based on your energy level
4. **Stores Profile Data** - Instant access to personal info (license #, insurance, etc.)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  ROUTER AGENT                                │
│  (Classifies query → routes to appropriate sub-agent)       │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  ADMIN AGENT  │ │ PRODUCTIVITY  │ │ PROFILE AGENT │
│               │ │    AGENT      │ │               │
│ • Calendar    │ │ • Eisenhower  │ │ • License #   │
│ • Email Draft │ │ • Scheduling  │ │ • Insurance   │
│ • Reminders   │ │ • Time-block  │ │ • Personal    │
└───────────────┘ └───────────────┘ └───────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT INJECTION LAYER                         │
│  USER_PROFILE + RENEWAL_REMINDERS (In-Memory)               │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Features Implemented

| Feature | Implementation |
|---------|---------------|
| Multi-agent system | Router + Admin + Productivity + Profile agents |
| Tools | Google Calendar, Gmail Draft, Custom tools |
| Sessions & Memory | InMemorySession for conversation history |
| Context Engineering | USER_PROFILE injection (no vector DB needed) |
| Observability | Logging in all tool calls |
| Agent Evaluation | Test suite with 5+ test cases |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud account (for Calendar/Gmail APIs)
- Gemini API key

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
# Edit .env with your API keys
```

### Configuration

1. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. (Optional) Set up Google Cloud credentials for Calendar/Gmail
3. Update `.env` with your credentials

### Running the Agent

```bash
# Interactive mode
python main.py

# Run evaluation tests
python -m pytest evaluation/test_agent.py -v
```

## 📁 Project Structure

```
life-admin-concierge/
├── README.md
├── requirements.txt
├── main.py                   # Entry point
├── config.py                 # Configuration
│
├── agents/
│   ├── router.py            # Query routing
│   ├── admin_agent.py       # Life admin tasks
│   └── productivity_agent.py # Task prioritization
│
├── tools/
│   ├── calendar_tool.py     # Google Calendar
│   ├── gmail_tool.py        # Gmail drafts
│   └── profile_tool.py      # Profile lookup
│
├── data/
│   ├── profile_data.py      # User profile context
│   └── eisenhower.py        # Prioritization logic
│
├── session/
│   └── memory.py            # In-memory sessions
│
└── evaluation/
    └── test_agent.py        # Test cases
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
- Gemini API for powering our agent
