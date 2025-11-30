"""
Data module initialization.
Contains user profile data and Eisenhower Matrix logic.
"""

from .profile_data import (
    USER_PROFILE,
    RENEWAL_REMINDERS,
    TASK_TEMPLATES,
    get_profile_summary,
    get_urgent_items
)

from .eisenhower import (
    EisenhowerMatrix,
    EISENHOWER_PROMPT,
    get_prioritization_prompt,
    parse_priority_response
)

__all__ = [
    'USER_PROFILE',
    'RENEWAL_REMINDERS', 
    'TASK_TEMPLATES',
    'get_profile_summary',
    'get_urgent_items',
    'EisenhowerMatrix',
    'EISENHOWER_PROMPT',
    'get_prioritization_prompt',
    'parse_priority_response'
]
