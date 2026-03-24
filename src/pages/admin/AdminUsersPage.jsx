import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { adminService } from '../../services';
import { Button, Input, Table, Pagination, Modal, Badge, toast } from '../../components/ui';

const AdminUsersPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);

  const itemsPerPage = 10;

  useEffect(() => {
    loadUsers();
  }, [currentPage, search]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await adminService.getUsers({ skip, limit: itemsPerPage, search });
      setUsers(data);
    } catch (error) {
      toast.error('Ошибка загрузки пользователей');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      if (userToDelete) {
        await adminService.deleteUser(userToDelete.id);
        toast.success('Пользователь удален');
        loadUsers();
      }
      setIsDeleteModalOpen(false);
      setUserToDelete(null);
    } catch (error) {
      toast.error('Ошибка при удалении');
    }
  };

  const handleStatusChange = async (user, newStatus) => {
    try {
      await adminService.updateUserStatus(user.id, newStatus);
      toast.success(`Пользователь ${newStatus ? 'активирован' : 'деактивирован'}`);
      loadUsers();
    } catch (error) {
      toast.error('Ошибка при изменении статуса');
    }
  };

  const columns = [
    {
      header: 'ID',
      accessor: 'id',
      width: '80px',
    },
    {
      header: 'Пользователь',
      accessor: 'name',
      render: (_, row) => (
        <div>
          <p className="font-medium">{row.first_name} {row.last_name}</p>
          <p className="text-sm text-primary-500">{row.email}</p>
        </div>
      ),
    },
    {
      header: 'Роль',
      accessor: 'is_admin',
      render: (value) => (
        <Badge variant={value ? 'purple' : 'default'}>
          {value ? 'Админ' : 'Пользователь'}
        </Badge>
      ),
    },
    {
      header: 'Статус',
      accessor: 'is_active',
      render: (value) => (
        <Badge variant={value ? 'success' : 'danger'}>
          {value ? 'Активен' : 'Неактивен'}
        </Badge>
      ),
    },
    {
      header: 'Действия',
      accessor: 'actions',
      render: (_, row) => (
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => handleStatusChange(row, !row.is_active)}
          >
            {row.is_active ? 'Деактивировать' : 'Активировать'}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setUserToDelete(row);
              setIsDeleteModalOpen(true);
            }}
            className="text-red-600 hover:text-red-700"
          >
            Удалить
          </Button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">
          Пользователи
        </h1>
        <p className="text-primary-600">Управление пользователями системы</p>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <div className="flex items-center justify-between mb-6">
          <Input
            placeholder="Поиск по имени или email"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-md"
          />
        </div>

        <Table columns={columns} data={users} />

        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(totalItems / itemsPerPage) || 1}
          onPageChange={setCurrentPage}
          totalItems={totalItems}
          itemsPerPage={itemsPerPage}
        />
      </div>

      <Modal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setUserToDelete(null);
        }}
        title="Удаление пользователя"
        size="sm"
      >
        <p className="mb-6">
          Вы уверены, что хотите удалить пользователя {userToDelete?.first_name} {userToDelete?.last_name}?
        </p>
        <div className="flex gap-3">
          <Button variant="danger" onClick={handleDelete}>
            Удалить
          </Button>
          <Button variant="ghost" onClick={() => setIsDeleteModalOpen(false)}>
            Отмена
          </Button>
        </div>
      </Modal>
    </AdminLayout>
  );
};

export default AdminUsersPage;
