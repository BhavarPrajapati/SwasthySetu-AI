/**
 * Authentication API calls for MongoDB + Django backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export async function registerUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
      password2: password,
      first_name: '',
      last_name: ''
    })
  });

  const data = await response.json();

  if (!response.ok) {
    // Handle DRF field-level errors like { password: ["too short"] }
    const firstError = Object.values(data)[0];
    const errorMessage = data.error || data.message ||
      (Array.isArray(firstError) ? firstError[0] : firstError) ||
      'Registration failed';
    throw new Error(errorMessage);
  }

  return data;
}

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password
    })
  });

  const data = await response.json();

  if (!response.ok) {
    const errorMessage = data.error || data.message || 'Login failed';
    throw new Error(errorMessage);
  }

  return {
    AuthenticationResult: {
      IdToken: data.access,
      AccessToken: data.access,
      RefreshToken: data.refresh
    },
    user: data.user
  };
}

export async function logoutUser() {
  // Clear tokens from localStorage
  localStorage.removeItem('idToken');
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  return true;
}

export async function confirmUser(email, code) {
  // Django doesn't require email confirmation in our setup
  // Return success immediately
  return { status: 'confirmed' };
}

export async function resendConfirmationCode(email) {
  // Django doesn't require email confirmation in our setup
  // Return success immediately
  return { status: 'code_sent' };
}
