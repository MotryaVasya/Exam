import api from './api';

export const producersService = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await api.get(`/producers/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/producers/${id}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/admin/producers/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/admin/producers/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/admin/producers/${id}`);
    return response.data;
  },
};
