# Technical Product Requirements Document (PRD)

## 1. Product Summary

### Product Name
**Local Voice Conversation Assistant**

### Product Description
A locally running, offline voice-based conversational application that allows a user to practice simple English conversations.

The application captures spoken English, converts it to text, generates a short AI response using a local language model, converts the response into speech, and plays it back to the user.

The application supports two modes:
- **AI Initiated:** The AI starts the conversation.
- **User Initiated:** The user starts speaking and the AI responds.

The first version is designed as a local application and does not require cloud APIs or user authentication.

---

## 2. Problem Statement

The user needs a simple conversational system that provides immediate spoken responses to short English sentences or questions.

The system should maintain enough conversation context to generate relevant responses while keeping the interaction simple and the response limited to approximately one sentence.

---

## 3. MVP Scope

### In Scope
- English speech input.
- Microphone recording.
- Local speech-to-text.
- Local AI response generation.
- Short conversational context.
- One-line AI responses.
- Local text-to-speech.
- Audio playback.
- AI conversation initiation.
- FastAPI backend.
- React frontend.
- Local/offline operation after installation.

### Out of Scope
- User accounts.
- Cloud deployment.
- Database storage.
- Conversation analytics.
- Progress tracking.
- Multiple users.
- Mobile application.
- Advanced educational features.
- Grammar scoring or correction.
- Wake-word detection.
- Continuous background listening.

---

# 4. High-Level Architecture

```text
React Frontend
      │
      │ Audio / API Requests
      ▼
FastAPI Backend
      │
      ├── Speech-to-Text Module
      │
      ├── Conversation Manager
      │
      ├── Local LLM
      │
      └── Text-to-Speech Module
      │
      ▼
Response Audio + Text
      │
      ▼
React Frontend
```

The frontend is responsible for recording and playing audio.

FastAPI acts as the orchestration layer. It receives audio, coordinates the AI pipeline, and returns the generated response.

---

# 5. Core Conversation Pipeline

The primary system flow is:

```text
User Speech
   ↓
Audio Recording
   ↓
Speech-to-Text
   ↓
Conversation Context
   ↓
Local LLM
   ↓
AI Text Response
   ↓
Text-to-Speech
   ↓
Audio Playback
```

The pipeline should execute sequentially for the MVP.

---

# 6. Technical Components

## 6.1 Frontend

### Technology
- React
- Browser MediaRecorder API

### Responsibilities
- Start and stop microphone recording.
- Send recorded audio to FastAPI.
- Display transcribed user text.
- Display AI response text.
- Receive and play generated AI audio.
- Provide a button to initiate a conversation.

### Basic UI

```text
--------------------------------
 Local Voice Conversation
--------------------------------

 AI: Hi! How are you today?

 User: [Tap and hold to speak]

 [ Start Recording ]
 [ Stop Recording ]

 You said:
 How are you?

 AI:
 I am good. What are you doing?
--------------------------------
```

---

## 6.2 FastAPI Backend

### Responsibilities
- Receive audio files.
- Validate audio input.
- Send audio to the STT module.
- Manage recent conversation history.
- Send conversation input to the local LLM.
- Send generated text to the TTS module.
- Return text and audio to the frontend.

The backend should keep AI components modular so that STT, LLM, and TTS models can be replaced later.

---

# 7. API Design

## POST `/api/conversation`

### Purpose
Process user speech and generate an AI voice response.

### Input
```text
multipart/form-data
audio: recorded_audio_file
```

### Internal Process
```text
Audio
 → Transcription
 → Conversation Context
 → LLM Response
 → TTS Audio
 → Response
```

### Response
```json
{
  "user_text": "How are you?",
  "ai_text": "I am good. How are you?"
}
```

The generated audio can initially be returned through a separate audio endpoint or as a file response.

---

## POST `/api/conversation/start`

### Purpose
Generate an AI sentence to start a conversation.

### Internal Process
```text
Conversation Prompt
        ↓
      Local LLM
        ↓
      AI Text
        ↓
        TTS
        ↓
   Generated Audio
```

Example:

```json
{
  "ai_text": "Hi! What are you doing today?"
}
```

---

# 8. Conversation Manager

The conversation manager is responsible for maintaining short-term context.

Example:

```python
conversation_history = [
    {
        "role": "assistant",
        "content": "Hi! What are you doing today?"
    },
    {
        "role": "user",
        "content": "I am playing."
    }
]
```

Only recent conversation messages should be passed to the model.

### Initial Rule
Keep approximately the last **3 to 6 conversation turns**.

This prevents the context from growing unnecessarily and helps maintain faster response times.

---

# 9. AI Response Requirements

