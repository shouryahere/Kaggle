"""
Life Admin Agent - ADK-based multi-agent system for the Concierge Agents track.

This package implements a Google ADK-powered personal assistant that handles:
- Life admin tasks (renewals, appointments, document lookup)
- Personal productivity (Eisenhower matrix, energy-based scheduling)
"""

from .agent import root_agent

__all__ = ["root_agent"]
