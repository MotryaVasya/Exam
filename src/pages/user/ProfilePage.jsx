import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { useAuth } from '../../context/AuthContext';
import { ordersService } from '../../services';
import { Button, Input, LoadingSpinner, Badge } from '../../components/ui';
import { toast } from '../../components/ui/Toast';

const ProfilePage = () => {
  const { user, isAuthenticated } = useAuth();
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get('tab') || 'profile');
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    father_name: '',
    email: '',
  });

  useEffect(() => {
    if (!isAuthenticated) return;
    
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        father_name: user.father_name || '',
        email: user.email || '',
      });
    }

    if (activeTab === 'orders') {
      loadOrders();
    }
  }, [activeTab, user, isAuthenticated]);

  const loadOrders = async () => {
    setLoading(true);
    try {
      const data = await ordersService.getMyOrders();
      setOrders(data);
    } catch (error) {
      console.error('Ошибка загрузки заказов:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    // Здесь будет API вызов для обновления профиля
    toast.success('Профиль обновлен (демо)');
    setEditing(false);
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      pending: { variant: 'warning', label: 'В обработке' },
      confirmed: { variant: 'info', label: 'Подтвержден' },
      shipped: { variant: 'purple', label: 'Отправлен' },
      delivered: { variant: 'success', label: 'Доставлен' },
      cancelled: { variant: 'danger', label: 'Отменен' },
    };
    const config = statusMap[status] || { variant: 'default', label: status };
    return <Badge variant={config.variant}>{config.label}</Badge>;
  };

  if (!isAuthenticated) {
    return (
      <MainLayout>
        <div className="container-custom py-20 text-center">
          <h1 className="text-2xl font-display font-bold text-primary-900 mb-4">
            Необходимо войти
          </h1>
          <p className="text-primary-600">
            Войдите в аккаунт для просмотра профиля
          </p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="container-custom py-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-8">
          Личный кабинет
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Боковое меню */}
          <aside className="lg:col-span-1">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
              <div className="text-center mb-6">
                <div className="w-20 h-20 bg-primary-200 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl font-bold text-primary-700">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
                <h3 className="font-display font-semibold text-lg">
                  {user?.first_name} {user?.last_name}
                </h3>
                <p className="text-sm text-primary-500">{user?.email}</p>
              </div>

              <nav className="space-y-2">
                <button
                  onClick={() => setActiveTab('profile')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'profile'
                      ? 'bg-gold-600 text-white'
                      : 'text-primary-600 hover:bg-primary-50'
                  }`}
                >
                  Профиль
                </button>
                <button
                  onClick={() => setActiveTab('orders')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeTab === 'orders'
                      ? 'bg-gold-600 text-white'
                      : 'text-primary-600 hover:bg-primary-50'
                  }`}
                >
                  Мои заказы
                </button>
              </nav>
            </div>
          </aside>

          {/* Контент */}
          <div className="lg:col-span-3">
            {activeTab === 'profile' && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="font-display font-semibold text-xl">
                    Профиль
                  </h2>
                  {!editing && (
                    <Button variant="secondary" size="sm" onClick={() => setEditing(true)}>
                      Редактировать
                    </Button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    label="Имя"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    disabled={!editing}
                  />
                  <Input
                    label="Фамилия"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    disabled={!editing}
                  />
                  <Input
                    label="Отчество"
                    name="father_name"
                    value={formData.father_name}
                    onChange={handleChange}
                    disabled={!editing}
                  />
                  <Input
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    disabled={!editing}
                  />
                </div>

                {editing && (
                  <div className="flex gap-4 mt-6">
                    <Button variant="primary" onClick={handleSave}>
                      Сохранить
                    </Button>
                    <Button variant="ghost" onClick={() => setEditing(false)}>
                      Отмена
                    </Button>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'orders' && (
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
                <h2 className="font-display font-semibold text-xl mb-6">
                  Мои заказы
                </h2>

                {loading ? (
                  <div className="py-12 text-center">
                    <LoadingSpinner size="lg" />
                  </div>
                ) : orders.length === 0 ? (
                  <div className="text-center py-12">
                    <svg className="w-16 h-16 mx-auto text-primary-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    <p className="text-primary-600">У вас пока нет заказов</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {orders.map((order) => (
                      <div
                        key={order.id}
                        className="border border-primary-200 rounded-xl p-4 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <p className="font-medium">Заказ №{order.id}</p>
                            <p className="text-sm text-primary-500">
                              {new Date(order.created_at).toLocaleDateString('ru-RU', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </p>
                          </div>
                          {getStatusBadge(order.status)}
                        </div>

                        <div className="flex items-center justify-between text-sm">
                          <div className="text-primary-600">
                            <p>
                              {order.is_pickup ? 'Самовывоз' : `Доставка: ${order.delivery_address}`}
                            </p>
                            {order.notification_email && (
                              <p>Email: {order.notification_email}</p>
                            )}
                          </div>
                          <p className="text-lg font-bold text-primary-900">
                            {Number(order.total_price).toLocaleString('ru-RU')} ₽
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ProfilePage;
