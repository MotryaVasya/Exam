import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import Button from '../ui/Button';
import { toast } from '../ui/Toast';

const WatchCard = ({ watch }) => {
  const { addToCart, addToCompare, compareItems } = useCart();

  const handleAddToCart = (e) => {
    e.preventDefault();
    if (watch.count === 0) {
      toast.warning('Товар отсутствует');
      return;
    }
    addToCart(watch);
    toast.success('Добавлено в корзину');
  };

  const handleAddToCompare = (e) => {
    e.preventDefault();
    addToCompare(watch);
    toast.info('Добавлено к сравнению');
  };

  const isInCompare = compareItems.find(item => item.id === watch.id);

  // Placeholder изображение если нет URL
  const imageUrl = watch.image_url || `https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop`;

  return (
    <div className="card group">
      {/* Изображение */}
      <Link to={`/catalog/${watch.id}`} className="block overflow-hidden">
        <div className="aspect-square bg-primary-100 relative overflow-hidden">
          <img
            src={imageUrl}
            alt={watch.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/400x400?text=Watch';
            }}
          />
          {watch.count === 0 && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <span className="text-white font-medium">Нет в наличии</span>
            </div>
          )}
        </div>
      </Link>

      {/* Контент */}
      <div className="p-4">
        {/* Производитель */}
        <p className="text-xs text-primary-500 uppercase tracking-wide mb-1">
          {watch.producer_name || 'Производитель'}
        </p>

        {/* Название */}
        <Link to={`/catalog/${watch.id}`}>
          <h3 className="font-display font-semibold text-lg text-primary-900 mb-2 hover:text-gold-600 transition-colors line-clamp-1">
            {watch.name}
          </h3>
        </Link>

        {/* Характеристики */}
        <div className="flex items-center gap-2 text-xs text-primary-500 mb-3">
          <span className="px-2 py-1 bg-primary-100 rounded">
            {watch.type === 'mechanical' ? 'Механические' : 
             watch.type === 'electronical' ? 'Электронные' : 'Гибридные'}
          </span>
          <span className="px-2 py-1 bg-primary-100 rounded">
            {watch.gender === 'male' ? 'Мужские' : 
             watch.gender === 'female' ? 'Женские' : 'Унисекс'}
          </span>
          <span className="px-2 py-1 bg-primary-100 rounded">
            {watch.size_milimetrs} мм
          </span>
        </div>

        {/* Цена и кнопки */}
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-primary-900">
            {Number(watch.price).toLocaleString('ru-RU')} ₽
          </span>
          
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleAddToCompare}
              className={`p-2 ${isInCompare ? 'text-gold-600' : ''}`}
              title="Сравнить"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
            </Button>
            
            <Button
              variant="primary"
              size="sm"
              onClick={handleAddToCart}
              disabled={watch.count === 0}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WatchCard;
