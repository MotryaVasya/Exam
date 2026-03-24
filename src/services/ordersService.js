import api from './api';

export const ordersService = {
  getMyOrders: async (skip = 0, limit = 100) => {
    const response = await api.get(`/orders/my?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/orders/', data);
    return response.data;
  },

  getAllAdmin: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);

    const response = await api.get(`/admin/orders/?${queryParams.toString()}`);
    return response.data;
  },

  updateAdmin: async (id, data) => {
    const response = await api.put(`/admin/orders/${id}`, data);
    return response.data;
  },

  deleteAdmin: async (id) => {
    const response = await api.delete(`/admin/orders/${id}`);
    return response.data;
  },
};
