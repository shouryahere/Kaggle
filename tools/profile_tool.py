"""
Profile Tool - Retrieves user profile information from context.

This tool provides access to the user's personal information stored
in the context injection layer (no external database needed).
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
import re

# Import profile data
from data.profile_data import (
    USER_PROFILE, 
    RENEWAL_REMINDERS,
    TASK_TEMPLATES,
    get_profile_summary,
    get_urgent_items
)

# Set up logging for observability
logger = logging.getLogger("ConciergeAgent.ProfileTool")


def get_profile_info(query: str) -> Dict[str, Any]:
    """
    Retrieves specific information from user profile based on query.
    
    Args:
        query: What information to look up (e.g., "license number", "insurance", "address")
    
    Returns:
        Dictionary with requested information
    
    Example:
        >>> get_profile_info("driver's license number")
        {"found": True, "info": "D99887766", "context": "Expires Dec 15, 2025"}
    """
    logger.info(f"[TOOL CALL] get_profile_info")
    logger.info(f"  Query: {query}")
    print(f"🔍 [Profile Tool] Looking up: {query}")
    
    query_lower = query.lower()
    
    # Search patterns for common queries
    search_patterns = {
        "license": {
            "pattern": r"License Number:\s*([A-Z0-9]+)",
            "context_pattern": r"DRIVER'S LICENSE:[\s\S]*?(?=\n\n|\Z)",
            "description": "Driver's License"
        },
        "passport": {
            "pattern": r"Passport Number:\s*([A-Z0-9]+)",
            "context_pattern": r"PASSPORT:[\s\S]*?(?=\n\n|\Z)",
            "description": "Passport"
        },
        "insurance": {
            "pattern": r"Policy Number:\s*([0-9-]+)",
            "context_pattern": r"AUTO INSURANCE:[\s\S]*?(?=\n\n|\Z)",
            "description": "Auto Insurance"
        },
        "address": {
            "pattern": r"ADDRESS:\s*\n\s*(.+)\n\s*(.+)",
            "context_pattern": r"ADDRESS:[\s\S]*?(?=\n\n[A-Z]|\Z)",
            "description": "Home Address"
        },
        "phone": {
            "pattern": r"PHONE:\s*(\+?[\d\s()-]+)",
            "context_pattern": r"PHONE:.*",
            "description": "Phone Number"
        },
        "email": {
            "pattern": r"EMAIL:\s*(\S+@\S+)",
            "context_pattern": r"EMAIL:.*",
            "description": "Email Address"
        },
        "emergency": {
            "pattern": r"EMERGENCY CONTACT:[\s\S]*?Phone:\s*(\+?[\d\s()-]+)",
            "context_pattern": r"EMERGENCY CONTACT:[\s\S]*?(?=\n\n|\Z)",
            "description": "Emergency Contact"
        }
    }
    
    # Find matching pattern
    result = {
        "found": False,
        "query": query,
        "info": None,
        "context": None
    }
    
    for key, config in search_patterns.items():
        if key in query_lower:
            # Try to extract specific info
            match = re.search(config["pattern"], USER_PROFILE)
            if match:
                result["found"] = True
                result["info"] = match.group(1) if match.lastindex else match.group(0)
                result["type"] = config["description"]
            
            # Get broader context
            context_match = re.search(config["context_pattern"], USER_PROFILE)
            if context_match:
                result["context"] = context_match.group(0).strip()
            
            break
    
    # If no specific pattern matched, return general search
    if not result["found"]:
        # Search for query terms in profile
        lines = USER_PROFILE.split('\n')
        matching_lines = [
            line.strip() for line in lines 
            if any(term in line.lower() for term in query_lower.split())
        ]
        
        if matching_lines:
            result["found"] = True
            result["info"] = "\n".join(matching_lines[:5])
            result["type"] = "General Search"
    
    logger.info(f"  Result: Found={result['found']}")
    print(f"  {'✅' if result['found'] else '❌'} {'Found' if result['found'] else 'Not found'}")
    
    return result


def get_renewal_status() -> Dict[str, Any]:
    """
    Gets the current status of all renewals and upcoming deadlines.
    
    Returns:
        Dictionary with categorized renewal information
    """
    logger.info("[TOOL CALL] get_renewal_status")
    print("🔍 [Profile Tool] Checking renewal status...")
    
    urgent = get_urgent_items()
    
    result = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "urgent_items": urgent,
        "full_renewal_list": RENEWAL_REMINDERS,
        "action_required": len([i for i in urgent if i["priority"] in ["CRITICAL", "HIGH"]])
    }
    
    logger.info(f"  Found {len(urgent)} urgent items")
    print(f"  ⚠️ {result['action_required']} items need attention")
    
    return result


def get_task_template(task_type: str) -> Dict[str, Any]:
    """
    Gets a checklist template for common life admin tasks.
    
    Args:
        task_type: Type of task (e.g., "license_renewal", "travel_prep")
    
    Returns:
        Dictionary with task template and steps
    """
    logger.info(f"[TOOL CALL] get_task_template: {task_type}")
    print(f"📋 [Profile Tool] Getting template for: {task_type}")
    
    template = TASK_TEMPLATES.get(task_type)
    
    if template:
        return {
            "success": True,
            "task_type": task_type,
            "template": template
        }
    else:
        # Return available templates if not found
        return {
            "success": False,
            "error": f"Template '{task_type}' not found",
            "available_templates": list(TASK_TEMPLATES.keys())
        }


def get_full_profile() -> str:
    """
    Returns the complete user profile for context injection.
    
    Returns:
        Full profile string
    """
    logger.info("[TOOL CALL] get_full_profile")
    return USER_PROFILE + "\n\n" + RENEWAL_REMINDERS


# Tool metadata for agent registration
PROFILE_TOOL_METADATA = {
    "name": "get_profile_info",
    "description": "Retrieves user's personal information from their profile. Use this when the user asks about their license number, passport, insurance details, address, phone, email, or any other personal information.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "What information to look up (e.g., 'driver's license number', 'insurance policy', 'address')"
            }
        },
        "required": ["query"]
    }
}

RENEWAL_TOOL_METADATA = {
    "name": "get_renewal_status",
    "description": "Gets the status of all upcoming renewals, deadlines, and bills. Use this when the user asks about what's due, upcoming renewals, or deadlines.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
