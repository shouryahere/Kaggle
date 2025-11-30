"""
Life Admin Concierge Agent - Google ADK Multi-Agent System with Real APIs

This agent uses Google's Agent Development Kit (ADK) with REAL Google API integrations:
- Google Calendar (create/list events)
- Gmail (create drafts, send emails)
- Google Tasks (create/list/complete tasks)
- Google Photos (search photos, list albums)

SETUP: Run `python setup_google_auth.py` first to authenticate!

Key Concepts Demonstrated:
1. Multi-agent systems (coordinator + specialized sub-agents)
2. Tools (real Google API integrations)
3. Sessions/Memory (InMemorySessionService)
4. Observability (logging)
"""

from google.adk.agents import Agent
import logging

# Import real Google API tools
from .google_tools import (
    # Calendar
    create_calendar_event,
    list_calendar_events,
    # Gmail
    create_gmail_draft,
    send_email,
    # Tasks
    list_task_lists,
    list_tasks,
    create_task,
    complete_task,
    # Photos
    search_google_photos,
    list_photo_albums,
    get_photos_from_album,
    # Utility
    get_current_datetime,
)

# Configure logging for observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LifeAdminAgent")

# =============================================================================
# SUB-AGENT: Calendar & Email Agent
# =============================================================================

calendar_email_agent = Agent(
    name="calendar_email_agent",
    model="gemini-2.0-flash",
    description="Manages Google Calendar events and Gmail emails/drafts.",
    instruction="""You are a Calendar and Email Assistant that helps manage schedules and communications.

YOUR CAPABILITIES:
1. **Calendar Management**:
   - Create calendar events with title, time, duration, location, and reminders
   - List upcoming events
   - Help schedule appointments and meetings

2. **Email Management**:
   - Create Gmail drafts for user to review before sending
   - Send emails directly when user confirms
   - Help compose professional emails

GUIDELINES:
- When creating calendar events, ask for: title, date/time, duration (default 1 hour), location (optional)
- Format times in ISO format: "2025-12-15T14:00:00" for 2 PM on Dec 15, 2025
- For emails, always create a draft first unless user explicitly says to send
- Be professional but friendly in email drafts
- Confirm details before creating events or sending emails

EXAMPLES:
- "Schedule a meeting tomorrow at 2pm" → Ask for title, then create_calendar_event
- "Draft an email to john@example.com about the project" → create_gmail_draft
- "What's on my calendar this week?" → list_calendar_events""",
    tools=[
        create_calendar_event,
        list_calendar_events,
        create_gmail_draft,
        send_email,
        get_current_datetime,
    ]
)

# =============================================================================
# SUB-AGENT: Tasks Agent
# =============================================================================

tasks_agent = Agent(
    name="tasks_agent",
    model="gemini-2.0-flash",
    description="Manages Google Tasks - create, list, and complete tasks.",
    instruction="""You are a Task Management Assistant that helps organize and track tasks using Google Tasks.

YOUR CAPABILITIES:
1. **View Tasks**:
   - List all task lists
   - List tasks in a specific list
   - Show pending and completed tasks

2. **Create Tasks**:
   - Add new tasks with titles and notes
   - Set due dates for tasks
   - Add tasks to specific lists

3. **Complete Tasks**:
   - Mark tasks as done
   - Track progress on task lists

GUIDELINES:
- Use "@default" for the main task list unless user specifies otherwise
- Due dates should be in format: "2025-12-15"
- When creating tasks, include helpful notes if the user provides context
- Celebrate when tasks are completed! 🎉

EXAMPLES:
- "What are my tasks?" → list_tasks
- "Add a task to renew my license" → create_task with appropriate due date
- "I finished the report" → complete_task""",
    tools=[
        list_task_lists,
        list_tasks,
        create_task,
        complete_task,
        get_current_datetime,
    ]
)

# =============================================================================
# SUB-AGENT: Photos Agent
# =============================================================================

photos_agent = Agent(
    name="photos_agent",
    model="gemini-2.0-flash",
    description="Searches Google Photos for documents, receipts, and other images.",
    instruction="""You are a Photos Assistant that helps find and organize photos in Google Photos.

YOUR CAPABILITIES:
1. **Search Photos**:
   - Find documents like licenses, passports, insurance cards
   - Search for receipts
   - Find photos by content type

2. **Browse Albums**:
   - List all photo albums
   - View photos in specific albums
   - Help organize document photos

GUIDELINES:
- Google Photos API searches by content categories (DOCUMENTS, RECEIPTS)
- Suggest users create an "Important Documents" album for easy access
- When showing photos, include the URL so users can view them
- Note: The API has limited text search - content category search works best

EXAMPLES:
- "Find my driver's license photo" → search_google_photos with query
- "Show my photo albums" → list_photo_albums
- "What documents do I have saved?" → search_google_photos for documents""",
    tools=[
        search_google_photos,
        list_photo_albums,
        get_photos_from_album,
    ]
)

# =============================================================================
# ROOT AGENT: Life Admin Concierge
# =============================================================================

root_agent = Agent(
    name="life_admin_concierge",
    model="gemini-2.0-flash",
    description="Personal Life Admin Concierge - manages calendar, email, tasks, and photos.",
    instruction="""You are a Personal Life Admin Concierge, an AI assistant that helps manage your digital life.

YOUR ROLE:
You coordinate between specialized sub-agents to help with:

1. **Calendar & Email** (calendar_email_agent):
   - Schedule appointments and meetings
   - View upcoming events
   - Draft and send emails

2. **Tasks** (tasks_agent):
   - Create and manage to-do lists
   - Track tasks with due dates
   - Mark tasks as complete

3. **Photos** (photos_agent):
   - Find document photos (license, passport, etc.)
   - Browse photo albums
   - Search for receipts

ROUTING GUIDELINES:
- Calendar events, scheduling, meetings → delegate to calendar_email_agent
- Email drafts, sending emails → delegate to calendar_email_agent
- Task lists, to-dos, reminders → delegate to tasks_agent
- Finding photos, documents, albums → delegate to photos_agent
- General questions → handle yourself

PERSONALITY:
- Be helpful and proactive
- Confirm important actions before executing
- Provide clear summaries of what was done
- Suggest related actions (e.g., after creating a task, offer to add it to calendar)

When starting a conversation, briefly introduce what you can help with.""",
    sub_agents=[calendar_email_agent, tasks_agent, photos_agent]
)

# =============================================================================
# For running locally
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Life Admin Concierge Agent")
    print("=" * 60)
    print("\nThis agent uses REAL Google APIs!")
    print("\nBefore running, make sure you have:")
    print("1. Run: python setup_google_auth.py")
    print("2. Completed Google OAuth authentication")
    print("3. token.json file exists in project root")
    print("\nTo start the agent:")
    print("  adk web .")
    print("\nThen open: http://127.0.0.1:8000")
