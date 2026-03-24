import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-primary-900 text-white mt-auto">
      <div className="container-custom py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* О компании */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gold-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-display font-bold text-xl">W</span>
              </div>
              <div>
                <h3 className="text-lg font-display font-bold">WatchWay</h3>
                <p className="text-xs text-primary-400 -mt-1">Премиум часы</p>
              </div>
            </div>
            <p className="text-primary-400 text-sm">
              Лучшие часы от ведущих мировых производителей. Качество, стиль и надежность в каждом изделии.
            </p>
          </div>

          {/* Навигация */}
          <div>
            <h4 className="font-display font-semibold mb-4">Навигация</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-primary-400 hover:text-white transition-colors">
                  Главная
                </Link>
              </li>
              <li>
                <Link to="/catalog" className="text-primary-400 hover:text-white transition-colors">
                  Каталог
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-primary-400 hover:text-white transition-colors">
                  О нас
                </Link>
              </li>
              <li>
                <Link to="/contacts" className="text-primary-400 hover:text-white transition-colors">
                  Контакты
                </Link>
              </li>
            </ul>
          </div>

          {/* Покупателям */}
          <div>
            <h4 className="font-display font-semibold mb-4">Покупателям</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/catalog?gender=male" className="text-primary-400 hover:text-white transition-colors">
                  Мужские часы
                </Link>
              </li>
              <li>
                <Link to="/catalog?gender=female" className="text-primary-400 hover:text-white transition-colors">
                  Женские часы
                </Link>
              </li>
              <li>
                <Link to="/catalog?type=mechanical" className="text-primary-400 hover:text-white transition-colors">
                  Механические
                </Link>
              </li>
              <li>
                <Link to="/catalog?type=electronical" className="text-primary-400 hover:text-white transition-colors">
                  Электронные
                </Link>
              </li>
            </ul>
          </div>

          {/* Контакты */}
          <div>
            <h4 className="font-display font-semibold mb-4">Контакты</h4>
            <ul className="space-y-2 text-sm text-primary-400">
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                +7 (999) 123-45-67
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                info@watchway.ru
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Москва, ул. Примерная, 10
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-primary-800 mt-8 pt-8 text-center text-sm text-primary-400">
          <p>&copy; {currentYear} WatchWay. Все права защищены.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
