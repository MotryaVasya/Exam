import api from './api';

export const adminService = {
  getUsers: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);
    if (params.search) queryParams.append('search', params.search);

    const response = await api.get(`/admin/users/?${queryParams.toString()}`);
    return response.data;
  },

  getUsersCount: async () => {
    const response = await api.get('/admin/users/count');
    return response.data;
  },

  updateUserStatus: async (id, isActive) => {
    const response = await api.patch(`/admin/users/${id}/status?is_active=${isActive}`);
    return response.data;
  },

  deleteUser: async (id) => {
    const response = await api.delete(`/admin/users/${id}`);
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/admin/stats/');
    return response.data;
  },

  getLogs: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);

    const response = await api.get(`/admin/logs/?${queryParams.toString()}`);
    return response.data;
  },

  cleanupLogs: async (days = 30) => {
    const response = await api.post(`/admin/logs/cleanup?days=${days}`);
    return response.data;
  },
};
