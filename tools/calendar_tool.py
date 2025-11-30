"""
Google Calendar Tool - Creates calendar events for reminders and deadlines.

MEMBER B: Implement real Google Calendar API integration here.
For demo purposes, a mock implementation is provided.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

# Set up logging for observability
logger = logging.getLogger("ConciergeAgent.CalendarTool")


def create_calendar_event(
    title: str,
    start_time: str,
    duration_hours: float = 1.0,
    description: str = "",
    location: str = "",
    reminder_minutes: int = 30
) -> Dict[str, Any]:
    """
    Creates a Google Calendar event.
    
    Args:
        title: Event title/summary
        start_time: Start time in ISO format (e.g., "2025-12-15T10:00:00")
        duration_hours: Event duration in hours (default: 1 hour)
        description: Event description/notes
        location: Event location
        reminder_minutes: Minutes before event to send reminder
    
    Returns:
        Dictionary with event details or error information
    
    Example:
        >>> create_calendar_event(
        ...     title="DMV Appointment - License Renewal",
        ...     start_time="2025-12-10T14:00:00",
        ...     duration_hours=1,
        ...     description="Bring current license and proof of residency",
        ...     location="DMV San Francisco, 1377 Fell St"
        ... )
    """
    # Log tool invocation (OBSERVABILITY)
    logger.info(f"[TOOL CALL] create_calendar_event")
    logger.info(f"  Title: {title}")
    logger.info(f"  Start: {start_time}")
    logger.info(f"  Duration: {duration_hours} hours")
    
    print(f"📅 [Calendar Tool] Creating event: '{title}' at {start_time}")
    
    try:
        # Parse start time
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = start_dt + timedelta(hours=duration_hours)
        
        # ===========================================
        # MOCK IMPLEMENTATION (for demo)
        # Replace with real Google Calendar API below
        # ===========================================
        
        event_result = {
            "success": True,
            "event_id": f"mock_event_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "description": description,
            "location": location,
            "html_link": f"https://calendar.google.com/calendar/event?eid=mock123",
            "reminder": f"{reminder_minutes} minutes before",
            "status": "confirmed"
        }
        
        logger.info(f"  Result: Event created successfully - {event_result['event_id']}")
        print(f"  ✅ Event created: {event_result['html_link']}")
        
        return event_result
        
        # ===========================================
        # REAL IMPLEMENTATION (uncomment when ready)
        # ===========================================
        """
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        # Load credentials (assumes credentials.json exists)
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('calendar', 'v3', credentials=creds)
        
        event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': reminder_minutes},
                ],
            },
        }
        
        created_event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        return {
            "success": True,
            "event_id": created_event.get('id'),
            "html_link": created_event.get('htmlLink'),
            "title": title,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
        """
        
    except ValueError as e:
        error_msg = f"Invalid date format: {str(e)}"
        logger.error(f"  Error: {error_msg}")
        print(f"  ❌ Error: {error_msg}")
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Failed to create event: {str(e)}"
        logger.error(f"  Error: {error_msg}")
        print(f"  ❌ Error: {error_msg}")
        return {"success": False, "error": error_msg}


def list_upcoming_events(max_results: int = 10) -> Dict[str, Any]:
    """
    Lists upcoming calendar events.
    
    Args:
        max_results: Maximum number of events to return
    
    Returns:
        Dictionary with list of upcoming events
    """
    logger.info(f"[TOOL CALL] list_upcoming_events (max: {max_results})")
    print(f"📅 [Calendar Tool] Listing upcoming events...")
    
    # MOCK IMPLEMENTATION
    mock_events = [
        {
            "id": "event1",
            "title": "Team Meeting",
            "start": "2025-12-01T10:00:00",
            "end": "2025-12-01T11:00:00"
        },
        {
            "id": "event2", 
            "title": "License Renewal Reminder",
            "start": "2025-12-10T09:00:00",
            "end": "2025-12-10T09:30:00"
        }
    ]
    
    return {
        "success": True,
        "count": len(mock_events),
        "events": mock_events
    }


def delete_calendar_event(event_id: str) -> Dict[str, Any]:
    """
    Deletes a calendar event.
    
    Args:
        event_id: The ID of the event to delete
    
    Returns:
        Dictionary with deletion status
    """
    logger.info(f"[TOOL CALL] delete_calendar_event: {event_id}")
    print(f"📅 [Calendar Tool] Deleting event: {event_id}")
    
    # MOCK IMPLEMENTATION
    return {
        "success": True,
        "deleted_event_id": event_id,
        "message": "Event deleted successfully"
    }


# Tool metadata for agent registration
CALENDAR_TOOL_METADATA = {
    "name": "create_calendar_event",
    "description": "Creates a Google Calendar event for reminders, appointments, or deadlines. Use this when the user wants to schedule something or set a reminder.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title/summary of the calendar event"
            },
            "start_time": {
                "type": "string", 
                "description": "Start time in ISO format (e.g., '2025-12-15T10:00:00')"
            },
            "duration_hours": {
                "type": "number",
                "description": "Duration of the event in hours (default: 1)"
            },
            "description": {
                "type": "string",
                "description": "Additional details or notes for the event"
            },
            "location": {
                "type": "string",
                "description": "Location of the event"
            }
        },
        "required": ["title", "start_time"]
    }
}
