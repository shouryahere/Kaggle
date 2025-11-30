"""
Tools module initialization.
Contains all tools available to the agent.
"""

from .calendar_tool import (
    create_calendar_event,
    list_upcoming_events,
    delete_calendar_event,
    CALENDAR_TOOL_METADATA
)

from .gmail_tool import (
    create_gmail_draft,
    generate_renewal_email,
    list_drafts,
    GMAIL_TOOL_METADATA
)

from .profile_tool import (
    get_profile_info,
    get_renewal_status,
    get_task_template,
    get_full_profile,
    PROFILE_TOOL_METADATA,
    RENEWAL_TOOL_METADATA
)

__all__ = [
    # Calendar tools
    'create_calendar_event',
    'list_upcoming_events',
    'delete_calendar_event',
    'CALENDAR_TOOL_METADATA',
    
    # Gmail tools
    'create_gmail_draft',
    'generate_renewal_email',
    'list_drafts',
    'GMAIL_TOOL_METADATA',
    
    # Profile tools
    'get_profile_info',
    'get_renewal_status',
    'get_task_template',
    'get_full_profile',
    'PROFILE_TOOL_METADATA',
    'RENEWAL_TOOL_METADATA'
]
