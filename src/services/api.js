import axios from 'axios';

// ✅ Base URL from .env - Django backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// ✅ Axios instance for main backend (MongoDB + Django)
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

// ✅ Authorization interceptor - JWT Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("idToken") || localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ Response error interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('idToken');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ==============================
// SCREENING API CALLS (MongoDB)
// ==============================

/**
 * Memory Assessment
 */
export async function runMemoryAssessment(payload) {
  const response = await api.post('/screening/memory/', payload);
  return response.data;
}

/**
 * Voice Transcription & Analysis
 */
export async function uploadAudioForTranscription(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'voice-input.webm');

  const response = await api.post('/screening/voice/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  return response.data;
}

/**
 * Alzheimer Prediction
 */
export async function getPrediction(payload) {
  const response = await api.post('/screening/prediction/', payload);
  return response.data;
}

/**
 * Get Screening History
 */
export async function getScreeningHistory() {
  const response = await api.get('/screening/history/');
  return response.data;
}

/**
 * Get Assessments (alias for history)
 */
export async function getAssessments(userId) {
  const response = await api.get('/screening/history/');
  return response.data;
}

/**
 * Get Screening Result Details
 */
export async function getScreeningResult(resultId) {
  const response = await api.get(`/screening/result/${resultId}/`);
  return response.data;
}

/**
 * PHC Finder - Get nearby health centers
 */
export async function findNearbyPHC(latitude, longitude) {
  const response = await api.post('/screening/phc-finder/', {
    latitude,
    longitude
  });
  return response.data;
}

/**
 * Text to Speech (if needed - local placeholder)
 */
export async function getPollyInstructionsAudio(payload) {
  // Using browser's native speech synthesis if available
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(payload.text || '');
    return { message: 'Using browser speech synthesis' };
  }
  return null;
}

/**
 * Save Assessment Results
 */
export async function saveAssessment(payload) {
  const response = await api.post('/screening/save/', payload);
  return response.data;
}

export default api;