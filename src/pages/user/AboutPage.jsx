import React from 'react';
import { MainLayout } from '../../components/layout';
import { Button } from '../../components/ui';
import { Link } from 'react-router-dom';

const AboutPage = () => {
  return (
    <MainLayout>
      {/* Hero */}
      <section className="bg-primary-900 text-white py-20">
        <div className="container-custom text-center">
          <h1 className="text-4xl md:text-5xl font-display font-bold mb-6">
            О WatchWay
          </h1>
          <p className="text-xl text-primary-300 max-w-3xl mx-auto">
            Мы предлагаем лучшие часы от ведущих мировых производителей с 2010 года
          </p>
        </div>
      </section>

      {/* О компании */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-display font-bold text-primary-900 mb-6">
                Наша история
              </h2>
              <div className="space-y-4 text-primary-700">
                <p>
                  WatchWay была основана в 2010 году группой энтузиастов, влюбленных в часовое искусство. 
                  Мы начинали как небольшой бутик в центре Москвы, а сегодня являемся одним из крупнейших 
                  онлайн-ретейлеров премиальных часов в России.
                </p>
                <p>
                  За более чем 10 лет работы мы заработали репутацию надежного партнера, предлагающего 
                  только оригинальную продукцию от официальных производителей. Каждая модель в нашем 
                  каталоге проходит строгую проверку качества.
                </p>
                <p>
                  Мы сотрудничаем с ведущими часовыми домами Швейцарии, Японии и Германии, чтобы 
                  предложить нашим клиентам самый широкий выбор моделей — от классических механических 
                  часов до современных электронных моделей.
                </p>
              </div>
            </div>
            <div>
              <div className="aspect-square bg-primary-100 rounded-xl overflow-hidden">
                <img
                  src="https://images.unsplash.com/photo-1590736969955-71cc94901144?w=600&h=600&fit=crop"
                  alt="О магазине"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Ценности */}
      <section className="py-16 bg-primary-50">
        <div className="container-custom">
          <h2 className="text-3xl font-display font-bold text-center text-primary-900 mb-12">
            Наши ценности
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Качество</h3>
              <p className="text-primary-600">
                Только оригинальные часы с официальной гарантией производителя
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Забота</h3>
              <p className="text-primary-600">
                Индивидуальный подход к каждому клиенту и помощь в выборе
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gold-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-display font-semibold text-lg mb-2">Скорость</h3>
              <p className="text-primary-600">
                Быстрая доставка и оперативная обработка заказов
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Статистика */}
      <section className="py-16 bg-white">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <p className="text-4xl font-display font-bold text-gold-600 mb-2">10+</p>
              <p className="text-primary-600">Лет на рынке</p>
            </div>
            <div>
              <p className="text-4xl font-display font-bold text-gold-600 mb-2">500+</p>
              <p className="text-primary-600">Моделей часов</p>
            </div>
            <div>
              <p className="text-4xl font-display font-bold text-gold-600 mb-2">50+</p>
              <p className="text-primary-600">Брендов</p>
            </div>
            <div>
              <p className="text-4xl font-display font-bold text-gold-600 mb-2">10K+</p>
              <p className="text-primary-600">Довольных клиентов</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-primary-900 text-white">
        <div className="container-custom text-center">
          <h2 className="text-3xl font-display font-bold mb-4">
            Готовы найти свои идеальные часы?
          </h2>
          <p className="text-primary-300 mb-8">
            Перейдите в каталог и выберите из более чем 500 моделей
          </p>
          <Link to="/catalog">
            <Button variant="accent" size="lg">
              Смотреть каталог
            </Button>
          </Link>
        </div>
      </section>
    </MainLayout>
  );
};

export default AboutPage;
