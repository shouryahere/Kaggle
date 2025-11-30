"""
Admin Agent - Handles life administration tasks.

Capabilities:
- Create calendar events for appointments and reminders
- Draft emails for renewals and communications
- Track and alert about upcoming deadlines
"""

from typing import Dict, Any, List
import logging
from datetime import datetime

from tools.calendar_tool import create_calendar_event, list_upcoming_events
from tools.gmail_tool import create_gmail_draft, generate_renewal_email
from tools.profile_tool import get_renewal_status

logger = logging.getLogger("ConciergeAgent.AdminAgent")


class AdminAgent:
    """
    Life Admin Agent - Automates personal administration tasks.
    
    Features:
    - Calendar event creation
    - Email draft generation  
    - Renewal tracking and reminders
    """
    
    def __init__(self):
        self.name = "AdminAgent"
        self.capabilities = [
            "create_calendar_event",
            "create_gmail_draft",
            "check_renewals",
            "set_reminder"
        ]
    
    def process(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process an admin-related query.
        
        Args:
            query: User's request
            context: Additional context (session, profile, etc.)
        
        Returns:
            Response with action taken and results
        """
        logger.info(f"[AdminAgent] Processing: {query[:50]}...")
        print(f"🗂️ [Admin Agent] Handling request...")
        
        query_lower = query.lower()
        
        # Determine action based on query
        if any(kw in query_lower for kw in ["calendar", "event", "appointment", "schedule"]):
            return self._handle_calendar_request(query, context)
        elif any(kw in query_lower for kw in ["email", "draft", "mail", "write"]):
            return self._handle_email_request(query, context)
        elif any(kw in query_lower for kw in ["renewal", "renew", "expir", "deadline", "due"]):
            return self._handle_renewal_request(query, context)
        else:
            return self._handle_general_admin(query, context)
    
    def _handle_calendar_request(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle calendar-related requests."""
        logger.info("  Action: Calendar request")
        
        # For demo, create a sample event
        # In production, this would parse the query to extract event details
        return {
            "agent": self.name,
            "action": "calendar_suggestion",
            "message": "I can help you create a calendar event. Please provide:",
            "required_info": [
                "Event title",
                "Date and time",
                "Duration (optional)",
                "Description (optional)"
            ],
            "example": "Example: 'Create a calendar event for DMV appointment on Dec 10 at 2pm'",
            "tool_available": "create_calendar_event"
        }
    
    def _handle_email_request(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle email draft requests."""
        logger.info("  Action: Email request")
        
        return {
            "agent": self.name,
            "action": "email_suggestion",
            "message": "I can draft an email for you. Please provide:",
            "required_info": [
                "Recipient email",
                "Subject",
                "Key points to include"
            ],
            "tool_available": "create_gmail_draft"
        }
    
    def _handle_renewal_request(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle renewal and deadline queries."""
        logger.info("  Action: Renewal check")
        
        # Get current renewal status
        status = get_renewal_status()
        
        return {
            "agent": self.name,
            "action": "renewal_status",
            "status": status,
            "message": f"Found {status['action_required']} items requiring attention.",
            "suggested_actions": [
                "Create calendar reminder for upcoming deadlines",
                "Draft renewal emails for urgent items"
            ]
        }
    
    def _handle_general_admin(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle general admin requests."""
        return {
            "agent": self.name,
            "action": "general_help",
            "message": "I can help with life admin tasks.",
            "capabilities": self.capabilities
        }
    
    def create_reminder(self, title: str, date: str, description: str = "") -> Dict[str, Any]:
        """
        Create a calendar reminder for a deadline or task.
        
        Args:
            title: Reminder title
            date: Date/time for reminder
            description: Additional details
        
        Returns:
            Calendar event creation result
        """
        logger.info(f"[AdminAgent] Creating reminder: {title}")
        
        return create_calendar_event(
            title=f"⏰ Reminder: {title}",
            start_time=date,
            duration_hours=0.5,
            description=description
        )
    
    def draft_renewal_email(self, renewal_type: str, provider: str, 
                           policy_number: str, expiration: str) -> Dict[str, Any]:
        """
        Generate and create a draft email for a renewal.
        
        Args:
            renewal_type: Type of renewal
            provider: Service provider
            policy_number: Policy/account number
            expiration: Expiration date
        
        Returns:
            Email draft creation result
        """
        logger.info(f"[AdminAgent] Drafting renewal email for: {renewal_type}")
        
        # Generate email content
        email_content = generate_renewal_email(
            renewal_type=renewal_type,
            provider=provider,
            policy_number=policy_number,
            expiration_date=expiration
        )
        
        if email_content["success"]:
            # Create the draft
            return create_gmail_draft(
                to=email_content["suggested_recipient"],
                subject=email_content["subject"],
                body=email_content["body"]
            )
        
        return email_content
