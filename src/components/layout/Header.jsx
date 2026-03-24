import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import Button from '../ui/Button';
import AuthModal from '../modals/AuthModal';

const Header = () => {
  const { isAuthenticated, user, isAdmin, logout } = useAuth();
  const { totalItems } = useCart();
  const navigate = useNavigate();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsUserMenuOpen(false);
  };

  return (
    <>
      <header className="bg-white border-b border-primary-200 sticky top-0 z-40">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            {/* Логотип */}
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-display font-bold text-xl">W</span>
              </div>
              <div>
                <h1 className="text-xl font-display font-bold text-primary-900">WatchWay</h1>
                <p className="text-xs text-primary-500 -mt-1">Премиум часы</p>
              </div>
            </Link>

            {/* Навигация */}
            <nav className="hidden md:flex items-center gap-6">
              <Link to="/" className="text-primary-600 hover:text-primary-900 transition-colors">
                Главная
              </Link>
              <Link to="/catalog" className="text-primary-600 hover:text-primary-900 transition-colors">
                Каталог
              </Link>
              <Link to="/about" className="text-primary-600 hover:text-primary-900 transition-colors">
                О нас
              </Link>
              <Link to="/contacts" className="text-primary-600 hover:text-primary-900 transition-colors">
                Контакты
              </Link>
              {isAdmin && (
                <Link 
                  to="/admin" 
                  className="text-gold-600 hover:text-gold-700 font-medium transition-colors"
                >
                  Админ-панель
                </Link>
              )}
            </nav>

            {/* Правая часть */}
            <div className="flex items-center gap-4">
              {/* Корзина */}
              <Link to="/cart" className="relative p-2 text-primary-600 hover:text-primary-900 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-gold-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                    {totalItems}
                  </span>
                )}
              </Link>

              {/* Профиль */}
              {isAuthenticated ? (
                <div className="relative">
                  <button
                    onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                    className="flex items-center gap-2 p-2 text-primary-600 hover:text-primary-900 transition-colors"
                  >
                    <div className="w-8 h-8 bg-primary-200 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium">
                        {user?.first_name?.[0]}{user?.last_name?.[0]}
                      </span>
                    </div>
                  </button>

                  {isUserMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-primary-200 py-2">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-primary-700 hover:bg-primary-50"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        Профиль
                      </Link>
                      <Link
                        to="/profile?tab=orders"
                        className="block px-4 py-2 text-sm text-primary-700 hover:bg-primary-50"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        Мои заказы
                      </Link>
                      {isAdmin && (
                        <Link
                          to="/admin"
                          className="block px-4 py-2 text-sm text-gold-600 hover:bg-primary-50"
                          onClick={() => setIsUserMenuOpen(false)}
                        >
                          Админ-панель
                        </Link>
                      )}
                      <hr className="my-2" />
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-primary-50"
                      >
                        Выйти
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <Button 
                  variant="primary" 
                  size="sm"
                  onClick={() => setIsAuthModalOpen(true)}
                >
                  Войти
                </Button>
              )}
            </div>
          </div>
        </div>
      </header>

      <AuthModal 
        isOpen={isAuthModalOpen} 
        onClose={() => setIsAuthModalOpen(false)} 
      />
    </>
  );
};

export default Header;
