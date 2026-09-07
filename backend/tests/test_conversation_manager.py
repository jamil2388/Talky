import pytest
from app.services.conversation_manager import ConversationManager

def test_conversation_manager_context_truncation():
    # Setup
    manager = ConversationManager(max_turns=3)
    
    # Execution: Add 5 turns
    for i in range(5):
        manager.add_turn(role="user", content=f"User turn {i}")
        manager.add_turn(role="ai", content=f"AI turn {i}")
    
    # Verification
    context = manager.get_context()
    
    # Max turns is 3, each turn is 1 user + 1 ai message = 2 messages
    # Total history should be 3 * 2 = 6 messages
    assert len(context) == 6
    
    # Check that it kept the last 3 turns (turns 2, 3, 4)
    assert context[0]["content"] == "User turn 2"
    assert context[-1]["content"] == "AI turn 4"

def test_conversation_manager_role_alternation():
    manager = ConversationManager()
    
    # Add user message
    manager.add_turn(role="user", content="Hello")
    
    # Add AI message
    manager.add_turn(role="ai", content="Hi")
    
    context = manager.get_context()
    assert context[0]["role"] == "user"
    assert context[1]["role"] == "ai"
