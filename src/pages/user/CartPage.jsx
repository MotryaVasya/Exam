import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { useCart } from '../../context/CartContext';
import { Button, toast } from '../../components/ui';

const CartPage = () => {
  const { cartItems, removeFromCart, updateQuantity, totalPrice, clearCart } = useCart();
  const navigate = useNavigate();

  const handleCheckout = () => {
    if (cartItems.length === 0) {
      toast.warning('Корзина пуста');
      return;
    }
    navigate('/checkout');
  };

  if (cartItems.length === 0) {
    return (
      <MainLayout>
        <div className="container-custom py-20 text-center">
          <svg className="w-24 h-24 mx-auto text-primary-300 mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h1 className="text-2xl font-display font-bold text-primary-900 mb-4">
            Корзина пуста
          </h1>
          <p className="text-primary-600 mb-8">
            Добавьте товары из каталога
          </p>
          <Link to="/catalog">
            <Button variant="primary" size="lg">
              Перейти в каталог
            </Button>
          </Link>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="container-custom py-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-8">
          Корзина
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Товары */}
          <div className="lg:col-span-2 space-y-4">
            {cartItems.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-xl p-6 shadow-sm border border-primary-100 flex gap-6"
              >
                {/* Изображение */}
                <Link to={`/catalog/${item.id}`} className="flex-shrink-0">
                  <div className="w-24 h-24 bg-primary-100 rounded-lg overflow-hidden">
                    <img
                      src={item.image_url || 'https://via.placeholder.com/100x100?text=Watch'}
                      alt={item.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/100x100?text=Watch';
                      }}
                    />
                  </div>
                </Link>

                {/* Информация */}
                <div className="flex-grow">
                  <Link to={`/catalog/${item.id}`}>
                    <h3 className="font-display font-semibold text-lg text-primary-900 hover:text-gold-600 transition-colors">
                      {item.name}
                    </h3>
                  </Link>
                  <p className="text-sm text-primary-500 mt-1">
                    {item.type === 'mechanical' ? 'Механические' : 
                     item.type === 'electronical' ? 'Электронные' : 'Гибридные'}
                  </p>

                  <div className="flex items-center justify-between mt-4">
                    {/* Количество */}
                    <div className="flex items-center border border-primary-300 rounded-lg">
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="px-3 py-1 hover:bg-primary-100 transition-colors"
                      >
                        -
                      </button>
                      <span className="px-4 py-1 border-x border-primary-300">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="px-3 py-1 hover:bg-primary-100 transition-colors"
                        disabled={item.quantity >= item.count}
                      >
                        +
                      </button>
                    </div>

                    {/* Цена */}
                    <div className="text-right">
                      <p className="text-lg font-bold text-primary-900">
                        {(Number(item.price) * item.quantity).toLocaleString('ru-RU')} ₽
                      </p>
                      <p className="text-sm text-primary-500">
                        {Number(item.price).toLocaleString('ru-RU')} ₽/шт.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Удалить */}
                <button
                  onClick={() => removeFromCart(item.id)}
                  className="text-primary-400 hover:text-red-500 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            ))}
          </div>

          {/* Итого */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100 sticky top-24">
              <h2 className="font-display font-semibold text-xl mb-6">
                Итого
              </h2>

              <dl className="space-y-4 mb-6">
                <div className="flex justify-between text-primary-600">
                  <dt>Товары</dt>
                  <dd>{cartItems.reduce((sum, item) => sum + item.quantity, 0)} шт.</dd>
                </div>
                <div className="flex justify-between text-primary-600">
                  <dt>Подытог</dt>
                  <dd>{totalPrice.toLocaleString('ru-RU')} ₽</dd>
                </div>
                <div className="border-t border-primary-200 pt-4">
                  <div className="flex justify-between text-lg font-bold text-primary-900">
                    <dt>Итого</dt>
                    <dd>{totalPrice.toLocaleString('ru-RU')} ₽</dd>
                  </div>
                </div>
              </dl>

              <div className="space-y-3">
                <Button
                  variant="accent"
                  size="lg"
                  className="w-full"
                  onClick={handleCheckout}
                >
                  Оформить заказ
                </Button>
                <Button
                  variant="ghost"
                  size="md"
                  className="w-full"
                  onClick={clearCart}
                >
                  Очистить корзину
                </Button>
              </div>

              <p className="text-xs text-primary-500 mt-4 text-center">
                Доставка рассчитывается после оформления
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default CartPage;
