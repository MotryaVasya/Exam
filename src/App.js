import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { ToastWrapper } from './components/ui';
import ProtectedRoute from './components/ProtectedRoute';

// Пользовательские страницы
import HomePage from './pages/user/HomePage';
import CatalogPage from './pages/user/CatalogPage';
import WatchDetailPage from './pages/user/WatchDetailPage';
import CartPage from './pages/user/CartPage';
import CheckoutPage from './pages/user/CheckoutPage';
import ProfilePage from './pages/user/ProfilePage';
import AboutPage from './pages/user/AboutPage';
import ContactsPage from './pages/user/ContactsPage';

// Админ страницы
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminUsersPage from './pages/admin/AdminUsersPage';
import AdminWatchesPage from './pages/admin/AdminWatchesPage';
import AdminOrdersPage from './pages/admin/AdminOrdersPage';
import AdminProducersPage from './pages/admin/AdminProducersPage';
import AdminDiscountsPage from './pages/admin/AdminDiscountsPage';
import AdminLogsPage from './pages/admin/AdminLogsPage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <CartProvider>
          <div className="App">
            <Routes>
              {/* Пользовательские маршруты */}
              <Route path="/" element={<HomePage />} />
              <Route path="/catalog" element={<CatalogPage />} />
              <Route path="/catalog/:watchId" element={<WatchDetailPage />} />
              <Route path="/cart" element={<CartPage />} />
              <Route path="/checkout" element={<CheckoutPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/contacts" element={<ContactsPage />} />

              {/* Админ маршруты */}
              <Route
                path="/admin"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/users"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminUsersPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/watches"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminWatchesPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/orders"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminOrdersPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/producers"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminProducersPage />
                  </ProtectedRoute>
                }

                
              />
              <Route
                path="/admin/discounts"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminDiscountsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/logs"
                element={
                  <ProtectedRoute requireAdmin>
                    <AdminLogsPage />
                  </ProtectedRoute>
                }
              />
            </Routes>
            <ToastWrapper />
          </div>
        </CartProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
