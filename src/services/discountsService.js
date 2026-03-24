import api from './api';

export const discountsService = {
  getByCode: async (code) => {
    const response = await api.get(`/discounts/code/${code}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/admin/discounts/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/admin/discounts/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/admin/discounts/${id}`);
    return response.data;
  },
};
