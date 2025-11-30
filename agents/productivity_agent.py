"""
Productivity Agent - Handles task prioritization and scheduling.

Capabilities:
- Eisenhower Matrix task categorization
- Energy-based task recommendations
- Daily schedule generation
- Time blocking suggestions
"""

from typing import Dict, Any, List
import logging
from datetime import datetime

from data.eisenhower import (
    EisenhowerMatrix, 
    get_prioritization_prompt,
    parse_priority_response
)

logger = logging.getLogger("ConciergeAgent.ProductivityAgent")


class ProductivityAgent:
    """
    Productivity Agent - Smart task prioritization and scheduling.
    
    Features:
    - Eisenhower Matrix categorization
    - Energy-level aware recommendations
    - Time-blocked daily schedules
    - End-of-day highlights
    """
    
    def __init__(self):
        self.name = "ProductivityAgent"
        self.capabilities = [
            "prioritize_tasks",
            "suggest_schedule", 
            "energy_based_recommendations",
            "create_time_blocks"
        ]
        self.matrix = EisenhowerMatrix()
    
    def process(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a productivity-related query.
        
        Args:
            query: User's request
            context: Additional context (energy level, tasks, etc.)
        
        Returns:
            Response with prioritization and recommendations
        """
        logger.info(f"[ProductivityAgent] Processing: {query[:50]}...")
        print(f"📊 [Productivity Agent] Analyzing request...")
        
        query_lower = query.lower()
        context = context or {}
        
        # Extract energy level from query or context
        energy_level = self._extract_energy_level(query_lower, context)
        
        # Determine action
        if any(kw in query_lower for kw in ["prioritize", "priority", "eisenhower", "important"]):
            return self._handle_prioritization(query, energy_level, context)
        elif any(kw in query_lower for kw in ["schedule", "time block", "plan", "daily"]):
            return self._handle_scheduling(query, energy_level, context)
        elif any(kw in query_lower for kw in ["tired", "low energy", "exhausted", "lazy"]):
            return self._handle_low_energy(query, context)
        elif any(kw in query_lower for kw in ["productive", "focus", "motivated", "energetic"]):
            return self._handle_high_energy(query, context)
        else:
            return self._handle_general_productivity(query, context)
    
    def _extract_energy_level(self, query: str, context: Dict) -> str:
        """Extract energy level from query or context."""
        if any(word in query for word in ["tired", "exhausted", "low", "lazy", "sleepy"]):
            return "LOW"
        elif any(word in query for word in ["energetic", "motivated", "pumped", "high"]):
            return "HIGH"
        elif "energy_level" in context:
            return context["energy_level"]
        else:
            # Check time of day for default
            hour = datetime.now().hour
            if hour < 10:
                return "LOW"  # Morning
            elif hour < 14:
                return "HIGH"  # Mid-day
            else:
                return "MEDIUM"  # Afternoon
    
    def _handle_prioritization(self, query: str, energy_level: str, 
                               context: Dict) -> Dict[str, Any]:
        """Handle task prioritization requests."""
        logger.info(f"  Action: Prioritization (Energy: {energy_level})")
        
        # Get task list from context or request
        task_list = context.get("task_list", "")
        
        if not task_list:
            return {
                "agent": self.name,
                "action": "request_tasks",
                "message": "I'll help you prioritize your tasks using the Eisenhower Matrix.",
                "prompt": "Please share your task list, and I'll categorize them by urgency and importance.",
                "energy_level": energy_level,
                "note": f"Based on your {energy_level} energy, I'll suggest appropriate tasks to focus on."
            }
        
        # Generate prioritization prompt for LLM
        prompt = get_prioritization_prompt(task_list, energy_level)
        
        return {
            "agent": self.name,
            "action": "prioritize",
            "energy_level": energy_level,
            "prioritization_prompt": prompt,
            "message": f"Ready to prioritize tasks for {energy_level} energy level."
        }
    
    def _handle_scheduling(self, query: str, energy_level: str, 
                          context: Dict) -> Dict[str, Any]:
        """Handle scheduling and time-blocking requests."""
        logger.info("  Action: Scheduling")
        
        return {
            "agent": self.name,
            "action": "schedule",
            "energy_level": energy_level,
            "suggested_blocks": self._get_default_time_blocks(energy_level),
            "message": "Here's a suggested time-blocked schedule based on your energy patterns."
        }
    
    def _handle_low_energy(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle requests when user has low energy."""
        logger.info("  Action: Low energy recommendations")
        
        return {
            "agent": self.name,
            "action": "low_energy_mode",
            "energy_level": "LOW",
            "recommendations": [
                "✅ Quick email responses (5-10 min each)",
                "✅ File organization and cleanup",
                "✅ Review and update to-do list",
                "✅ Schedule future appointments",
                "✅ Light reading or research",
                "✅ Take a short walk or stretch break"
            ],
            "avoid": [
                "❌ Complex problem-solving",
                "❌ Important decisions",
                "❌ Deep work requiring focus",
                "❌ Difficult conversations"
            ],
            "message": "When energy is low, focus on easy wins and administrative tasks. "
                      "Save deep work for when you're more energized."
        }
    
    def _handle_high_energy(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle requests when user has high energy."""
        logger.info("  Action: High energy recommendations")
        
        return {
            "agent": self.name,
            "action": "high_energy_mode",
            "energy_level": "HIGH",
            "recommendations": [
                "🚀 Tackle your most important project",
                "🚀 Work on tasks requiring deep focus",
                "🚀 Make important decisions",
                "🚀 Creative work and brainstorming",
                "🚀 Difficult conversations or negotiations",
                "🚀 Learn something new"
            ],
            "time_suggestion": "Block 2-3 hours for uninterrupted deep work",
            "message": "High energy is prime time! Focus on your most important and "
                      "challenging tasks now."
        }
    
    def _handle_general_productivity(self, query: str, context: Dict) -> Dict[str, Any]:
        """Handle general productivity queries."""
        return {
            "agent": self.name,
            "action": "general_help",
            "message": "I can help optimize your productivity.",
            "capabilities": self.capabilities,
            "quick_tips": [
                "Share your task list for Eisenhower Matrix prioritization",
                "Tell me your current energy level for personalized recommendations",
                "Ask for a time-blocked schedule for today"
            ]
        }
    
    def _get_default_time_blocks(self, energy_level: str) -> List[Dict[str, str]]:
        """Get default time blocks based on energy level."""
        if energy_level == "LOW":
            return [
                {"time": "9:00 AM", "activity": "Easy admin tasks", "duration": "1h"},
                {"time": "10:00 AM", "activity": "Email and messages", "duration": "30m"},
                {"time": "10:30 AM", "activity": "Short break", "duration": "15m"},
                {"time": "10:45 AM", "activity": "Light work", "duration": "1h"},
                {"time": "12:00 PM", "activity": "Lunch break", "duration": "1h"},
            ]
        elif energy_level == "HIGH":
            return [
                {"time": "9:00 AM", "activity": "Deep work - Priority task", "duration": "2h"},
                {"time": "11:00 AM", "activity": "Short break", "duration": "15m"},
                {"time": "11:15 AM", "activity": "Important meetings/calls", "duration": "1h"},
                {"time": "12:15 PM", "activity": "Lunch break", "duration": "45m"},
                {"time": "1:00 PM", "activity": "Creative work", "duration": "2h"},
            ]
        else:  # MEDIUM
            return [
                {"time": "9:00 AM", "activity": "Planning and review", "duration": "30m"},
                {"time": "9:30 AM", "activity": "Focused work", "duration": "1.5h"},
                {"time": "11:00 AM", "activity": "Meetings", "duration": "1h"},
                {"time": "12:00 PM", "activity": "Lunch break", "duration": "1h"},
                {"time": "1:00 PM", "activity": "Collaborative work", "duration": "2h"},
            ]
    
    def get_end_of_day_summary(self, completed_tasks: List[str], 
                               pending_tasks: List[str]) -> Dict[str, Any]:
        """
        Generate end-of-day highlights report.
        
        Args:
            completed_tasks: List of completed tasks
            pending_tasks: List of pending tasks
        
        Returns:
            Summary report
        """
        logger.info("[ProductivityAgent] Generating EOD summary")
        
        return {
            "agent": self.name,
            "report_type": "end_of_day_summary",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "completed": {
                "count": len(completed_tasks),
                "tasks": completed_tasks
            },
            "pending": {
                "count": len(pending_tasks),
                "tasks": pending_tasks,
                "carry_over": "These will be prioritized for tomorrow"
            },
            "productivity_score": min(100, len(completed_tasks) * 20),
            "message": f"Great work today! You completed {len(completed_tasks)} tasks. "
                      f"{len(pending_tasks)} tasks will carry over to tomorrow."
        }
