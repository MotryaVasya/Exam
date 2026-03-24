import React, { useState } from 'react';
import Modal from '../ui/Modal';
import Input from '../ui/Input';
import Button from '../ui/Button';
import { toast } from '../ui/Toast';
import { useAuth } from '../../context/AuthContext';

const AuthModal = ({ isOpen, onClose }) => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    father_name: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Введите email';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Некорректный email';
    }

    if (!formData.password) {
      newErrors.password = 'Введите пароль';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Пароль должен быть не менее 6 символов';
    }

    if (!isLoginMode) {
      if (!formData.first_name) {
        newErrors.first_name = 'Введите имя';
      }
      if (!formData.last_name) {
        newErrors.last_name = 'Введите фамилию';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);

    try {
      if (isLoginMode) {
        await login(formData.email, formData.password);
        toast.success('Вы успешно вошли!');
        onClose();
      } else {
        await register({
          email: formData.email,
          password: formData.password,
          first_name: formData.first_name,
          last_name: formData.last_name,
          father_name: formData.father_name || null,
        });
        toast.success('Регистрация успешна! Теперь войдите.');
        setIsLoginMode(true);
      }
      setFormData({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        father_name: '',
      });
    } catch (error) {
      const message = error.response?.data?.detail || 'Произошла ошибка';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isLoginMode ? 'Вход' : 'Регистрация'}
      size="md"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {!isLoginMode && (
          <>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Имя"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                error={errors.first_name}
                placeholder="Иван"
              />
              <Input
                label="Фамилия"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                error={errors.last_name}
                placeholder="Иванов"
              />
            </div>
            <Input
              label="Отчество (необязательно)"
              name="father_name"
              value={formData.father_name}
              onChange={handleChange}
              placeholder="Иванович"
            />
          </>
        )}

        <Input
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="example@mail.ru"
        />

        <Input
          label="Пароль"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="••••••••"
        />

        <Button 
          type="submit" 
          variant="primary" 
          className="w-full"
          disabled={loading}
        >
          {loading ? 'Загрузка...' : isLoginMode ? 'Войти' : 'Зарегистрироваться'}
        </Button>

        <div className="text-center">
          <button
            type="button"
            onClick={() => setIsLoginMode(!isLoginMode)}
            className="text-sm text-primary-600 hover:text-primary-800 transition-colors"
          >
            {isLoginMode 
              ? 'Нет аккаунта? Зарегистрироваться' 
              : 'Уже есть аккаунт? Войти'}
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default AuthModal;
