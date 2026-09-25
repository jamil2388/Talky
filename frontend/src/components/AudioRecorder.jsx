import React, { useState, useRef } from 'react';
import './AudioRecorder.css';

export default function AudioRecorder({ onRecordingComplete, disabled = false }) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        if (onRecordingComplete) {
          onRecordingComplete(audioBlob);
        }
        // Stop all tracks on the active stream to release microphone
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="audio-recorder">
      {!isRecording ? (
        <button
          className="record-btn"
          onClick={startRecording}
          disabled={disabled}
          aria-label="Record"
        >
          🎤 Tap to Record
        </button>
      ) : (
        <button
          className="stop-btn recording-pulse"
          onClick={stopRecording}
          disabled={disabled}
          aria-label="Stop"
        >
          ⏹️ Stop Recording
        </button>
      )}
    </div>
  );
}
