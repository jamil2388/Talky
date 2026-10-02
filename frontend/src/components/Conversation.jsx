import React, { useState, useRef, useEffect } from 'react';
import AudioRecorder from './AudioRecorder';
import { startConversation, sendAudio } from '../services/api';
import './AudioRecorder.css';

export default function Conversation() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const audioRef = useRef(null);

  const playAudio = (audioUrl) => {
    if (!audioUrl) return;
    const fullUrl = audioUrl.startsWith('http') ? audioUrl : `http://localhost:8000${audioUrl}`;
    const audio = new Audio(fullUrl);
    audio.play().catch((err) => {
      console.error('Error playing audio response:', err);
    });
  };

  const handleStartConversation = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await startConversation();
      setMessages((prev) => [...prev, { role: 'ai', text: data.ai_text }]);
      if (data.audio_url) {
        playAudio(data.audio_url);
      }
    } catch (err) {
      console.error('Failed to start conversation:', err);
      setError('Failed to start conversation. Is backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleRecordingComplete = async (audioBlob) => {
    setLoading(true);
    setError(null);
    try {
      const data = await sendAudio(audioBlob);
      setMessages((prev) => [
        ...prev,
        { role: 'user', text: data.user_text },
        { role: 'ai', text: data.ai_text },
      ]);
      if (data.audio_url) {
        playAudio(data.audio_url);
      }
    } catch (err) {
      console.error('Failed to send audio:', err);
      setError('Failed to process voice message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="conversation-container" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Talky - Voice Assistant</h1>
      
      <div className="controls" style={{ marginBottom: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
        <button
          onClick={handleStartConversation}
          disabled={loading}
          className="start-btn"
          style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
        >
          🤖 Start AI Conversation
        </button>
      </div>

      {error && <div className="error-banner" style={{ color: 'red', marginBottom: '15px', textAlign: 'center' }}>{error}</div>}
      {loading && <div className="loading-banner" style={{ color: 'blue', marginBottom: '15px', textAlign: 'center' }}>Thinking...</div>}

      <div
        className="message-log"
        style={{
          border: '1px solid #ccc',
          borderRadius: '8px',
          padding: '15px',
          minHeight: '250px',
          maxHeight: '400px',
          overflowY: 'auto',
          marginBottom: '20px',
          backgroundColor: '#f9f9f9',
          textAlign: 'left'
        }}
      >
        {messages.length === 0 ? (
          <p style={{ color: '#888', textAlign: 'center' }}>No messages yet. Click "Start AI Conversation" or record your voice below!</p>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              style={{
                marginBottom: '12px',
                padding: '10px',
                borderRadius: '6px',
                backgroundColor: msg.role === 'user' ? '#e1f5fe' : '#e8f5e9',
              }}
            >
              <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong> {msg.text}
            </div>
          ))
        )}
      </div>

      <div className="recorder-section" style={{ display: 'flex', justifyContent: 'center' }}>
        <AudioRecorder onRecordingComplete={handleRecordingComplete} disabled={loading} />
      </div>
    </div>
  );
}
