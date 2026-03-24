import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { adminService } from '../../services';
import { Table, Pagination, Badge, Button, toast } from '../../components/ui';

const AdminLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  useEffect(() => {
    loadLogs();
  }, [currentPage]);

  const loadLogs = async () => {
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await adminService.getLogs({ skip, limit: itemsPerPage });
      setLogs(data);
    } catch (error) {
      toast.error('Ошибка загрузки логов');
    }
  };

  const getActionBadge = (action) => {
    const map = {
      CREATE: 'success',
      UPDATE: 'info',
      DELETE: 'danger',
      LOGIN: 'default',
    };
    return <Badge variant={map[action] || 'default'}>{action}</Badge>;
  };

  const handleCleanup = async () => {
    if (!window.confirm('Удалить логи старше 30 дней?')) return;
    try {
      await adminService.cleanupLogs(30);
      toast.success('Логи очищены');
      loadLogs();
    } catch (error) {
      toast.error('Ошибка при очистке');
    }
  };

  const columns = [
    { header: 'ID', accessor: 'id', width: '60px' },
    { header: 'Админ', accessor: 'admin_id', render: (v) => v || '—' },
    { header: 'Действие', accessor: 'action', render: (v) => getActionBadge(v) },
    { header: 'Сущность', accessor: 'entity' },
    { header: 'ID сущности', accessor: 'entity_id', render: (v) => v || '—' },
    { header: 'Описание', accessor: 'description', render: (v) => v || '—' },
    { header: 'Дата', accessor: 'created_at', render: (v) => new Date(v).toLocaleString('ru-RU') },
  ];

  return (
    <AdminLayout>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">Логи действий</h1>
          <p className="text-primary-600">История действий администраторов</p>
        </div>
        <Button variant="danger" onClick={handleCleanup}>Очистить старые логи</Button>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <Table columns={columns} data={logs} />
        <Pagination currentPage={currentPage} totalPages={Math.ceil(logs.length / itemsPerPage) || 1} onPageChange={setCurrentPage} />
      </div>
    </AdminLayout>
  );
};

export default AdminLogsPage;
