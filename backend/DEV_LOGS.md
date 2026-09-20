# Dev Logs

## Issue: Deadlock in Integration Tests
### Problem
Integration tests running via `pytest` and `FastAPI TestClient` hang indefinitely when executing the `/api/conversation` endpoint.
The trace locates the hang at `self.engine.runAndWait()` inside `TTSService.convert_text_to_speech()`. 
`pyttsx3` is a synchronous, blocking engine. Calling `runAndWait()` inside the FastAPI route handler blocks the thread processing the request. Because `pyttsx3` requires a responsive event loop to interact with the OS speech driver and signal completion, and that loop is being blocked by the test runner itself, the engine never receives the completion signal. This results in a classic deadlock where the thread waits for a completion signal that it is currently preventing from being processed.

### Proposed Fix: Dependency Injection
Refactor `ConversationService` and the FastAPI endpoint to use Dependency Injection. By injecting the `TTSService` (and other services) rather than instantiating them globally in `conversation.py`, we can:
1. Provide a `MockTTSService` during testing that simulates audio file generation without invoking the blocking `pyttsx3` event loop.
2. Maintain clean, modular production code that still uses the real `TTSService`.
This will resolve the deadlock by bypassing the need for a real speech driver during integration testing.
