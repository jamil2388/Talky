import pytest
from app.services.llm_service import LLMService

def test_llm_service_response_constraints():
    """Verify LLM service generates child-friendly, single-sentence, simple English."""
    llm_service = LLMService()
    
    # Testing with a simple prompt
    response = llm_service.generate("What is your name?")
    
    # Assertions based on constraints
    assert isinstance(response, str)
    assert len(response.split('.')) <= 2  # Basic check for single sentence
    assert len(response.split()) < 20     # Simple English (word count)
    
def test_llm_service_empty_prompt():
    """Verify LLM service handles empty input."""
    llm_service = LLMService()
    with pytest.raises(ValueError):
        llm_service.generate("")
