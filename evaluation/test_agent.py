"""
Agent Evaluation - Test Suite for Life Admin Concierge Agent

This module provides automated testing to verify agent functionality
across all key features. Satisfies the "Agent Evaluation" requirement.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import LifeAdminConcierge
from agents.router import RouterAgent
from tools.profile_tool import get_profile_info, get_renewal_status
from tools.calendar_tool import create_calendar_event
from tools.gmail_tool import create_gmail_draft
from session.memory import InMemorySession, SessionManager


class AgentEvaluator:
    """
    Evaluates the Life Admin Concierge Agent across multiple test cases.
    """
    
    def __init__(self):
        self.concierge = LifeAdminConcierge()
        self.results: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, name: str, query: str, expected_contains: List[str],
                 expected_agent: str = None) -> bool:
        """
        Run a single test case.
        
        Args:
            name: Test name
            query: Query to test
            expected_contains: Strings that should appear in response
            expected_agent: Expected agent to handle the query
        
        Returns:
            True if test passed, False otherwise
        """
        print(f"\n{'='*50}")
        print(f"🧪 TEST: {name}")
        print(f"   Query: {query}")
        
        try:
            result = self.concierge.process_query(query)
            response_str = str(result.get("response", ""))
            routing = result.get("routing", {})
            actual_agent = routing.get("routed_to", "unknown")
            
            # Check expected content
            content_pass = all(
                exp.lower() in response_str.lower() 
                for exp in expected_contains
            )
            
            # Check expected agent (if specified)
            agent_pass = (expected_agent is None or 
                         actual_agent == expected_agent)
            
            passed = content_pass and agent_pass
            
            test_result = {
                "name": name,
                "query": query,
                "passed": passed,
                "expected_contains": expected_contains,
                "actual_agent": actual_agent,
                "expected_agent": expected_agent,
                "content_match": content_pass,
                "agent_match": agent_pass,
                "response_preview": response_str[:200]
            }
            
            self.results.append(test_result)
            
            if passed:
                self.passed += 1
                print(f"   ✅ PASSED")
            else:
                self.failed += 1
                print(f"   ❌ FAILED")
                if not content_pass:
                    print(f"      Missing expected content: {expected_contains}")
                if not agent_pass:
                    print(f"      Wrong agent: expected {expected_agent}, got {actual_agent}")
            
            return passed
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            self.failed += 1
            self.results.append({
                "name": name,
                "query": query,
                "passed": False,
                "error": str(e)
            })
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """Get evaluation summary."""
        total = self.passed + self.failed
        return {
            "total_tests": total,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": f"{(self.passed/total)*100:.1f}%" if total > 0 else "N/A",
            "timestamp": datetime.now().isoformat()
        }


def test_profile_lookup():
    """Test profile information retrieval."""
    print("\n" + "="*60)
    print("📋 TESTING: Profile Lookup")
    print("="*60)
    
    tests = [
        ("Driver's License", "license", ["D99887766"]),
        ("Passport Number", "passport", ["P11223344"]),
        ("Insurance Policy", "insurance", ["Geico", "999-000"]),
        ("Phone Number", "phone", ["555"]),
        ("Email Address", "email", ["@"]),
    ]
    
    passed = 0
    for name, query, expected in tests:
        result = get_profile_info(query)
        found = result.get("found", False)
        
        if found and all(e in str(result) for e in expected):
            print(f"  ✅ {name}: PASSED")
            passed += 1
        else:
            print(f"  ❌ {name}: FAILED - {result}")
    
    print(f"\nProfile Lookup: {passed}/{len(tests)} tests passed")
    return passed == len(tests)


def test_renewal_status():
    """Test renewal status retrieval."""
    print("\n" + "="*60)
    print("📋 TESTING: Renewal Status")
    print("="*60)
    
    result = get_renewal_status()
    
    checks = [
        ("Success flag", result.get("success", False)),
        ("Urgent items present", len(result.get("urgent_items", [])) > 0),
        ("Full list present", len(result.get("full_renewal_list", "")) > 0),
        ("Action count present", "action_required" in result),
    ]
    
    passed = sum(1 for _, check in checks if check)
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
    
    print(f"\nRenewal Status: {passed}/{len(checks)} checks passed")
    return passed == len(checks)


def test_calendar_tool():
    """Test calendar event creation."""
    print("\n" + "="*60)
    print("📅 TESTING: Calendar Tool")
    print("="*60)
    
    result = create_calendar_event(
        title="Test Event",
        start_time="2025-12-15T14:00:00",
        duration_hours=1,
        description="Test description"
    )
    
    checks = [
        ("Success flag", result.get("success", False)),
        ("Event ID generated", "event_id" in result),
        ("Title preserved", result.get("title") == "Test Event"),
        ("Times set", "start" in result and "end" in result),
    ]
    
    passed = sum(1 for _, check in checks if check)
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
    
    print(f"\nCalendar Tool: {passed}/{len(checks)} checks passed")
    return passed == len(checks)


def test_gmail_tool():
    """Test Gmail draft creation."""
    print("\n" + "="*60)
    print("📧 TESTING: Gmail Tool")
    print("="*60)
    
    result = create_gmail_draft(
        to="test@example.com",
        subject="Test Subject",
        body="Test email body content."
    )
    
    checks = [
        ("Success flag", result.get("success", False)),
        ("Draft ID generated", "draft_id" in result),
        ("Recipient set", result.get("to") == "test@example.com"),
        ("Subject preserved", result.get("subject") == "Test Subject"),
    ]
    
    passed = sum(1 for _, check in checks if check)
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
    
    print(f"\nGmail Tool: {passed}/{len(checks)} checks passed")
    return passed == len(checks)


def test_router():
    """Test query routing."""
    print("\n" + "="*60)
    print("🔀 TESTING: Router Agent")
    print("="*60)
    
    router = RouterAgent()
    
    test_cases = [
        ("Create a calendar event", "admin_agent"),
        ("Draft an email", "admin_agent"),
        ("What's my license number?", "profile_agent"),
        ("Prioritize my tasks", "productivity_agent"),
        ("I'm tired, what should I do?", "productivity_agent"),
        ("Check my insurance policy", "profile_agent"),
    ]
    
    passed = 0
    for query, expected_agent in test_cases:
        result = router.route(query)
        actual = result.get("routed_to", "")
        
        if actual == expected_agent:
            print(f"  ✅ '{query[:30]}...' → {actual}")
            passed += 1
        else:
            print(f"  ❌ '{query[:30]}...' → {actual} (expected {expected_agent})")
    
    print(f"\nRouter: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_session_management():
    """Test session and memory management."""
    print("\n" + "="*60)
    print("💾 TESTING: Session Management")
    print("="*60)
    
    session = InMemorySession()
    
    # Test message adding
    session.add_user_message("Test query")
    session.add_assistant_message("Test response")
    
    # Test state management
    session.set_state("energy_level", "HIGH")
    
    checks = [
        ("Session ID generated", len(session.session_id) > 0),
        ("Messages stored", len(session.history) == 2),
        ("State stored", session.get_state("energy_level") == "HIGH"),
        ("History retrievable", len(session.get_history()) == 2),
        ("Not expired", not session.is_expired()),
    ]
    
    passed = sum(1 for _, check in checks if check)
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
    
    print(f"\nSession Management: {passed}/{len(checks)} checks passed")
    return passed == len(checks)


def test_full_agent_queries():
    """Test full agent with real queries."""
    print("\n" + "="*60)
    print("🤖 TESTING: Full Agent Queries")
    print("="*60)
    
    evaluator = AgentEvaluator()
    
    # Define test cases
    test_cases = [
        {
            "name": "License Number Lookup",
            "query": "What's my driver's license number?",
            "expected_contains": ["D99887766"],
            "expected_agent": "profile_agent"
        },
        {
            "name": "Renewal Check",
            "query": "What renewals are coming up?",
            "expected_contains": ["renewal", "insurance"],
            "expected_agent": "admin_agent"
        },
        {
            "name": "Low Energy Recommendations",
            "query": "I'm tired today, what should I work on?",
            "expected_contains": ["energy", "task"],
            "expected_agent": "productivity_agent"
        },
        {
            "name": "Calendar Event Request",
            "query": "Create a calendar event for DMV on Dec 10",
            "expected_contains": ["calendar", "event"],
            "expected_agent": "admin_agent"
        },
        {
            "name": "Email Draft Request",
            "query": "Draft an email about my insurance renewal",
            "expected_contains": ["email", "draft"],
            "expected_agent": "admin_agent"
        },
    ]
    
    for tc in test_cases:
        evaluator.run_test(
            name=tc["name"],
            query=tc["query"],
            expected_contains=tc["expected_contains"],
            expected_agent=tc.get("expected_agent")
        )
    
    summary = evaluator.get_summary()
    print(f"\n📊 Full Agent Tests: {summary['passed']}/{summary['total_tests']} passed")
    print(f"   Success Rate: {summary['success_rate']}")
    
    return summary["failed"] == 0


def run_all_tests():
    """Run all evaluation tests."""
    print("\n" + "="*70)
    print("🧪 LIFE ADMIN CONCIERGE - AGENT EVALUATION SUITE")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "Profile Lookup": test_profile_lookup(),
        "Renewal Status": test_renewal_status(),
        "Calendar Tool": test_calendar_tool(),
        "Gmail Tool": test_gmail_tool(),
        "Router Agent": test_router(),
        "Session Management": test_session_management(),
        "Full Agent Queries": test_full_agent_queries(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("📊 EVALUATION SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n{'='*70}")
    print(f"  TOTAL: {passed}/{total} test suites passed")
    print(f"  SUCCESS RATE: {(passed/total)*100:.1f}%")
    print(f"{'='*70}")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
