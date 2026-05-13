import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Uvicorn default
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token expiration generically
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Optionally trigger refresh logic or redirect to login here
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
