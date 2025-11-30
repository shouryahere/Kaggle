"""
Agents module initialization.
"""

from .router import RouterAgent, AgentMessage, send_a2a_message, get_router
from .admin_agent import AdminAgent
from .productivity_agent import ProductivityAgent

__all__ = [
    'RouterAgent',
    'AgentMessage', 
    'send_a2a_message',
    'get_router',
    'AdminAgent',
    'ProductivityAgent'
]
