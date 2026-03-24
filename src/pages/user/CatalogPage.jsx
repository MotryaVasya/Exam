import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { watchesService, producersService } from '../../services';
import WatchCard from '../../components/user/WatchCard';
import { Button, Input, Select, Pagination, LoadingSpinner } from '../../components/ui';

const CatalogPage = () => {
  const { watchId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const [watches, setWatches] = useState([]);
  const [producers, setProducers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalItems, setTotalItems] = useState(0);

  // Фильтры
  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    producer_id: searchParams.get('producer_id') || '',
    type: searchParams.get('type') || '',
    gender: searchParams.get('gender') || '',
    min_price: searchParams.get('min_price') || '',
    max_price: searchParams.get('max_price') || '',
  });

  // Пагинация
  const [currentPage, setCurrentPage] = useState(parseInt(searchParams.get('skip') || '0') / 12 + 1);
  const itemsPerPage = 12;

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const skip = (currentPage - 1) * itemsPerPage;
        const [watchesRes, producersRes] = await Promise.all([
          watchesService.getAll({ ...filters, skip, limit: itemsPerPage }),
          producersService.getAll(0, 100),
        ]);
        setWatches(watchesRes);
        setProducers(producersRes);
        setTotalItems(watchesRes.length); // Для простоты
      } catch (error) {
        console.error('Ошибка загрузки:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [currentPage, filters]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const applyFilters = () => {
    const params = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params[key] = value;
    });
    params.skip = (currentPage - 1) * itemsPerPage;
    params.limit = itemsPerPage;
    setSearchParams(params);
  };

  const clearFilters = () => {
    setFilters({
      search: '',
      producer_id: '',
      type: '',
      gender: '',
      min_price: '',
      max_price: '',
    });
    setCurrentPage(1);
    setSearchParams({});
  };

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  const typeOptions = [
    { value: '', label: 'Все типы' },
    { value: 'electronical', label: 'Электронные' },
    { value: 'mechanical', label: 'Механические' },
    { value: 'hybrid', label: 'Гибридные' },
  ];

  const genderOptions = [
    { value: '', label: 'Все' },
    { value: 'male', label: 'Мужские' },
    { value: 'female', label: 'Женские' },
    { value: 'unisex', label: 'Унисекс' },
  ];

  return (
    <MainLayout>
      <div className="bg-primary-50 py-8">
        <div className="container-custom">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-primary-900">
            Каталог часов
          </h1>
          <p className="text-primary-600 mt-2">
            Найдите свои идеальные часы
          </p>
        </div>
      </div>

      <div className="container-custom py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Фильтры */}
          <aside className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100 sticky top-24">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-display font-semibold text-lg">Фильтры</h2>
                <button
                  onClick={clearFilters}
                  className="text-sm text-primary-600 hover:text-primary-800"
                >
                  Сбросить
                </button>
              </div>

              <div className="space-y-4">
                <Input
                  label="Поиск"
                  placeholder="Название модели"
                  value={filters.search}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                />

                <Select
                  label="Производитель"
                  value={filters.producer_id}
                  onChange={(e) => handleFilterChange('producer_id', e.target.value)}
                  options={[
                    { value: '', label: 'Все производители' },
                    ...producers.map(p => ({ value: p.id, label: p.name })),
                  ]}
                />

                <Select
                  label="Тип"
                  value={filters.type}
                  onChange={(e) => handleFilterChange('type', e.target.value)}
                  options={typeOptions}
                />

                <Select
                  label="Пол"
                  value={filters.gender}
                  onChange={(e) => handleFilterChange('gender', e.target.value)}
                  options={genderOptions}
                />

                <div>
                  <label className="block text-sm font-medium text-primary-700 mb-1">
                    Цена от
                  </label>
                  <Input
                    type="number"
                    placeholder="0"
                    value={filters.min_price}
                    onChange={(e) => handleFilterChange('min_price', e.target.value)}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-primary-700 mb-1">
                    Цена до
                  </label>
                  <Input
                    type="number"
                    placeholder="1000000"
                    value={filters.max_price}
                    onChange={(e) => handleFilterChange('max_price', e.target.value)}
                  />
                </div>

                <Button 
                  variant="primary" 
                  className="w-full"
                  onClick={applyFilters}
                >
                  Применить
                </Button>
              </div>
            </div>
          </aside>

          {/* Товары */}
          <div className="flex-grow">
            {loading ? (
              <div className="flex items-center justify-center py-20">
                <LoadingSpinner size="xl" />
              </div>
            ) : watches.length === 0 ? (
              <div className="text-center py-20">
                <svg className="w-16 h-16 mx-auto text-primary-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <h3 className="text-xl font-display font-semibold text-primary-900 mb-2">
                  Ничего не найдено
                </h3>
                <p className="text-primary-600">
                  Попробуйте изменить параметры фильтрации
                </p>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between mb-6">
                  <p className="text-primary-600">
                    Найдено: {watches.length} товаров
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {watches.map((watch) => (
                    <WatchCard key={watch.id} watch={watch} />
                  ))}
                </div>

                <Pagination
                  currentPage={currentPage}
                  totalPages={Math.ceil(totalItems / itemsPerPage) || 1}
                  onPageChange={setCurrentPage}
                  totalItems={totalItems}
                  itemsPerPage={itemsPerPage}
                />
              </>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default CatalogPage;
