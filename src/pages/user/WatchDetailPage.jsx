import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { watchesService, producersService } from '../../services';
import { useCart } from '../../context/CartContext';
import { Button, LoadingSpinner, toast } from '../../components/ui';

const WatchDetailPage = () => {
  const { watchId } = useParams();
  const { addToCart, addToCompare, compareItems } = useCart();
  const [watch, setWatch] = useState(null);
  const [producer, setProducer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    const loadData = async () => {
      try {
        const watchData = await watchesService.getById(watchId);
        setWatch(watchData);
        
        if (watchData.producer_id) {
          const producerData = await producersService.getById(watchData.producer_id);
          setProducer(producerData);
        }
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        toast.error('Не удалось загрузить товар');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [watchId]);

  if (loading) {
    return (
      <MainLayout>
        <div className="min-h-screen flex items-center justify-center">
          <LoadingSpinner size="xl" />
        </div>
      </MainLayout>
    );
  }

  if (!watch) {
    return (
      <MainLayout>
        <div className="container-custom py-20 text-center">
          <h1 className="text-2xl font-display font-bold text-primary-900 mb-4">
            Товар не найден
          </h1>
          <Link to="/catalog">
            <Button variant="primary">Вернуться в каталог</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }

  const isInCompare = compareItems.find(item => item.id === watch.id);

  const handleAddToCart = () => {
    if (watch.count === 0) {
      toast.warning('Товар отсутствует');
      return;
    }
    addToCart(watch, quantity);
    toast.success(`Добавлено ${quantity} шт. в корзину`);
  };

  const handleAddToCompare = () => {
    addToCompare(watch);
    toast.info('Добавлено к сравнению');
  };

  const imageUrl = watch.image_url || `https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&h=600&fit=crop`;

  return (
    <MainLayout>
      <div className="container-custom py-8">
        {/* Хлебные крошки */}
        <nav className="flex items-center gap-2 text-sm text-primary-600 mb-8">
          <Link to="/" className="hover:text-primary-900">Главная</Link>
          <span>/</span>
          <Link to="/catalog" className="hover:text-primary-900">Каталог</Link>
          <span>/</span>
          <span className="text-primary-900">{watch.name}</span>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Изображение */}
          <div>
            <div className="bg-primary-100 rounded-xl overflow-hidden aspect-square">
              <img
                src={imageUrl}
                alt={watch.name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/600x600?text=Watch';
                }}
              />
            </div>
          </div>

          {/* Информация */}
          <div>
            <p className="text-sm text-primary-500 uppercase tracking-wide mb-2">
              {producer?.name || 'Производитель'}
            </p>
            
            <h1 className="text-3xl md:text-4xl font-display font-bold text-primary-900 mb-4">
              {watch.name}
            </h1>

            <div className="text-3xl font-bold text-gold-600 mb-6">
              {Number(watch.price).toLocaleString('ru-RU')} ₽
            </div>

            {/* Наличие */}
            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg mb-6 ${
              watch.count > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              <span className={`w-2 h-2 rounded-full ${
                watch.count > 0 ? 'bg-green-500' : 'bg-red-500'
              }`} />
              {watch.count > 0 ? `В наличии: ${watch.count} шт.` : 'Нет в наличии'}
            </div>

            {/* Характеристики */}
            <div className="bg-primary-50 rounded-xl p-6 mb-8">
              <h2 className="font-display font-semibold text-lg mb-4">Характеристики</h2>
              <dl className="grid grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm text-primary-500">Тип</dt>
                  <dd className="font-medium">
                    {watch.type === 'mechanical' ? 'Механические' : 
                     watch.type === 'electronical' ? 'Электронные' : 'Гибридные'}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-primary-500">Пол</dt>
                  <dd className="font-medium">
                    {watch.gender === 'male' ? 'Мужские' : 
                     watch.gender === 'female' ? 'Женские' : 'Унисекс'}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-primary-500">Размер</dt>
                  <dd className="font-medium">{watch.size_milimetrs} мм</dd>
                </div>
                <div>
                  <dt className="text-sm text-primary-500">Водонепроницаемость</dt>
                  <dd className="font-medium">
                    {watch.is_whatertightness ? 'Есть' : 'Нет'}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-primary-500">Дата выпуска</dt>
                  <dd className="font-medium">
                    {new Date(watch.released_at).toLocaleDateString('ru-RU')}
                  </dd>
                </div>
              </dl>
            </div>

            {/* Количество и кнопки */}
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <label className="text-sm font-medium text-primary-700">
                  Количество:
                </label>
                <div className="flex items-center border border-primary-300 rounded-lg">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-4 py-2 hover:bg-primary-100 transition-colors"
                    disabled={quantity <= 1}
                  >
                    -
                  </button>
                  <span className="px-6 py-2 border-x border-primary-300">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(Math.min(watch.count, quantity + 1))}
                    className="px-4 py-2 hover:bg-primary-100 transition-colors"
                    disabled={quantity >= watch.count}
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="flex gap-4">
                <Button
                  variant="primary"
                  size="lg"
                  className="flex-grow"
                  onClick={handleAddToCart}
                  disabled={watch.count === 0}
                >
                  Добавить в корзину
                </Button>
                <Button
                  variant={isInCompare ? 'accent' : 'secondary'}
                  size="lg"
                  onClick={handleAddToCompare}
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                  </svg>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default WatchDetailPage;
