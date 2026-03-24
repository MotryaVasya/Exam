import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [compareItems, setCompareItems] = useState([]);

  // Загрузка из localStorage при монтировании
  useEffect(() => {
    const savedCart = localStorage.getItem('cart');
    const savedCompare = localStorage.getItem('compare');
    
    if (savedCart) {
      setCartItems(JSON.parse(savedCart));
    }
    if (savedCompare) {
      setCompareItems(JSON.parse(savedCompare));
    }
  }, []);

  // Сохранение в localStorage при изменении
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cartItems));
  }, [cartItems]);

  useEffect(() => {
    localStorage.setItem('compare', JSON.stringify(compareItems));
  }, [compareItems]);

  // Добавление в корзину
  const addToCart = (watch, quantity = 1) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === watch.id);
      if (existing) {
        return prev.map(item =>
          item.id === watch.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...prev, { ...watch, quantity }];
    });
  };

  // Удаление из корзины
  const removeFromCart = (watchId) => {
    setCartItems(prev => prev.filter(item => item.id !== watchId));
  };

  // Обновление количества
  const updateQuantity = (watchId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(watchId);
      return;
    }
    setCartItems(prev =>
      prev.map(item =>
        item.id === watchId ? { ...item, quantity } : item
      )
    );
  };

  // Очистка корзины
  const clearCart = () => {
    setCartItems([]);
  };

  // Общее количество товаров
  const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  // Общая сумма
  const totalPrice = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  // Добавление в сравнение
  const addToCompare = (watch) => {
    setCompareItems(prev => {
      if (prev.find(item => item.id === watch.id)) {
        return prev;
      }
      if (prev.length >= 3) {
        alert('Можно сравнивать максимум 3 товара');
        return prev;
      }
      return [...prev, watch];
    });
  };

  // Удаление из сравнения
  const removeFromCompare = (watchId) => {
    setCompareItems(prev => prev.filter(item => item.id !== watchId));
  };

  // Очистка сравнения
  const clearCompare = () => {
    setCompareItems([]);
  };

  const value = {
    cartItems,
    compareItems,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    addToCompare,
    removeFromCompare,
    clearCompare,
    totalItems,
    totalPrice,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart должен использоваться внутри CartProvider');
  }
  return context;
};