The local LLM should receive a system instruction similar to:

```text
You are having a conversation with a child learning English.

Rules:
- Use simple English.
- Reply in only one short sentence.
- Keep the response relevant to the conversation.
- You may ask a simple question to continue the conversation.
- Do not provide long explanations.
```

Example:

**User:**  
> I played outside.

**AI:**  
> That sounds fun! Who did you play with?

The exact model will be selected during implementation based on hardware performance.

---

# 10. Speech-to-Text Requirements

The STT component should:

- Run locally.
- Accept recorded audio.
- Transcribe English speech.
- Return plain text.
- Return a confidence value if supported by the selected model.

### Initial Limitation
The first version will not attempt to automatically correct uncertain transcriptions.

The frontend should display the transcription so the developer can evaluate recognition quality during testing.

---

# 11. Text-to-Speech Requirements

The TTS component should:

- Run locally.
- Accept AI-generated text.
- Generate speech audio.
- Produce an audio format playable in a browser.
- Use one default voice in the MVP.

The frontend should automatically play the response after receiving it.

---

# 12. Local Model Requirements

The application should support interchangeable local models.

```text
modules/
├── stt/
│   └── speech_to_text.py
│
├── llm/
│   └── conversation_model.py
│
└── tts/
    └── text_to_speech.py
```

The application code should communicate with abstract service functions rather than depending directly on a specific model implementation.

Example:

```python
text = speech_to_text(audio)
response = generate_response(text, history)
audio = text_to_speech(response)
```

This allows individual components to be replaced without modifying the complete pipeline.

---

# 13. Backend Project Structure

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── conversation.py
│   │
│   ├── services/
│   │   ├── conversation_service.py
│   │   ├── stt_service.py
│   │   ├── llm_service.py
│   │   └── tts_service.py
│   │
│   └── schemas/
│       └── conversation.py
│
├── models/
├── generated_audio/
└── requirements.txt
```

---

# 14. Frontend Project Structure

```text
frontend/
├── src/
│   ├── components/
│   │   ├── AudioRecorder.jsx
│   │   └── Conversation.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── App.jsx
│   └── main.jsx
```

The frontend should remain intentionally simple for the MVP.

---

# 15. Functional Requirements

### FR-01: AI Initiation
The user can request the AI to start a conversation.

### FR-02: Voice Input
The user can record a voice message through the browser.

### FR-03: Transcription
The system converts the recorded English speech into text locally.

### FR-04: AI Response
The system generates one short conversational response using a local language model.

### FR-05: Voice Output
The system converts the AI response into speech and plays it automatically.

### FR-06: Conversation Context
The system maintains recent conversation messages during the current session.

---

# 16. Non-Functional Requirements

### Offline Operation
The application must operate without an internet connection after all dependencies and models have been downloaded.

### Performance
The application should prioritize reasonable response latency, but real-time performance is not required for the first version.

### Privacy
Voice recordings should be processed locally and should not be sent to third-party APIs.

### Modularity
STT, LLM, and TTS components should be replaceable.

### Simplicity
The MVP should prioritize a working end-to-end pipeline over advanced features.

---

# 17. Known Limitations

- Speech recognition may have reduced accuracy for child speech.
- Local LLM response quality depends on the selected model and available hardware.
- Response latency is the combined processing time of STT, LLM, and TTS.
- The system will only maintain temporary conversation history during an active session.
- The AI may occasionally produce an inappropriate or irrelevant response despite prompt restrictions.
- Audio quality depends on the microphone and selected TTS model.

---

# 18. Development Plan

## Phase 1: Core AI Modules
Individually test:
- Local STT.
- Local LLM.
- Local TTS.

**Success:** Each component works independently through Python.

## Phase 2: Backend Pipeline
Connect:

```text
STT → Conversation Manager → LLM → TTS
```

**Success:** A single audio file can produce a spoken AI response.

## Phase 3: Web Interface
Add React microphone recording and FastAPI integration.

**Success:** The complete pipeline works through the browser.

## Phase 4: Refinement
Test real conversations and improve:
- transcription accuracy,
- response quality,
- prompt design,
- latency.

---

# 19. MVP Success Criteria

The first version is successful when:

1. The AI can initiate a short conversation.
2. The user can speak a short English sentence.
3. The system transcribes the speech locally.
4. The local LLM generates a relevant one-line response.
5. The response is converted to speech.
6. The user can hear the AI response and continue the conversation.
7. The application runs locally without external paid services.

---

## Final MVP Definition

**A local React + FastAPI application where a user speaks one sentence, the application transcribes it locally, generates one short AI response using a local LLM, converts that response into speech, and plays it back while maintaining minimal conversation context.**