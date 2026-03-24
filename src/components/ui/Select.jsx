import React from 'react';

const Select = ({ 
  label, 
  error, 
  className = '', 
  id,
  options = [],
  placeholder = 'Выберите...',
  ...props 
}) => {
  const selectId = id || label?.toLowerCase().replace(/\s+/g, '-');
  
  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label 
          htmlFor={selectId} 
          className="block text-sm font-medium text-primary-700 mb-1"
        >
          {label}
        </label>
      )}
      <select
        id={selectId}
        className={`
          w-full px-4 py-2.5 border rounded-lg
          focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
          transition-all duration-200
          ${error ? 'border-red-500' : 'border-primary-300'}
          disabled:bg-primary-100 disabled:cursor-not-allowed
          bg-white
        `}
        {...props}
      >
        {placeholder && (
          <option value="">{placeholder}</option>
        )}
        {options.map((option) => (
          <option 
            key={option.value} 
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Select;
