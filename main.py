"""
Life Admin Concierge Agent - Main Entry Point

A multi-agent system for personal life administration.
Powered by Google Gemini.

Features:
- Multi-agent system (Router + Admin + Productivity agents)
- Tools (Google Calendar, Gmail Draft, Profile Lookup)
- Sessions & Memory (In-memory conversation history)
- Context Engineering (Profile data injection)
- Observability (Logging throughout)
- Agent Evaluation (Test suite included)
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging (OBSERVABILITY)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ConciergeAgent")

# Import configuration
from config import GEMINI_API_KEY, DEFAULT_MODEL, ENABLE_OBSERVABILITY

# Import data and context
from data.profile_data import USER_PROFILE, RENEWAL_REMINDERS, get_profile_summary
from data.eisenhower import get_prioritization_prompt

# Import agents
from agents.router import RouterAgent, AgentMessage, send_a2a_message
from agents.admin_agent import AdminAgent
from agents.productivity_agent import ProductivityAgent

# Import tools
from tools.calendar_tool import create_calendar_event
from tools.gmail_tool import create_gmail_draft
from tools.profile_tool import get_profile_info, get_renewal_status

# Import session management
from session.memory import InMemorySession, get_session_manager


class LifeAdminConcierge:
    """
    Main orchestrator for the Life Admin Concierge Agent.
    
    This class coordinates the multi-agent system, manages sessions,
    and provides the main interface for user interactions.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Life Admin Concierge.
        
        Args:
            api_key: Gemini API key (uses env var if not provided)
        """
        self.api_key = api_key or GEMINI_API_KEY
        
        # Initialize sub-agents
        self.router = RouterAgent()
        self.admin_agent = AdminAgent()
        self.productivity_agent = ProductivityAgent()
        
        # Initialize session manager
        self.session_manager = get_session_manager()
        
        # System context (CONTEXT ENGINEERING)
        self.system_context = self._build_system_context()
        
        # Initialize Gemini client if API key available
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("✅ Gemini client initialized")
            except ImportError:
                logger.warning("google-genai not installed, running in demo mode")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini: {e}")
        
        logger.info("🛎️ Life Admin Concierge initialized")
    
    def _build_system_context(self) -> str:
        """Build the system context with user profile injection."""
        return f"""
You are a Life Admin Concierge Agent - a helpful assistant for managing personal life administration.

=== USER PROFILE (Context Injection) ===
{USER_PROFILE}

=== RENEWAL CALENDAR ===
{RENEWAL_REMINDERS}

=== YOUR CAPABILITIES ===
1. **Profile Lookup**: Answer questions about user's personal information (license #, insurance, etc.)
2. **Calendar Events**: Create reminders and calendar events for deadlines
3. **Email Drafts**: Draft emails for renewals, appointments, and communications
4. **Task Prioritization**: Use Eisenhower Matrix to prioritize tasks based on urgency/importance
5. **Energy-Based Scheduling**: Recommend tasks appropriate for user's current energy level

