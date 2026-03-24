import api from './api';

export const authService = {
  login: async (email, password) => {
    const response = await api.post('/users/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },

  isAuthenticated: () => !!localStorage.getItem('token'),
  
  getUserFromStorage: () => JSON.parse(localStorage.getItem('user') || 'null'),
};
