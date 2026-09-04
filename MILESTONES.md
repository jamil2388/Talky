# Project Milestones

This file is used to track the major development phases, deliverables, and branches for the Local Voice Conversation Assistant. We adhere strictly to Test-Driven Development (TDD), meaning each milestone's implementation is guided and verified by pre-written test suites.

## Phase 1: Backend Base & Mock Services (TDD Core)
- [x] Branch : feature/backend-core
- [x] Write unit and integration tests first for API schemas and basic endpoint structure (`POST /api/conversation/start` and `POST /api/conversation`).
- [x] Set up the FastAPI folder structure, configuration, and dependencies (`requirements.txt`).
- [x] Implement request and response Pydantic schemas in `app/schemas/conversation.py`.
- [x] Create stub endpoint handlers in `app/api/conversation.py` that return mock response data to satisfy pre-written API tests.
- [x] Verify that all base endpoint tests pass successfully.

## Phase 2: Modular AI Services (TDD Service Wrappers)
- [x] Branch : feature/ai-services
- [x] **Speech-to-Text Wrapper (STT):**
  - [x] Write tests to verify STT wrapper behavior using local audio files (success and error conditions).
  - [x] Implement `STTService` class using a local STT engine (e.g., HuggingFace Transformers, Whisper-cpp, or Faster-Whisper).
  - [x] Run STT tests and ensure the service successfully transcribes standard test audio files.
- [x] **Language Model Wrapper (LLM):**
  - [x] Write tests to verify LLM response restrictions (simple English, max one sentence, child-friendly).
  - [x] Implement `LLMService` class with a local LLM runner integration and custom system prompts.
  - [x] Run LLM tests and verify prompt constraints are strictly satisfied.
- [ ] **Text-to-Speech Wrapper (TTS):**
  - [ ] Write tests to verify audio file generation, file output pathing, and metadata completeness.
  - [ ] Implement `TTSService` class using a local TTS engine (e.g., pyttsx3, gTTS offline, Coqui TTS, or equivalent).
  - [ ] Run TTS tests and ensure playable audio files are compiled correctly offline.
- [ ] **Conversation Context Manager:**
  - [ ] Write unit tests to verify context truncation (ensuring history stays within 3 to 6 turns) and role alternation.
  - [ ] Implement `ConversationManager` class maintaining state/history limits.
  - [ ] Run context manager tests and ensure correct context assembly.

## Phase 3: Connected Backend Pipeline Integration
- [ ] Branch : feature/backend-integration
- [ ] Write comprehensive integration tests for the full pipeline (`Audio file input -> STT -> History Context -> LLM -> TTS -> Audio output response`).
- [ ] Refactor `ConversationService` in `app/services/conversation_service.py` to orchestrate actual service instances.
- [ ] Update endpoints in `app/api/conversation.py` to route real requests through the complete orchestration pipeline.
- [ ] Verify the full pipeline's functional success using integration tests offline.

## Phase 4: Frontend Development & Component Testing
- [ ] Branch : feature/frontend-ui
- [ ] Initialize the React project with Vite, setup test suites (Jest/React Testing Library) and write basic component unit tests.
- [ ] Develop and test `AudioRecorder.jsx` for recording voice from browser microphone and handling state.
- [ ] Develop and test `Conversation.jsx` for displaying history logs and initiating conversations.
- [ ] Implement API helper in `api.js` to send recorded audio blobs and receive JSON/Audio outputs.
- [ ] Assemble all frontend parts in `App.jsx`, running local component/integration tests to ensure correct frontend flow.

## Phase 5: Refinement, Latency & Final Verification
- [ ] Branch : feature/refinement-optimization
- [ ] Add latency instrumentation tests to benchmark local pipeline execution.
- [ ] Refine local model configurations and quantization to optimize execution speed on standard hardware.
- [ ] Perform full-pipeline manual and automated testing to ensure offline reliability and child-appropriate conversation guidelines.
