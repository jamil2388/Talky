import axios from 'axios';
import { API_BASE_URL } from '../config';

export const startConversation = async () => {
  const response = await axios.post(`${API_BASE_URL}/api/conversation/start`);
  return response.data;
};

export const sendAudio = async (audioBlob) => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'audio.wav');
  
  const response = await axios.post(`${API_BASE_URL}/api/conversation`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
