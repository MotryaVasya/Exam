import React from 'react';

const Input = ({ 
  label, 
  error, 
  className = '', 
  type = 'text',
  id,
  ...props 
}) => {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
  
  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label 
          htmlFor={inputId} 
          className="block text-sm font-medium text-primary-700 mb-1"
        >
          {label}
        </label>
      )}
      <input
        type={type}
        id={inputId}
        className={`
          w-full px-4 py-2.5 border rounded-lg
          focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
          transition-all duration-200
          ${error ? 'border-red-500' : 'border-primary-300'}
          disabled:bg-primary-100 disabled:cursor-not-allowed
        `}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Input;
