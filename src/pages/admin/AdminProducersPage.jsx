import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { producersService } from '../../services';
import { Button, Input, Table, Modal, toast } from '../../components/ui';

const AdminProducersPage = () => {
  const [producers, setProducers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProducer, setEditingProducer] = useState(null);
  const [formData, setFormData] = useState({ name: '' });

  useEffect(() => {
    loadProducers();
  }, []);

  const loadProducers = async () => {
    setLoading(true);
    try {
      const data = await producersService.getAll(0, 100);
      setProducers(data);
    } catch (error) {
      toast.error('Ошибка загрузки');
    } finally {
      setLoading(false);
    }
  };

  const openModal = (producer = null) => {
    if (producer) {
      setEditingProducer(producer);
      setFormData({ name: producer.name || '' });
    } else {
      setEditingProducer(null);
      setFormData({ name: '' });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingProducer) {
        await producersService.update(editingProducer.id, formData);
        toast.success('Производитель обновлен');
      } else {
        await producersService.create(formData);
        toast.success('Производитель создан');
      }
      setIsModalOpen(false);
      loadProducers();
    } catch (error) {
      toast.error('Ошибка при сохранении');
    }
  };

  const handleDelete = async (producer) => {
    if (!window.confirm('Вы уверены?')) return;
    try {
      await producersService.delete(producer.id);
      toast.success('Производитель удален');
      loadProducers();
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const columns = [
    { header: 'ID', accessor: 'id', width: '60px' },
    { header: 'Название', accessor: 'name' },
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
          <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">Производители</h1>
          <p className="text-primary-600">Управление брендами</p>
        </div>
        <Button variant="primary" onClick={() => openModal()}>Добавить</Button>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <Table columns={columns} data={producers} />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingProducer ? 'Редактировать' : 'Новый производитель'} size="sm">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Название" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required />
          <div className="flex gap-3 pt-4">
            <Button type="submit" variant="primary">{editingProducer ? 'Сохранить' : 'Создать'}</Button>
            <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>Отмена</Button>
          </div>
        </form>
      </Modal>
    </AdminLayout>
  );
};

export default AdminProducersPage;
