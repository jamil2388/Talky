import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AudioRecorder from './AudioRecorder';

// Mock MediaRecorder
class MockMediaRecorder {
  constructor(stream, options) {
    this.stream = stream;
    this.options = options;
    this.state = 'inactive';
    MockMediaRecorder.instances.push(this);
  }

  start() {
    this.state = 'recording';
    if (this.onstart) this.onstart();
  }

  stop() {
    this.state = 'inactive';
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

describe('AudioRecorder Component', () => {
  beforeEach(() => {
    MockMediaRecorder.instances = [];
    vi.clearAllMocks();
  });

  it('renders record button in idle state', () => {
    const onRecordingComplete = vi.fn();
    render(<AudioRecorder onRecordingComplete={onRecordingComplete} />);
    
    const recordButton = screen.getByRole('button', { name: /record/i });
    expect(recordButton).toBeInTheDocument();
    expect(screen.getByText(/tap to record/i)).toBeInTheDocument();
  });

  it('starts and stops recording correctly', async () => {
    const onRecordingComplete = vi.fn();
    render(<AudioRecorder onRecordingComplete={onRecordingComplete} />);

    const recordButton = screen.getByRole('button', { name: /record/i });

    // Start recording
    fireEvent.click(recordButton);
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /stop/i })).toBeInTheDocument();
    });

    const stopButton = screen.getByRole('button', { name: /stop/i });

    // Stop recording
    fireEvent.click(stopButton);

    await waitFor(() => {
      expect(onRecordingComplete).toHaveBeenCalledWith(expect.any(Blob));
    });
  });
});
