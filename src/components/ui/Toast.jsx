import React from 'react';
import { ToastContainer, toast as toastify } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ToastWrapper = () => {
  return (
    <ToastContainer
      position="top-right"
      autoClose={3000}
      hideProgressBar={false}
      newestOnTop
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="light"
      className="font-sans"
    />
  );
};

export const toast = {
  success: (message) => toastify.success(message, {
    icon: '✓',
    style: { background: '#10b981', color: '#fff' },
  }),
  error: (message) => toastify.error(message, {
    icon: '✕',
    style: { background: '#ef4444', color: '#fff' },
  }),
  warning: (message) => toastify.warning(message, {
    icon: '⚠',
    style: { background: '#f59e0b', color: '#fff' },
  }),
  info: (message) => toastify.info(message, {
    icon: 'ℹ',
    style: { background: '#3b82f6', color: '#fff' },
  }),
};

export default ToastWrapper;