=== GUIDELINES ===
- Be proactive about upcoming deadlines (check RENEWAL CALENDAR)
- When user asks about personal info, retrieve from USER PROFILE
- For task prioritization, consider both urgency and user's energy level
- Always confirm before taking actions (creating events, drafting emails)
- Be concise but thorough in your responses
"""
    
    def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a user query through the multi-agent system.
        
        Args:
            query: User's input query
            session_id: Optional session ID for conversation continuity
        
        Returns:
            Response dictionary with results and metadata
        """
        # Get or create session (SESSIONS & MEMORY)
        session = self.session_manager.get_or_create_session(session_id)
        session.add_user_message(query)
        
        logger.info(f"📥 Processing query: {query[:50]}...")
        print(f"\n{'='*60}")
        print(f"📥 User: {query}")
        print(f"{'='*60}")
        
        # Route query to appropriate agent (MULTI-AGENT SYSTEM)
        routing = self.router.route(query)
        target_agent = routing["routed_to"]
        
        # Create A2A message for inter-agent communication
        a2a_msg = AgentMessage(
            sender="router",
            receiver=target_agent,
            content=query
        )
        send_a2a_message(a2a_msg)
        
        # Process with appropriate agent
        if target_agent == "admin_agent":
            result = self.admin_agent.process(query, {"session": session})
        elif target_agent == "productivity_agent":
            result = self.productivity_agent.process(query, {"session": session})
        elif target_agent == "profile_agent":
            result = get_profile_info(query)
        else:
            result = self._handle_general_query(query, session)
        
        # If we have Gemini client, enhance response with LLM
        if self.client and result:
            result = self._enhance_with_llm(query, result, session)
        
        # Add response to session history
        response_text = result.get("response", str(result))
        session.add_assistant_message(response_text)
        
        # Track agent invocation
        if target_agent not in session.metadata["agents_invoked"]:
            session.metadata["agents_invoked"].append(target_agent)
        
        # Log result (OBSERVABILITY)
        logger.info(f"📤 Response generated by {target_agent}")
        
        return {
            "query": query,
            "response": result,
            "routing": routing,
            "session_id": session.session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_general_query(self, query: str, session: InMemorySession) -> Dict[str, Any]:
        """Handle general queries not routed to specific agents."""
        return {
            "agent": "general",
            "message": "I'm your Life Admin Concierge. I can help you with:",
            "capabilities": [
                "📋 Looking up your personal information (license, insurance, etc.)",
                "📅 Creating calendar events and reminders",
                "📧 Drafting emails for renewals and communications",
                "✅ Prioritizing tasks using the Eisenhower Matrix",
                "⚡ Suggesting tasks based on your energy level"
            ],
            "quick_actions": [
                "What renewals do I have coming up?",
                "What's my driver's license number?",
                "I'm tired, what should I work on?",
                "Help me prioritize my tasks"
            ]
        }
    
    def _enhance_with_llm(self, query: str, agent_result: Dict, 
                          session: InMemorySession) -> Dict[str, Any]:
        """
        Enhance agent response with LLM for natural language output.
        
        Args:
            query: Original user query
            agent_result: Result from sub-agent
            session: Current session
        
        Returns:
            Enhanced response dictionary
        """
        try:
            # Build prompt with context and agent result
            prompt = f"""
{self.system_context}

=== CURRENT CONVERSATION ===
User Query: {query}

=== AGENT RESULT ===
{agent_result}

=== INSTRUCTIONS ===
Based on the user's query and the agent result above, provide a helpful, 
natural language response. If there are action items or recommendations, 
list them clearly. Be concise but thorough.
"""
            
            # Generate response using Gemini
            response = self.client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=prompt
            )
            
            agent_result["response"] = response.text
            agent_result["llm_enhanced"] = True
            
        except Exception as e:
            logger.error(f"LLM enhancement failed: {e}")
            agent_result["response"] = str(agent_result)
            agent_result["llm_enhanced"] = False
        
        return agent_result
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool directly.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
        
        Returns:
            Tool execution result
        """
        tools = {
            "create_calendar_event": create_calendar_event,
            "create_gmail_draft": create_gmail_draft,
            "get_profile_info": get_profile_info,
            "get_renewal_status": get_renewal_status
        }
        
        if tool_name not in tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        logger.info(f"🔧 Executing tool: {tool_name}")
        return tools[tool_name](**kwargs)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics."""
        return {
            "status": "operational",
            "gemini_connected": self.client is not None,
            "model": DEFAULT_MODEL,
            "sessions": self.session_manager.get_stats(),
            "agents": {
                "router": "active",
                "admin_agent": "active",
                "productivity_agent": "active"
            },
            "observability": ENABLE_OBSERVABILITY
        }


def interactive_mode():
    """Run the agent in interactive mode."""
    print("\n" + "="*60)
    print("🛎️  LIFE ADMIN CONCIERGE AGENT")
    print("="*60)
    print("Your personal assistant for life administration tasks.")
    print("Type 'quit' to exit, 'status' for system info.\n")
    
    # Check for API key
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. Running in demo mode.")
        print("   Set your API key in .env file for full functionality.\n")
    
    # Initialize concierge
    concierge = LifeAdminConcierge()
    session_id = None
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n👋 Goodbye! Stay organized!")
                break
            
            if user_input.lower() == 'status':
                status = concierge.get_system_status()
                print(f"\n📊 System Status:")
                for key, value in status.items():
                    print(f"   {key}: {value}")
                continue
            
            # Process the query
            result = concierge.process_query(user_input, session_id)
            session_id = result["session_id"]  # Maintain session
            
            # Display response
            print(f"\n🤖 Concierge:")
            response = result["response"]
            if isinstance(response, dict):
                if "response" in response:
                    print(f"   {response['response']}")
                elif "message" in response:
                    print(f"   {response['message']}")
                    if "capabilities" in response:
                        for cap in response.get("capabilities", []):
                            print(f"      {cap}")
                    if "recommendations" in response:
                        for rec in response.get("recommendations", []):
                            print(f"      {rec}")
                else:
                    for key, value in response.items():
                        print(f"   {key}: {value}")
            else:
                print(f"   {response}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\n❌ Error: {e}")


def demo_mode():
    """Run a quick demo of the agent capabilities."""
    print("\n" + "="*60)
    print("🛎️  LIFE ADMIN CONCIERGE - DEMO MODE")
    print("="*60 + "\n")
    
    concierge = LifeAdminConcierge()
    
    demo_queries = [
        "What's my driver's license number?",
        "What renewals do I have coming up?",
        "I'm feeling tired today, what should I work on?",
        "Create a calendar event for my DMV appointment on December 10th at 2pm",
        "Draft an email to renew my car insurance"
    ]
    
    for query in demo_queries:
        print(f"\n{'='*60}")
        result = concierge.process_query(query)
        print(f"\n📤 Result: {result['response']}")
        print(f"{'='*60}")
        input("\nPress Enter for next demo...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        interactive_mode()
