import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Conversation from './Conversation';
import * as api from '../services/api';

vi.mock('../services/api', () => ({
  startConversation: vi.fn(),
  sendAudio: vi.fn(),
}));

// Mock Audio and MediaRecorder
window.Audio = class {
  constructor(url) {
    this.url = url;
  }
  play() {
    return Promise.resolve();
  }
};

class MockMediaRecorder {
  constructor(stream, options) {
    this.stream = stream;
    this.options = options;
    MockMediaRecorder.instances.push(this);
  }
  start() {
    if (this.onstart) this.onstart();
  }
  stop() {
    if (this.ondataavailable) {
      this.ondataavailable({ data: new Blob(['audio'], { type: 'audio/webm' }) });
    }
    if (this.onstop) this.onstop();
  }
  static instances = [];
}
window.MediaRecorder = MockMediaRecorder;
window.navigator.mediaDevices = {
  getUserMedia: vi.fn().mockResolvedValue({
    getTracks: () => [{ stop: vi.fn() }]
  })
};

describe('Conversation Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    MockMediaRecorder.instances = [];
  });

  it('renders initial state correctly', () => {
    render(<Conversation />);
    expect(screen.getByText(/Talky - Voice Assistant/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Start AI Conversation/i })).toBeInTheDocument();
    expect(screen.getByText(/No messages yet/i)).toBeInTheDocument();
  });

  it('handles starting conversation successfully', async () => {
    api.startConversation.mockResolvedValueOnce({
      ai_text: 'Hello! How can I help you?',
      audio_url: '/audio/g_1.wav'
    });

    render(<Conversation />);
    const startButton = screen.getByRole('button', { name: /Start AI Conversation/i });
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText(/Hello! How can I help you?/i)).toBeInTheDocument();
    });
  });

  it('handles sending audio message successfully', async () => {
    api.sendAudio.mockResolvedValueOnce({
      user_text: 'Hi there',
      ai_text: 'Hello back!',
      audio_url: '/audio/g_2.wav'
    });

    render(<Conversation />);
    const recordButton = screen.getByRole('button', { name: /Record/i });

    // Start & stop recording
    fireEvent.click(recordButton);
    const stopButton = await screen.findByRole('button', { name: /Stop/i });
    fireEvent.click(stopButton);

    await waitFor(() => {
      expect(screen.getByText(/Hi there/i)).toBeInTheDocument();
      expect(screen.getByText(/Hello back!/i)).toBeInTheDocument();
    });
  });
});
