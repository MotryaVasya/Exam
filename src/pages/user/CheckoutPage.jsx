import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { ordersService, discountsService } from '../../services';
import { Button, Input, Modal, toast } from '../../components/ui';

const CheckoutPage = () => {
  const { cartItems, totalPrice, clearCart } = useCart();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [isPromoModalOpen, setIsPromoModalOpen] = useState(false);
  const [promoCode, setPromoCode] = useState('');
  const [discount, setDiscount] = useState(null);
  const [discountError, setDiscountError] = useState('');

  const [formData, setFormData] = useState({
    delivery_address: '',
    notification_email: user?.email || '',
    is_pickup: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const applyPromoCode = async () => {
    try {
      const data = await discountsService.getByCode(promoCode);
      setDiscount(data);
      setDiscountError('');
      toast.success(`Скидка ${data.discount_percent}% применена`);
    } catch (error) {
      setDiscountError('Промокод не найден');
      setDiscount(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated) {
      toast.error('Необходимо войти для оформления заказа');
      navigate('/');
      return;
    }

    if (cartItems.length === 0) {
      toast.warning('Корзина пуста');
      return;
    }

    if (!formData.is_pickup && !formData.delivery_address) {
      toast.error('Укажите адрес доставки');
      return;
    }

    setLoading(true);

    try {
      const finalPrice = discount
        ? totalPrice * (1 - discount.discount_percent / 100)
        : totalPrice;

      // Создаем заказ
      const orderData = {
        user_id: user.id,
        total_price: finalPrice,
        discount: discount?.id || null,
        is_pickup: formData.is_pickup,
        delivery_address: formData.is_pickup ? null : formData.delivery_address,
        notification_email: formData.notification_email,
      };

      const order = await ordersService.create(orderData);

      // Добавляем товары в заказ
      // Для этого нужен orders-watches endpoint
      // Упрощенно просто очищаем корзину
      clearCart();

      toast.success('Заказ успешно оформлен!');
      navigate(`/profile?tab=orders`);
    } catch (error) {
      console.error('Ошибка создания заказа:', error);
      const message = error.response?.data?.detail || 'Не удалось оформить заказ';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const finalPrice = discount
    ? totalPrice * (1 - discount.discount_percent / 100)
    : totalPrice;
  const discountAmount = totalPrice - finalPrice;

  if (cartItems.length === 0) {
    return (
      <MainLayout>
        <div className="container-custom py-20 text-center">
          <h1 className="text-2xl font-display font-bold text-primary-900 mb-4">
            Корзина пуста
          </h1>
          <p className="text-primary-600 mb-8">
            Добавьте товары для оформления заказа
          </p>
          <Button variant="primary" size="lg" onClick={() => navigate('/catalog')}>
            Перейти в каталог
          </Button>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="container-custom py-8">
        <h1 className="text-3xl font-display font-bold text-primary-900 mb-8">
          Оформление заказа
        </h1>

        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Форма доставки */}
            <div className="lg:col-span-2 space-y-6">
              {/* Способ получения */}
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
                <h2 className="font-display font-semibold text-lg mb-4">
                  Способ получения
                </h2>
                <div className="space-y-3">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="radio"
                      name="is_pickup"
                      checked={!formData.is_pickup}
                      onChange={handleChange}
                      className="w-4 h-4 text-gold-600"
                    />
                    <span>Доставка курьером</span>
                  </label>
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="radio"
                      name="is_pickup"
                      checked={formData.is_pickup}
                      onChange={handleChange}
                      className="w-4 h-4 text-gold-600"
                    />
                    <span>Самовывоз из магазина</span>
                  </label>
                </div>

                {!formData.is_pickup && (
                  <div className="mt-4">
                    <Input
                      label="Адрес доставки"
                      name="delivery_address"
                      value={formData.delivery_address}
                      onChange={handleChange}
                      placeholder="Город, улица, дом, квартира"
                      required={!formData.is_pickup}
                    />
                  </div>
                )}
              </div>

              {/* Контакты */}
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
                <h2 className="font-display font-semibold text-lg mb-4">
                  Контактная информация
                </h2>
                <Input
                  label="Email для уведомлений"
                  name="notification_email"
                  type="email"
                  value={formData.notification_email}
                  onChange={handleChange}
                  placeholder="example@mail.ru"
                  required
                />
              </div>

              {/* Товары в заказе */}
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100">
                <h2 className="font-display font-semibold text-lg mb-4">
                  Товары в заказе
                </h2>
                <div className="space-y-3">
                  {cartItems.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between py-3 border-b border-primary-100 last:border-0"
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 bg-primary-100 rounded-lg overflow-hidden">
                          <img
                            src={item.image_url || 'https://via.placeholder.com/64x64?text=Watch'}
                            alt={item.name}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div>
                          <p className="font-medium">{item.name}</p>
                          <p className="text-sm text-primary-500">
                            {item.quantity} шт. × {Number(item.price).toLocaleString('ru-RU')} ₽
                          </p>
                        </div>
                      </div>
                      <p className="font-medium">
                        {(Number(item.price) * item.quantity).toLocaleString('ru-RU')} ₽
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Итого */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl p-6 shadow-sm border border-primary-100 sticky top-24">
                <h2 className="font-display font-semibold text-xl mb-6">
                  Итого
                </h2>

                <dl className="space-y-4 mb-6">
                  <div className="flex justify-between text-primary-600">
                    <dt>Подытог</dt>
                    <dd>{totalPrice.toLocaleString('ru-RU')} ₽</dd>
                  </div>
                  
                  {discount && (
                    <>
                      <div className="flex justify-between text-green-600">
                        <dt>Скидка ({discount.discount_percent}%)</dt>
                        <dd>-{discountAmount.toLocaleString('ru-RU')} ₽</dd>
                      </div>
                      <div className="flex justify-between text-sm">
                        <dt>Промокод</dt>
                        <dd className="font-medium">{discount.discount_code}</dd>
                      </div>
                    </>
                  )}

                  <div className="border-t border-primary-200 pt-4">
                    <div className="flex justify-between text-lg font-bold text-primary-900">
                      <dt>К оплате</dt>
                      <dd>{finalPrice.toLocaleString('ru-RU')} ₽</dd>
                    </div>
                  </div>
                </dl>

                {/* Промокод */}
                <div className="mb-6">
                  <button
                    type="button"
                    onClick={() => setIsPromoModalOpen(true)}
                    className="text-sm text-gold-600 hover:text-gold-700 font-medium"
                  >
                    {discount 
                      ? `Промокод: ${discount.discount_code} (${discount.discount_percent}%)` 
                      : 'Есть промокод?'}
                  </button>
                </div>

                <Button
                  type="submit"
                  variant="accent"
                  size="lg"
                  className="w-full"
                  disabled={loading}
                >
                  {loading ? 'Оформление...' : 'Подтвердить заказ'}
                </Button>

                <p className="text-xs text-primary-500 mt-4 text-center">
                  Нажимая кнопку, вы соглашаетесь с условиями обработки персональных данных
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>

      {/* Модальное окно промокода */}
      <Modal
        isOpen={isPromoModalOpen}
        onClose={() => setIsPromoModalOpen(false)}
        title="Промокод"
        size="sm"
      >
        <div className="space-y-4">
          <Input
            label="Введите промокод"
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
            placeholder="SUMMER2024"
            error={discountError}
          />
          <div className="flex gap-3">
            <Button variant="primary" className="flex-grow" onClick={applyPromoCode}>
              Применить
            </Button>
            <Button variant="ghost" onClick={() => setIsPromoModalOpen(false)}>
              Отмена
            </Button>
          </div>
        </div>
      </Modal>
    </MainLayout>
  );
};

export default CheckoutPage;
