# Project Logs - Local Voice Conversation Assistant

## Phase 1: Backend Base & Mock Services (TDD Core)
**Status:** Completed

### Steps Performed:
1.  **Branch Initialization:** Created and switched to `feature/backend-core` to isolate Phase 1 development.
2.  **Project Infrastructure:**
    *   Created `backend/` structure: `app/` (API, services, schemas), `tests/`.
    *   Defined `backend/requirements.txt` with essential dependencies (fastapi, uvicorn, pydantic, pytest, httpx).
    *   Created `backend/pytest.ini` to configure the test environment.
3.  **TDD - Test Implementation (Before Code):**
    *   Created `backend/tests/test_schemas.py` to define Pydantic schema validation requirements.
    *   Created `backend/tests/test_api.py` to define FastAPI endpoint functional expectations (API structure, status codes, input validation).
4.  **Implementation (To satisfy tests):**
    *   Created Pydantic schemas in `backend/app/schemas/conversation.py`.
    *   Created router and mock endpoint handlers in `backend/app/api/conversation.py`.
    *   Initialized the FastAPI app in `backend/app/main.py`.
5.  **Verification:**
    *   Ran `pytest` to confirm all 7 test cases passed (tests for API endpoints and schemas).
    *   Verified the integration successfully.

## Phase 2: Modular AI Services (TDD Service Wrappers)
**Status:** In Progress

### Steps Performed:
1.  **Branch Initialization:** Switched to `feature/ai-services` to isolate Phase 2 development.
2.  **STT-Service Implementation:**
    *   Created `backend/tests/test_stt_service.py` to define STT wrapper requirements.
    *   Implemented `STTService` in `backend/app/services/stt_service.py`.
3.  **LLM-Service Implementation:**
    *   Created `backend/tests/test_llm_service.py` to define LLM wrapper constraints (single sentence, simple English).
    *   Implemented `LLMService` in `backend/app/services/llm_service.py` with placeholder engine integration.
    *   Verified successful implementation by running pytest.
4. **TTS-Service Implementation:**
    *   Added `pyttsx3` to `requirements.txt`.
    *   Created `backend/tests/test_tts_service.py` to verify audio file generation.
    *   Implemented `TTSService` in `backend/app/services/tts_service.py` using `pyttsx3`.
    *   Verified successful implementation by running pytest.
5.  **Conversation-Manager Implementation:**
    *   Created `backend/tests/test_conversation_manager.py` to define history truncation and role alternation requirements.
    *   Implemented `ConversationManager` in `backend/app/services/conversation_manager.py`.
    *   Verified successful implementation by running pytest.

## Phase 3: Connected Backend Pipeline Integration
**Status:** In Progress

### Steps Performed:
1.  **Branch Initialization:** Created and switched to `feature/backend-integration` to isolate Phase 3 development.
2.  **Pipeline Integration:**
    *   Created `backend/tests/test_integration.py` to define end-to-end pipeline behavior (`Audio -> STT -> History -> LLM -> TTS -> Audio`).
    *   Implemented `ConversationService` in `backend/app/services/conversation_service.py` to orchestrate STT, LLM, TTS, and ConversationManager.
    *   Verified full pipeline success via integration tests.
