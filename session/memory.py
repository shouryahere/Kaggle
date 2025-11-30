"""
In-Memory Session Management for Life Admin Concierge Agent.

Provides conversation history and state management without
external databases (satisfies "Sessions & Memory" requirement).
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
import uuid

logger = logging.getLogger("ConciergeAgent.Session")


class InMemorySession:
    """
    In-memory session for conversation history and state.
    
    Features:
    - Conversation history tracking
    - Session state management
    - Context window management
    - Session expiration
    """
    
    def __init__(self, session_id: str = None, timeout_minutes: int = 30):
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.timeout_minutes = timeout_minutes
        self.history: List[Dict[str, Any]] = []
        self.state: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {
            "message_count": 0,
            "tools_used": [],
            "agents_invoked": []
        }
    
    def add_message(self, role: str, content: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        Add a message to the conversation history.
        
        Args:
            role: Message role ('user', 'assistant', 'system', 'tool')
            content: Message content
            metadata: Additional metadata (tool calls, etc.)
        
        Returns:
            The added message object
        """
        message = {
            "id": len(self.history) + 1,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.history.append(message)
        self.last_activity = datetime.now()
        self.metadata["message_count"] += 1
        
        logger.info(f"[Session {self.session_id[:8]}] Added {role} message")
        
        return message
    
    def add_user_message(self, content: str) -> Dict[str, Any]:
        """Add a user message."""
        return self.add_message("user", content)
    
    def add_assistant_message(self, content: str, tool_calls: List = None) -> Dict[str, Any]:
        """Add an assistant message."""
        return self.add_message("assistant", content, {"tool_calls": tool_calls})
    
    def add_tool_result(self, tool_name: str, result: Any) -> Dict[str, Any]:
        """Add a tool execution result."""
        if tool_name not in self.metadata["tools_used"]:
            self.metadata["tools_used"].append(tool_name)
        return self.add_message("tool", str(result), {"tool_name": tool_name})
    
    def get_history(self, last_n: int = None) -> List[Dict[str, Any]]:
        """
        Get conversation history.
        
        Args:
            last_n: Return only the last N messages (optional)
        
        Returns:
            List of message dictionaries
        """
        if last_n:
            return self.history[-last_n:]
        return self.history
    
    def get_context_window(self, max_tokens: int = 4000) -> List[Dict[str, Any]]:
        """
        Get messages that fit within a token budget.
        
        Args:
            max_tokens: Maximum tokens to include
        
        Returns:
            List of recent messages within token limit
        """
        # Rough estimation: ~4 chars per token
        char_limit = max_tokens * 4
        
        context = []
        total_chars = 0
        
        for msg in reversed(self.history):
            msg_chars = len(msg["content"])
            if total_chars + msg_chars > char_limit:
                break
            context.insert(0, msg)
            total_chars += msg_chars
        
        return context
    
    def set_state(self, key: str, value: Any):
        """Set a session state value."""
        self.state[key] = value
        self.last_activity = datetime.now()
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a session state value."""
        return self.state.get(key, default)
    
    def update_state(self, updates: Dict[str, Any]):
        """Update multiple state values."""
        self.state.update(updates)
        self.last_activity = datetime.now()
    
    def clear_history(self):
        """Clear conversation history but keep session."""
        self.history = []
        self.metadata["message_count"] = 0
        logger.info(f"[Session {self.session_id[:8]}] History cleared")
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        expiry = self.last_activity + timedelta(minutes=self.timeout_minutes)
        return datetime.now() > expiry
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary for logging/debugging."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "message_count": self.metadata["message_count"],
            "tools_used": self.metadata["tools_used"],
            "is_expired": self.is_expired(),
            "history_length": len(self.history)
        }
    
    def to_langchain_format(self) -> List[tuple]:
        """
        Convert history to LangChain message format.
        
        Returns:
            List of (role, content) tuples
        """
        return [(msg["role"], msg["content"]) for msg in self.history]


class SessionManager:
    """
    Manages multiple user sessions.
    
    Provides session creation, retrieval, and cleanup.
    """
    
    def __init__(self, default_timeout: int = 30):
        self.sessions: Dict[str, InMemorySession] = {}
        self.default_timeout = default_timeout
    
    def create_session(self, session_id: str = None) -> InMemorySession:
        """Create a new session."""
        session = InMemorySession(
            session_id=session_id,
            timeout_minutes=self.default_timeout
        )
        self.sessions[session.session_id] = session
        logger.info(f"[SessionManager] Created session: {session.session_id[:8]}")
        return session
    
    def get_session(self, session_id: str) -> Optional[InMemorySession]:
        """Get an existing session."""
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            return session
        elif session and session.is_expired():
            logger.info(f"[SessionManager] Session expired: {session_id[:8]}")
            self.delete_session(session_id)
        return None
    
    def get_or_create_session(self, session_id: str = None) -> InMemorySession:
        """Get existing session or create new one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        return self.create_session(session_id)
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"[SessionManager] Deleted session: {session_id[:8]}")
    
    def cleanup_expired(self) -> int:
        """Remove all expired sessions."""
        expired = [
            sid for sid, session in self.sessions.items() 
            if session.is_expired()
        ]
        for sid in expired:
            self.delete_session(sid)
        return len(expired)
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs."""
        return [
            sid for sid, session in self.sessions.items()
            if not session.is_expired()
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get session manager statistics."""
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(self.get_active_sessions()),
            "default_timeout": self.default_timeout
        }


# Global session manager instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get or create the global session manager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
