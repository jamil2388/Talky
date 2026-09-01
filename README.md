# Local Voice Conversation Assistant

This project is a locally running, offline voice-based conversational application designed to help users (particularly children) practice simple English conversations. The application captures spoken English from a microphone, transcribes it to text, generates a short one-line response using a local language model, converts that response back to speech, and plays it back to the user.

It supports two conversation modes:
- **AI Initiated:** The AI starts the conversation with a simple sentence or question.
- **User Initiated:** The user starts speaking, and the AI responds.

The entire application runs fully offline, ensuring high privacy and zero cloud API dependency.

## Features

- **Local Speech-to-Text (STT):** Converts recorded English audio files into text locally.
- **Modular AI Response Generation (LLM):** Uses a local language model configured to respond in simple English, with a single, child-friendly sentence.
- **Short-Term Context Management:** Automatically maintains the last 3 to 6 turns of the conversation context to provide relevant replies.
- **Local Text-to-Speech (TTS):** Converts AI text response to browser-playable audio offline.
- **Interactive React UI:** Simple tap-and-record microphone interface with real-time text visualization and automated audio playback.
- **Test-Driven Development (TDD):** Built using a rigorous TDD workflow, ensuring all modules and integration flows are verified via automated tests.

## How It Works

1. **User Input / Initiation:** The user starts speaking using the React frontend's microphone control (FR-02), or clicks a button to request the AI to initiate the conversation (FR-01).
2. **Audio Transmission:** Recorded audio is sent via multipart POST request to the FastAPI backend.
3. **Local Speech-to-Text:** The FastAPI backend passes the audio to the STT module, which transcribes the audio into plain text (FR-03).
4. **Context Preparation:** The backend’s Conversation Manager prepends recent dialogue turns (3-6 turns) to maintain context (FR-06).
5. **Local LLM Execution:** The combined context is sent to a local LLM, which generates a short, simple, child-friendly response of exactly one sentence (FR-04).
6. **Local Text-to-Speech:** The generated text response is converted to speech audio by the TTS module (FR-05).
7. **Frontend Playback:** The frontend receives the audio response and plays it back automatically, displaying the transcription and reply.

## Requirements

- Python 3.10+
- Node.js (v18+) & npm
- Local model runtime dependencies (e.g., ffmpeg for audio processing, local LLM runner like Ollama, or Python-native libraries)
- Microphone/Audio recording hardware on host machine

## Installation

### 1. Clone the repository:
```bash
git clone <repository-url>
cd Talky
```

### 2. Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup:
```bash
cd ../frontend
npm install
```

## Usage

### Test-Driven Development (TDD) Workflow
We prioritize writing automated tests *before* writing production code.

To run the backend tests:
```bash
cd backend
pytest
```

To run the frontend tests:
```bash
cd frontend
npm test
```

### Running the Application

1. **Start the Backend Server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start the Frontend Application:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Web UI:**
   Open your browser and navigate to `http://localhost:5173` (or the port specified by Vite).

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── api/
│   │   │   └── conversation.py   # Conversation endpoints (/start, /conversation)
│   │   ├── services/
│   │   │   ├── conversation_service.py # Core orchestration service
│   │   │   ├── stt_service.py    # Local Speech-to-Text module wrapper
│   │   │   ├── llm_service.py    # Local LLM wrapper & system prompt logic
│   │   │   └── tts_service.py    # Local Text-to-Speech module wrapper
│   │   └── schemas/
│   │       └── conversation.py   # Request/response validation schemas
│   ├── tests/                    # Backend test suites (unit & integration tests)
│   ├── models/                   # Directory to store local offline models
│   ├── generated_audio/          # Output folder for generated TTS voice files
│   └── requirements.txt          # Python packages
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioRecorder.jsx # Recording button & microphone state
│   │   │   └── Conversation.jsx  # Main conversation message logs and actions
│   │   ├── services/
│   │   │   └── api.js            # Axios/Fetch integration with FastAPI endpoints
│   │   ├── App.jsx               # Application main layout
│   │   └── main.jsx              # React initialization
│   ├── tests/                    # Frontend unit and component tests
│   ├── package.json              # Frontend scripts and packages
│   └── vite.config.js            # Build and development configuration
│
└── GEMINI.md                     # Project rules and instructions
```
