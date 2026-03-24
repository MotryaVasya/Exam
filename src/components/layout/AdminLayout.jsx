import React from 'react';
import AdminSidebar from './AdminSidebar';

const AdminLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex bg-primary-50">
      <AdminSidebar />
      <main className="flex-grow p-8 overflow-auto">
        {children}
      </main>
    </div>
  );
};

export default AdminLayout;
