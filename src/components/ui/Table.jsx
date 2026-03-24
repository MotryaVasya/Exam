import React from 'react';

const Table = ({ columns, data, onRowClick, className = '' }) => {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-12 text-primary-500">
        Нет данных для отображения
      </div>
    );
  }

  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="min-w-full divide-y divide-primary-200">
        <thead className="bg-primary-50">
          <tr>
            {columns.map((column, index) => (
              <th
                key={index}
                className={`
                  px-6 py-3 text-left text-xs font-medium text-primary-500 uppercase tracking-wider
                  ${column.className || ''}
                `}
                style={{ width: column.width }}
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-primary-200">
          {data.map((row, rowIndex) => (
            <tr
              key={row.id || rowIndex}
              onClick={() => onRowClick?.(row)}
              className={`${onRowClick ? 'cursor-pointer hover:bg-primary-50' : ''} transition-colors`}
            >
              {columns.map((column, colIndex) => (
                <td
                  key={colIndex}
                  className="px-6 py-4 whitespace-nowrap text-sm text-primary-900"
                >
                  {column.render ? column.render(row[column.accessor], row, rowIndex) : row[column.accessor]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
