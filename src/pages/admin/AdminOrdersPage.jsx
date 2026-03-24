import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { ordersService, adminService } from '../../services';
import { Button, Table, Pagination, Modal, Badge, Select, toast } from '../../components/ui';

const AdminOrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [isStatusModalOpen, setIsStatusModalOpen] = useState(false);
  const [newStatus, setNewStatus] = useState('');

  const itemsPerPage = 10;

  useEffect(() => {
    loadOrders();
  }, [currentPage]);

  const loadOrders = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await adminService.getUsers({ skip: 0, limit: 100 }); // Для получения user_id
      const ordersData = await ordersService.getAllAdmin({ skip, limit: itemsPerPage });
      setOrders(ordersData);
    } catch (error) {
      toast.error('Ошибка загрузки заказов');
    } finally {
      setLoading(false);
    }
  };

  const openStatusModal = (order) => {
    setSelectedOrder(order);
    setNewStatus(order.status);
    setIsStatusModalOpen(true);
  };

  const handleStatusChange = async () => {
    try {
      await ordersService.updateAdmin(selectedOrder.id, { status: newStatus });
      toast.success('Статус обновлен');
      setIsStatusModalOpen(false);
      loadOrders();
    } catch (error) {
      toast.error('Ошибка при обновлении статуса');
    }
  };

  const handleDelete = async (order) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот заказ?')) return;
    try {
      await ordersService.deleteAdmin(order.id);
      toast.success('Заказ удален');
      loadOrders();
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const getStatusBadge = (status) => {
    const map = {
      pending: { variant: 'warning', label: 'В обработке' },
      confirmed: { variant: 'info', label: 'Подтвержден' },
      shipped: { variant: 'purple', label: 'Отправлен' },
      delivered: { variant: 'success', label: 'Доставлен' },
      cancelled: { variant: 'danger', label: 'Отменен' },
    };
    const cfg = map[status] || { variant: 'default', label: status };
    return <Badge variant={cfg.variant}>{cfg.label}</Badge>;
  };

  const columns = [
    { header: 'ID', accessor: 'id', width: '60px' },
    {
      header: 'Клиент',
      accessor: 'user_id',
      render: (_, row) => <span className="font-medium">#{row.user_id}</span>,
    },
    {
      header: 'Сумма',
      accessor: 'total_price',
      render: (v) => <span className="font-bold">{Number(v).toLocaleString()} ₽</span>,
    },
    {
      header: 'Статус',
      accessor: 'status',
      render: (v) => getStatusBadge(v),
    },
    {
      header: 'Доставка',
      accessor: 'is_pickup',
      render: (v) => v ? 'Самовывоз' : 'Доставка',
    },
    {
      header: 'Дата',
      accessor: 'created_at',
      render: (v) => new Date(v).toLocaleDateString('ru-RU'),
    },
    {
      header: 'Действия',
      accessor: 'actions',
      render: (_, row) => (
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => openStatusModal(row)}>Статус</Button>
          <Button variant="ghost" size="sm" onClick={() => handleDelete(row)} className="text-red-600">Удалить</Button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">Заказы</h1>
        <p className="text-primary-600">Управление заказами клиентов</p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <Table columns={columns} data={orders} />
        <Pagination currentPage={currentPage} totalPages={Math.ceil(orders.length / itemsPerPage) || 1} onPageChange={setCurrentPage} />
      </div>

      <Modal isOpen={isStatusModalOpen} onClose={() => setIsStatusModalOpen(false)} title="Изменить статус заказа" size="sm">
        <div className="space-y-4">
          <Select
            label="Статус"
            value={newStatus}
            onChange={e => setNewStatus(e.target.value)}
            options={[
              { value: 'pending', label: 'В обработке' },
              { value: 'confirmed', label: 'Подтвержден' },
              { value: 'shipped', label: 'Отправлен' },
              { value: 'delivered', label: 'Доставлен' },
              { value: 'cancelled', label: 'Отменен' },
            ]}
          />
          <div className="flex gap-3">
            <Button variant="primary" onClick={handleStatusChange}>Сохранить</Button>
            <Button variant="ghost" onClick={() => setIsStatusModalOpen(false)}>Отмена</Button>
          </div>
        </div>
      </Modal>
    </AdminLayout>
  );
};

export default AdminOrdersPage;
