import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
});

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor for Token Refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 Unauthorized and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Attempt to refresh token (mock endpoint for now)
        // const { data } = await axios.post('/auth/refresh', { refresh: localStorage.getItem('refreshToken') });
        // localStorage.setItem('accessToken', data.accessToken);
        // api.defaults.headers.common['Authorization'] = `Bearer ${data.accessToken}`;
        // return api(originalRequest);
        
        // If refresh fails or not implemented, logout
        console.warn("Session expired. Logging out.");
        localStorage.removeItem('accessToken');
        window.location.href = '/auth/login';
      } catch (refreshError) {
        localStorage.removeItem('accessToken');
        window.location.href = '/auth/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

