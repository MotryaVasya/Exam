import React, { useState, useEffect } from 'react';
import { AdminLayout } from '../../components/layout';
import { adminService } from '../../services';
import LoadingSpinner from '../../components/ui/LoadingSpinner';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [revenueData, setRevenueData] = useState([]);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [statsData, revenueData] = await Promise.all([
          adminService.getStats(),
          adminService.getRevenueStats('week'),
        ]);
        setStats(statsData);
        setRevenueData(revenueData);
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="xl" />
        </div>
      </AdminLayout>
    );
  }

  const statCards = [
    {
      title: 'Пользователи',
      value: stats?.users?.total || 0,
      subtitle: `Активных: ${stats?.users?.active || 0}`,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ),
      color: 'bg-blue-500',
    },
    {
      title: 'Заказы',
      value: stats?.orders?.total || 0,
      subtitle: `Выручка: ${stats?.orders?.total_revenue?.toLocaleString() || 0} ₽`,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      ),
      color: 'bg-green-500',
    },
    {
      title: 'Товары',
      value: stats?.watches?.total_products || 0,
      subtitle: `В наличии: ${stats?.watches?.total_in_stock || 0}`,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
      ),
      color: 'bg-purple-500',
    },
    {
      title: 'Производители',
      value: stats?.producers?.total || 0,
      subtitle: 'Брендов в каталоге',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      color: 'bg-gold-500',
    },
  ];

  return (
    <AdminLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-2">
          Дашборд
        </h1>
        <p className="text-primary-600">
          Общая статистика магазина
        </p>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((card, index) => (
          <div
            key={index}
            className="bg-white rounded-xl p-6 shadow-sm border border-primary-100"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-14 h-14 ${card.color} rounded-xl flex items-center justify-center text-white`}>
                {card.icon}
              </div>
            </div>
            <h3 className="text-3xl font-bold text-primary-900 mb-1">
              {card.value.toLocaleString()}
            </h3>
            <p className="text-sm text-primary-600 mb-1">{card.title}</p>
            <p className="text-xs text-primary-500">{card.subtitle}</p>
          </div>
        ))}
      </div>

      {/* Дополнительная информация */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Средняя сумма заказа */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
          <h3 className="font-display font-semibold text-lg mb-4">
            Средняя сумма заказа
          </h3>
          <p className="text-4xl font-bold text-gold-600">
            {stats?.orders?.average_order_price?.toLocaleString('ru-RU') || 0} ₽
          </p>
          <p className="text-sm text-primary-500 mt-2">
            Средний чек по всем заказам
          </p>
        </div>

        {/* Скидки */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
          <h3 className="font-display font-semibold text-lg mb-4">
            Активные скидки
          </h3>
          <p className="text-4xl font-bold text-primary-900">
            {stats?.discounts?.total || 0}
          </p>
          <p className="text-sm text-primary-500 mt-2">
            Промокодов доступно
          </p>
        </div>
      </div>

      {/* Быстрые действия */}
      <div className="mt-8 bg-white rounded-xl p-6 shadow-sm border border-primary-100">
        <h3 className="font-display font-semibold text-lg mb-4">
          Быстрые действия
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <a
            href="/admin/watches"
            className="flex flex-col items-center justify-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <svg className="w-8 h-8 text-primary-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="text-sm font-medium text-primary-700">Добавить товар</span>
          </a>
          <a
            href="/admin/orders"
            className="flex flex-col items-center justify-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <svg className="w-8 h-8 text-primary-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <span className="text-sm font-medium text-primary-700">Заказы</span>
          </a>
          <a
            href="/admin/users"
            className="flex flex-col items-center justify-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <svg className="w-8 h-8 text-primary-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span className="text-sm font-medium text-primary-700">Пользователи</span>
          </a>
          <a
            href="/admin/discounts"
            className="flex flex-col items-center justify-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <svg className="w-8 h-8 text-primary-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span className="text-sm font-medium text-primary-700">Скидки</span>
          </a>
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminDashboard;
