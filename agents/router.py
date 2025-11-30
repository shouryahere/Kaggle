"""
Router Agent - Routes user queries to appropriate sub-agents.

This is the main orchestrator that classifies incoming queries
and delegates them to specialized agents.
"""

from typing import Dict, Any, Tuple
import logging
import re

logger = logging.getLogger("ConciergeAgent.Router")


class RouterAgent:
    """
    Routes user queries to the appropriate sub-agent based on intent classification.
    
    Sub-agents:
    - admin_agent: Life admin tasks (calendar, email, reminders)
    - productivity_agent: Task prioritization, scheduling, Eisenhower matrix
    - profile_agent: Personal information lookup
    - general_agent: General conversation and fallback
    """
    
    def __init__(self):
        self.routes = {
            "admin_agent": {
                "keywords": [
                    "calendar", "event", "schedule", "remind", "reminder", 
                    "appointment", "meeting", "book", "email", "draft", 
                    "mail", "send", "renew", "renewal", "deadline"
                ],
                "description": "Handles calendar events, email drafts, and renewal reminders"
            },
            "productivity_agent": {
                "keywords": [
                    "task", "priority", "prioritize", "eisenhower", "matrix",
                    "energy", "todo", "to-do", "schedule", "time block",
                    "productive", "focus", "plan", "daily", "routine"
                ],
                "description": "Handles task prioritization and daily planning"
            },
            "profile_agent": {
                "keywords": [
                    "license", "passport", "insurance", "policy", "number",
                    "address", "phone", "email", "contact", "ssn", "id",
                    "document", "info", "information", "profile", "what's my",
                    "what is my", "do i have"
                ],
                "description": "Retrieves personal information from profile"
            }
        }
    
    def classify_intent(self, query: str) -> Tuple[str, float]:
        """
        Classify the user's query intent.
        
        Args:
            query: User's input query
        
        Returns:
            Tuple of (agent_name, confidence_score)
        """
        query_lower = query.lower()
        scores = {}
        
        for agent, config in self.routes.items():
            # Count keyword matches
            matches = sum(1 for kw in config["keywords"] if kw in query_lower)
            # Weight by keyword specificity (longer keywords = more specific)
            weighted_score = sum(
                len(kw) for kw in config["keywords"] if kw in query_lower
            )
            scores[agent] = weighted_score
        
        # Find best match
        if scores:
            best_agent = max(scores, key=scores.get)
            max_score = scores[best_agent]
            
            # Calculate confidence (normalize by query length)
            confidence = min(max_score / max(len(query_lower), 1) * 10, 1.0)
            
            if max_score > 0:
                return best_agent, confidence
        
        return "general_agent", 0.5
    
    def route(self, query: str) -> Dict[str, Any]:
        """
        Route the query to the appropriate agent.
        
        Args:
            query: User's input query
        
        Returns:
            Dictionary with routing decision and metadata
        """
        logger.info(f"[ROUTER] Processing query: {query[:50]}...")
        print(f"🔀 [Router] Analyzing query...")
        
        agent, confidence = self.classify_intent(query)
        
        routing_result = {
            "query": query,
            "routed_to": agent,
            "confidence": confidence,
            "description": self.routes.get(agent, {}).get("description", "General assistance")
        }
        
        logger.info(f"  Routed to: {agent} (confidence: {confidence:.2f})")
        print(f"  → Routing to: {agent} (confidence: {confidence:.1%})")
        
        return routing_result
    
    def get_available_agents(self) -> Dict[str, str]:
        """Returns list of available agents and their descriptions."""
        return {
            agent: config["description"] 
            for agent, config in self.routes.items()
        }


class AgentMessage:
    """
    A2A Protocol simulation - Message passing between agents.
    
    This provides a structured way for agents to communicate,
    simulating the A2A (Agent-to-Agent) protocol.
    """
    
    def __init__(self, sender: str, receiver: str, content: str, 
                 message_type: str = "request"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type  # request, response, notification
        self.timestamp = self._get_timestamp()
        self.metadata = {}
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "type": self.message_type,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    def __repr__(self):
        return f"AgentMessage({self.sender} → {self.receiver}: {self.content[:30]}...)"


def send_a2a_message(msg: AgentMessage) -> Dict[str, Any]:
    """
    Send a message from one agent to another (A2A Protocol simulation).
    
    Args:
        msg: AgentMessage object
    
    Returns:
        Delivery confirmation
    """
    logger.info(f"[A2A] Message: {msg.sender} → {msg.receiver}")
    print(f"📨 [A2A] Routing message from {msg.sender} to {msg.receiver}...")
    
    return {
        "delivered": True,
        "message_id": f"msg_{msg.timestamp.replace(':', '').replace('-', '')}",
        "sender": msg.sender,
        "receiver": msg.receiver,
        "timestamp": msg.timestamp
    }


# Singleton router instance
_router_instance = None

def get_router() -> RouterAgent:
    """Get or create the router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = RouterAgent()
    return _router_instance
