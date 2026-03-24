import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { discountsService } from '../../services';
import { Button, Input, Table, Modal, toast } from '../../components/ui';

const AdminDiscountsPage = () => {
  const [discounts, setDiscounts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDiscount, setEditingDiscount] = useState(null);
  const [formData, setFormData] = useState({ discount_code: '', discount_percent: '' });

  useEffect(() => {
    loadDiscounts();
  }, []);

  const loadDiscounts = async () => {
    try {
      const data = await discountsService.getAll(0, 100);
      setDiscounts(data);
    } catch (error) {
      toast.error('Ошибка загрузки');
    }
  };

  const openModal = (discount = null) => {
    if (discount) {
      setEditingDiscount(discount);
      setFormData({ discount_code: discount.discount_code || '', discount_percent: discount.discount_percent || '' });
    } else {
      setEditingDiscount(null);
      setFormData({ discount_code: '', discount_percent: '' });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = { ...formData, discount_percent: parseInt(formData.discount_percent) };
      if (editingDiscount) {
        await discountsService.update(editingDiscount.id, data);
        toast.success('Скидка обновлена');
      } else {
        await discountsService.create(data);
        toast.success('Скидка создана');
      }
      setIsModalOpen(false);
      loadDiscounts();
    } catch (error) {
      toast.error('Ошибка при сохранении');
    }
  };

  const handleDelete = async (discount) => {
    if (!window.confirm('Вы уверены?')) return;
    try {
      await discountsService.delete(discount.id);
      toast.success('Скидка удалена');
      loadDiscounts();
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const columns = [
    { header: 'ID', accessor: 'id', width: '60px' },
    { header: 'Код', accessor: 'discount_code' },
    { header: 'Процент', accessor: 'discount_percent', render: (v) => `${v}%` },
    {
      header: 'Действия',
      accessor: 'actions',
      render: (_, row) => (
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => openModal(row)}>Ред.</Button>
          <Button variant="ghost" size="sm" onClick={() => handleDelete(row)} className="text-red-600">Удал.</Button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">Скидки</h1>
          <p className="text-primary-600">Промокоды и скидки</p>
        </div>
        <Button variant="primary" onClick={() => openModal()}>Добавить скидку</Button>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <Table columns={columns} data={discounts} />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingDiscount ? 'Редактировать скидку' : 'Новая скидка'} size="sm">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Код промокода" value={formData.discount_code} onChange={e => setFormData({...formData, discount_code: e.target.value.toUpperCase()})} required />
          <Input label="Процент скидки" type="number" min="1" max="100" value={formData.discount_percent} onChange={e => setFormData({...formData, discount_percent: e.target.value})} required />
          <div className="flex gap-3 pt-4">
            <Button type="submit" variant="primary">{editingDiscount ? 'Сохранить' : 'Создать'}</Button>
            <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>Отмена</Button>
          </div>
        </form>
      </Modal>
    </AdminLayout>
  );
};

export default AdminDiscountsPage;
