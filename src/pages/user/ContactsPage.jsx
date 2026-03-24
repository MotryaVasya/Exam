import React, { useState } from 'react';
import { MainLayout } from '../../components/layout';
import { Button, Input, toast } from '../../components/ui';

const ContactsPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Имитация отправки
    setTimeout(() => {
      toast.success('Сообщение отправлено! Мы свяжемся с вами в ближайшее время.');
      setFormData({ name: '', email: '', phone: '', message: '' });
      setLoading(false);
    }, 1000);
  };

  return (
    <MainLayout>
      {/* Hero */}
      <section className="bg-primary-900 text-white py-20">
        <div className="container-custom text-center">
          <h1 className="text-4xl md:text-5xl font-display font-bold mb-6">
            Контакты
          </h1>
          <p className="text-xl text-primary-300 max-w-3xl mx-auto">
            Свяжитесь с нами любым удобным способом
          </p>
        </div>
      </section>

      {/* Контактная информация и форма */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Информация */}
            <div>
              <h2 className="text-2xl font-display font-bold text-primary-900 mb-6">
                Контактная информация
              </h2>

              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gold-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-primary-900 mb-1">Адрес</h3>
                    <p className="text-primary-600">
                      г. Москва, ул. Примерная, д. 10, стр. 1<br />
                      Бизнес-центр "Премиум", офис 500
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gold-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-primary-900 mb-1">Телефон</h3>
                    <p className="text-primary-600">
                      <a href="tel:+79991234567" className="hover:text-gold-600 transition-colors">
                        +7 (999) 123-45-67
                      </a>
                    </p>
                    <p className="text-sm text-primary-500 mt-1">Пн-Пт: 9:00 - 20:00</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gold-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-primary-900 mb-1">Email</h3>
                    <p className="text-primary-600">
                      <a href="mailto:info@watchway.ru" className="hover:text-gold-600 transition-colors">
                        info@watchway.ru
                      </a>
                    </p>
                    <p className="text-sm text-primary-500 mt-1">Ответим в течение 24 часов</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gold-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-primary-900 mb-1">Режим работы</h3>
                    <p className="text-primary-600">
                      Пн-Пт: 9:00 - 20:00<br />
                      Сб-Вс: 10:00 - 18:00
                    </p>
                  </div>
                </div>
              </div>

              {/* Карта (заглушка) */}
              <div className="mt-8 bg-primary-100 rounded-xl overflow-hidden aspect-video">
                <img
                  src="https://images.unsplash.com/photo-1524661135-423995f22d0b?w=800&h=400&fit=crop"
                  alt="Карта"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* Форма обратной связи */}
            <div>
              <div className="bg-primary-50 rounded-xl p-8">
                <h2 className="text-2xl font-display font-bold text-primary-900 mb-6">
                  Напишите нам
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <Input
                    label="Ваше имя"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Иван Иванов"
                    required
                  />

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Input
                      label="Email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="example@mail.ru"
                      required
                    />

                    <Input
                      label="Телефон"
                      name="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder="+7 (___) ___-__-__"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-primary-700 mb-1">
                      Сообщение
                    </label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      rows={5}
                      className="w-full px-4 py-2.5 border border-primary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 resize-none"
                      placeholder="Ваш вопрос или пожелание..."
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    className="w-full"
                    disabled={loading}
                  >
                    {loading ? 'Отправка...' : 'Отправить сообщение'}
                  </Button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
    </MainLayout>
  );
};

export default ContactsPage;
