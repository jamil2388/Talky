import { vi, describe, it, expect, beforeEach } from 'vitest';
import axios from 'axios';
import { startConversation, sendAudio } from './api';

vi.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should call startConversation endpoint', async () => {
    axios.post.mockResolvedValue({ data: { session_id: 'test-123' } });
    const response = await startConversation();
    expect(axios.post).toHaveBeenCalledWith(expect.stringContaining('/api/conversation/start'));
    expect(response.session_id).toBe('test-123');
  });

  it('should call sendAudio endpoint with FormData', async () => {
    const mockAudioBlob = new Blob(['audio-data'], { type: 'audio/wav' });
    axios.post.mockResolvedValue({ data: { response_text: 'Hello!' } });

    const response = await sendAudio(mockAudioBlob);
    
    expect(axios.post).toHaveBeenCalled();
    const [url, data] = axios.post.mock.calls[0];

    console.log(axios.post.mock.calls);

    expect(url).toContain('/api/conversation');
    expect(data).toBeInstanceOf(FormData);
    expect(response.response_text).toBe('Hello!');
  });
});
