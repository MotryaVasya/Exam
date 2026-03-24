import api from './api';

export const watchesService = {
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);
    if (params.producer_id) queryParams.append('producer_id', params.producer_id);
    if (params.type) queryParams.append('type', params.type);
    if (params.gender) queryParams.append('gender', params.gender);
    if (params.min_price) queryParams.append('min_price', params.min_price);
    if (params.max_price) queryParams.append('max_price', params.max_price);

    const response = await api.get(`/watches/?${queryParams.toString()}`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/watches/${id}`);
    return response.data;
  },

  getAllAdmin: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);
    if (params.search) queryParams.append('search', params.search);

    const response = await api.get(`/admin/watches/?${queryParams.toString()}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/admin/watches/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/admin/watches/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/admin/watches/${id}`);
    return response.data;
  },

  updateCount: async (id, count) => {
    const response = await api.patch(`/admin/watches/${id}/count?count=${count}`);
    return response.data;
  },
};
