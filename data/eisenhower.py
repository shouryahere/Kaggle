"""
Eisenhower Matrix - Task Prioritization Logic

This module implements the Eisenhower Matrix for task prioritization.
Tasks are categorized into four quadrants:
- Q1 (Do First): Urgent AND Important
- Q2 (Schedule): Important but NOT Urgent
- Q3 (Delegate): Urgent but NOT Important
- Q4 (Eliminate): NOT Urgent AND NOT Important

The system also adapts recommendations based on user's energy level.

MEMBER A: Implement the prioritization logic here.
"""

from typing import List, Dict, Any
from datetime import datetime
import json

# Eisenhower Matrix prompt template for LLM
EISENHOWER_PROMPT = """
You are a productivity expert using the Eisenhower Matrix framework.

CONTEXT:
- Current date/time: {current_time}
- User's energy level: {energy_level}
- User's work hours: 9 AM - 5 PM PST

USER'S TASK LIST:
{task_list}

INSTRUCTIONS:
1. Categorize each task into one of four quadrants:
   - Q1 (DO FIRST): Urgent AND Important - Crisis, deadlines, problems
   - Q2 (SCHEDULE): Important NOT Urgent - Planning, development, prevention
   - Q3 (DELEGATE): Urgent NOT Important - Interruptions, some meetings, some calls
   - Q4 (ELIMINATE): NOT Urgent NOT Important - Time wasters, pleasant activities

2. Consider the user's current energy level:
   - If LOW energy: Prioritize Q3/Q4 tasks (easy wins, low cognitive load)
   - If MEDIUM energy: Mix of Q2/Q3 tasks
   - If HIGH energy: Prioritize Q1/Q2 tasks (deep work, complex problems)

3. Create a time-blocked schedule for today based on the prioritization.

OUTPUT FORMAT (JSON):
{{
    "analysis": "Brief analysis of the task list",
    "quadrants": {{
        "Q1_do_first": ["task1", "task2"],
        "Q2_schedule": ["task3", "task4"],
        "Q3_delegate": ["task5"],
        "Q4_eliminate": ["task6"]
    }},
    "energy_adjusted_recommendation": "Based on {energy_level} energy, here's what to focus on...",
    "suggested_schedule": [
        {{"time": "9:00 AM", "task": "task_name", "duration": "30 min", "quadrant": "Q1"}},
        {{"time": "9:30 AM", "task": "task_name", "duration": "1 hour", "quadrant": "Q2"}}
    ],
    "quick_wins": ["Easy tasks to build momentum"],
    "defer_to_tomorrow": ["Tasks that can wait"]
}}
"""


class EisenhowerMatrix:
    """
    Implements the Eisenhower Matrix for task prioritization.
    """
    
    def __init__(self):
        self.quadrants = {
            "Q1_do_first": [],      # Urgent & Important
            "Q2_schedule": [],       # Important, Not Urgent
            "Q3_delegate": [],       # Urgent, Not Important
            "Q4_eliminate": []       # Not Urgent, Not Important
        }
    
    def categorize_task(self, task: str, urgent: bool, important: bool) -> str:
        """
        Categorize a single task into a quadrant.
        
        Args:
            task: Task description
            urgent: Is the task urgent?
            important: Is the task important?
        
        Returns:
            Quadrant identifier (Q1, Q2, Q3, or Q4)
        """
        if urgent and important:
            quadrant = "Q1_do_first"
        elif important and not urgent:
            quadrant = "Q2_schedule"
        elif urgent and not important:
            quadrant = "Q3_delegate"
        else:
            quadrant = "Q4_eliminate"
        
        self.quadrants[quadrant].append(task)
        return quadrant
    
    def get_energy_adjusted_tasks(self, energy_level: str) -> List[str]:
        """
        Get recommended tasks based on current energy level.
        
        Args:
            energy_level: "LOW", "MEDIUM", or "HIGH"
        
        Returns:
            List of recommended tasks for current energy level
        """
        energy_level = energy_level.upper()
        
        if energy_level == "LOW":
            # Easy wins - Q3 and Q4 tasks (or simple Q2 tasks)
            return self.quadrants["Q3_delegate"] + self.quadrants["Q4_eliminate"]
        elif energy_level == "MEDIUM":
            # Mix of Q2 and Q3
            return self.quadrants["Q2_schedule"] + self.quadrants["Q3_delegate"]
        else:  # HIGH
            # Deep work - Q1 and Q2
            return self.quadrants["Q1_do_first"] + self.quadrants["Q2_schedule"]
    
    def create_time_blocks(self, tasks: List[Dict], start_hour: int = 9) -> List[Dict]:
        """
        Create time-blocked schedule from prioritized tasks.
        
        Args:
            tasks: List of task dictionaries with 'name' and 'duration_min'
            start_hour: Starting hour (24-hour format)
        
        Returns:
            List of time-blocked schedule entries
        """
        schedule = []
        current_hour = start_hour
        current_min = 0
        
        for task in tasks:
            time_str = f"{current_hour:02d}:{current_min:02d}"
            schedule.append({
                "time": time_str,
                "task": task.get("name", "Unknown task"),
                "duration": f"{task.get('duration_min', 30)} min"
            })
            
            # Advance time
            current_min += task.get("duration_min", 30)
            if current_min >= 60:
                current_hour += current_min // 60
                current_min = current_min % 60
        
        return schedule
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all quadrants."""
        return {
            "total_tasks": sum(len(q) for q in self.quadrants.values()),
            "quadrants": self.quadrants,
            "focus_areas": {
                "critical": len(self.quadrants["Q1_do_first"]),
                "important": len(self.quadrants["Q2_schedule"]),
                "delegatable": len(self.quadrants["Q3_delegate"]),
                "eliminatable": len(self.quadrants["Q4_eliminate"])
            }
        }


def get_prioritization_prompt(task_list: str, energy_level: str = "MEDIUM") -> str:
    """
    Generate a prioritization prompt for the LLM.
    
    Args:
        task_list: Raw task list from user
        energy_level: Current energy level (LOW/MEDIUM/HIGH)
    
    Returns:
        Formatted prompt string
    """
    return EISENHOWER_PROMPT.format(
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M %Z"),
        energy_level=energy_level,
        task_list=task_list
    )


def parse_priority_response(response: str) -> Dict[str, Any]:
    """
    Parse LLM response into structured priority data.
    
    Args:
        response: JSON string from LLM
    
    Returns:
        Parsed dictionary with prioritization data
    """
    try:
        # Try to extract JSON from response
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # Return default structure if parsing fails
    return {
        "error": "Could not parse response",
        "raw_response": response
    }


# Example usage
if __name__ == "__main__":
    matrix = EisenhowerMatrix()
    
    # Example tasks
    tasks = [
        ("Renew car insurance (overdue!)", True, True),
        ("Plan Q1 goals", False, True),
        ("Reply to non-urgent emails", True, False),
        ("Browse social media", False, False),
    ]
    
    for task, urgent, important in tasks:
        q = matrix.categorize_task(task, urgent, important)
        print(f"'{task}' → {q}")
    
    print("\nSummary:", matrix.get_summary())
    print("\nFor LOW energy:", matrix.get_energy_adjusted_tasks("LOW"))
