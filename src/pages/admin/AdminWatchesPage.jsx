import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { watchesService, producersService } from '../../services';
import { Button, Input, Select, Table, Pagination, Modal, Badge, toast } from '../../components/ui';

const AdminWatchesPage = () => {
  const [watches, setWatches] = useState([]);
  const [producers, setProducers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingWatch, setEditingWatch] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    producer_id: '',
    is_whatertightness: false,
    released_at: '',
    size_milimetrs: '',
    type: 'mechanical',
    count: '',
    gender: 'unisex',
    price: '',
    image_url: '',
  });

  const itemsPerPage = 10;

  useEffect(() => {
    loadData();
  }, [currentPage]);

  const loadData = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const [watchesData, producersData] = await Promise.all([
        watchesService.getAllAdmin({ skip, limit: itemsPerPage }),
        producersService.getAll(0, 100),
      ]);
      setWatches(watchesData);
      setProducers(producersData);
    } catch (error) {
      toast.error('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  const openModal = (watch = null) => {
    if (watch) {
      setEditingWatch(watch);
      setFormData({
        name: watch.name || '',
        producer_id: watch.producer_id || '',
        is_whatertightness: watch.is_whatertightness || false,
        released_at: watch.released_at ? new Date(watch.released_at).toISOString().split('T')[0] : '',
        size_milimetrs: watch.size_milimetrs || '',
        type: watch.type || 'mechanical',
        count: watch.count || '',
        gender: watch.gender || 'unisex',
        price: watch.price || '',
        image_url: watch.image_url || '',
      });
    } else {
      setEditingWatch(null);
      setFormData({
        name: '',
        producer_id: '',
        is_whatertightness: false,
        released_at: '',
        size_milimetrs: '',
        type: 'mechanical',
        count: '',
        gender: 'unisex',
        price: '',
        image_url: '',
      });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        producer_id: parseInt(formData.producer_id),
        is_whatertightness: formData.is_whatertightness,
        released_at: new Date(formData.released_at).toISOString(),
        size_milimetrs: parseInt(formData.size_milimetrs),
        count: parseInt(formData.count),
        price: parseFloat(formData.price),
      };

      if (editingWatch) {
        await watchesService.update(editingWatch.id, data);
        toast.success('Товар обновлен');
      } else {
        await watchesService.create(data);
        toast.success('Товар создан');
      }
      setIsModalOpen(false);
      loadData();
    } catch (error) {
      toast.error('Ошибка при сохранении');
    }
  };

  const handleDelete = async (watch) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот товар?')) return;
    try {
      await watchesService.delete(watch.id);
      toast.success('Товар удален');
      loadData();
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const columns = [
    { header: 'ID', accessor: 'id', width: '60px' },
    {
      header: 'Название',
      accessor: 'name',
      render: (_, row) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-100 rounded overflow-hidden">
            <img src={row.image_url || 'https://via.placeholder.com/40'} alt="" className="w-full h-full object-cover" />
          </div>
          <span className="font-medium">{row.name}</span>
        </div>
      ),
    },
    { header: 'Цена', accessor: 'price', render: (v) => `${Number(v).toLocaleString()} ₽` },
    { header: 'Остаток', accessor: 'count', render: (v) => <Badge variant={v > 0 ? 'success' : 'danger'}>{v} шт.</Badge> },
    {
      header: 'Тип',
      accessor: 'type',
      render: (v) => ({ electronical: 'Электронные', mechanical: 'Механические', hybrid: 'Гибридные' }[v] || v),
    },
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
          <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">Товары</h1>
          <p className="text-primary-600">Управление ассортиментом часов</p>
        </div>
        <Button variant="primary" onClick={() => openModal()}>Добавить товар</Button>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <Table columns={columns} data={watches} />
        <Pagination currentPage={currentPage} totalPages={Math.ceil(watches.length / itemsPerPage) || 1} onPageChange={setCurrentPage} />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingWatch ? 'Редактировать товар' : 'Новый товар'} size="lg">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Название" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required />
            <Select label="Производитель" value={formData.producer_id} onChange={e => setFormData({...formData, producer_id: e.target.value})} options={producers.map(p => ({ value: p.id, label: p.name }))} required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Цена (₽)" type="number" value={formData.price} onChange={e => setFormData({...formData, price: e.target.value})} required />
            <Input label="Количество" type="number" value={formData.count} onChange={e => setFormData({...formData, count: e.target.value})} required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Select label="Тип" value={formData.type} onChange={e => setFormData({...formData, type: e.target.value})} options={[{value:'mechanical',label:'Механические'},{value:'electronical',label:'Электронные'},{value:'hybrid',label:'Гибридные'}]} />
            <Select label="Пол" value={formData.gender} onChange={e => setFormData({...formData, gender: e.target.value})} options={[{value:'unisex',label:'Унисекс'},{value:'male',label:'Мужские'},{value:'female',label:'Женские'}]} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Размер (мм)" type="number" value={formData.size_milimetrs} onChange={e => setFormData({...formData, size_milimetrs: e.target.value})} required />
            <Input label="Дата выпуска" type="date" value={formData.released_at} onChange={e => setFormData({...formData, released_at: e.target.value})} required />
          </div>
          <Input label="URL изображения" value={formData.image_url} onChange={e => setFormData({...formData, image_url: e.target.value})} />
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={formData.is_whatertightness} onChange={e => setFormData({...formData, is_whatertightness: e.target.checked})} />
            <span>Водонепроницаемость</span>
          </label>
          <div className="flex gap-3 pt-4">
            <Button type="submit" variant="primary">{editingWatch ? 'Сохранить' : 'Создать'}</Button>
            <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>Отмена</Button>
          </div>
        </form>
      </Modal>
    </AdminLayout>
  );
};

export default AdminWatchesPage;
