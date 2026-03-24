import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MainLayout } from '../../components/layout';
import { watchesService, producersService } from '../../services';
import WatchCard from '../../components/user/WatchCard';
import { Button, LoadingSpinner } from '../../components/ui';

const HomePage = () => {
  const [featuredWatches, setFeaturedWatches] = useState([]);
  const [producers, setProducers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [watchesRes, producersRes] = await Promise.all([
          watchesService.getAll({ limit: 8 }),
          producersService.getAll(0, 10),
        ]);
        setFeaturedWatches(watchesRes);
        setProducers(producersRes);
      } catch (error) {
        console.error('Ошибка загрузки:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <MainLayout>
        <div className="min-h-screen flex items-center justify-center">
          <LoadingSpinner size="xl" />
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      {/* Hero секция */}
      <section className="relative bg-primary-900 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <img
            src="https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?w=1920&h=600&fit=crop"
            alt="Background"
            className="w-full h-full object-cover"
          />
        </div>
        <div className="container-custom relative py-24 md:py-32">
          <div className="max-w-2xl">
            <h1 className="text-4xl md:text-6xl font-display font-bold mb-6">
              Время — это роскошь
            </h1>
            <p className="text-lg md:text-xl text-primary-300 mb-8">
              Откройте для себя коллекцию премиальных часов от ведущих мировых производителей
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/catalog">
                <Button variant="accent" size="lg">
                  Смотреть каталог
                </Button>
              </Link>
              <Link to="/about">
                <Button variant="secondary" size="lg" className="border-white text-white hover:bg-white hover:text-primary-900">
                  О бренде
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Популярные товары */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-primary-900 mb-4">
              Популярные модели
            </h2>
            <p className="text-primary-600 max-w-2xl mx-auto">
              Выберите идеальные часы из нашей коллекции премиальных моделей
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredWatches.map((watch) => (
              <WatchCard key={watch.id} watch={watch} />
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/catalog">
              <Button variant="secondary" size="lg">
                Смотреть весь каталог
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Преимущества */}
      <section className="py-16 bg-primary-50">
        <div className="container-custom">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Гарантия качества</h3>
              <p className="text-primary-600 text-sm">Только оригинальные часы от официальных производителей</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Бесплатная доставка</h3>
              <p className="text-primary-600 text-sm">При заказе от 50 000 ₽ доставка за наш счет</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Возврат 30 дней</h3>
              <p className="text-primary-600 text-sm">Если часы не подойдут, вернем деньги без вопросов</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Поддержка 24/7</h3>
              <p className="text-primary-600 text-sm">Ответим на любые вопросы в любое время</p>
            </div>
          </div>
        </div>
      </section>

      {/* Производители */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-display font-bold text-primary-900 mb-4">
              Наши бренды
            </h2>
            <p className="text-primary-600">
              Работаем только с проверенными производителями
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            {producers.map((producer) => (
              <div
                key={producer.id}
                className="flex items-center justify-center p-6 bg-primary-50 rounded-xl hover:bg-primary-100 transition-colors"
              >
                <span className="font-display font-semibold text-primary-800 text-center">
                  {producer.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA секция */}
      <section className="py-16 bg-primary-900 text-white">
        <div className="container-custom text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold mb-4">
            Готовы найти свои идеальные часы?
          </h2>
          <p className="text-primary-300 mb-8 max-w-2xl mx-auto">
            Перейдите в каталог и выберите из более чем 100 моделей премиальных часов
          </p>
          <Link to="/catalog">
            <Button variant="accent" size="lg">
              Перейти в каталог
            </Button>
          </Link>
        </div>
      </section>
    </MainLayout>
  );
};

export default HomePage;
