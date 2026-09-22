import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Assuming FastAPI runs here

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
