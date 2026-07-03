import { createBrowserRouter, Navigate } from 'react-router-dom';
import { DashboardLayout, AuthLayout } from '../layouts';
import { CommandCenter } from '../features/dashboard/CommandCenter';
import { TransferFlow } from '../features/transfers/TransferFlow';
import { DecisionDetails } from '../features/transfers/DecisionDetails';
import { SecurityCenter } from '../features/security/SecurityCenter';
import { TransactionsHub } from '../features/transactions/TransactionsHub';
import { AnalyticsDashboard } from '../features/analytics/AnalyticsDashboard';
import { ProfileSettings } from '../features/settings/ProfileSettings';
import { AdminDashboard } from '../features/admin/AdminDashboard';
import { LoginScreen } from '../features/authentication/LoginScreen';
import { AuthGuard, GuestGuard } from '../guards';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/auth',
    element: <GuestGuard />,
    children: [
      {
        path: '',
        element: <AuthLayout />,
        children: [
          {
            path: 'login',
            element: <LoginScreen />
          }
        ]
      }
    ]
  },
  {
    path: '/',
    element: <AuthGuard />,
    children: [
      {
        path: '',
        element: <DashboardLayout />,
        children: [
          {
            path: 'dashboard',
            element: <CommandCenter />
          },
          {
            path: 'transfer',
            element: <TransferFlow />
          },
          {
            path: 'decision/:id',
            element: <DecisionDetails />
          },
          {
            path: 'security',
            element: <SecurityCenter />
          },
          {
            path: 'transactions',
            element: <TransactionsHub />
          },
          {
            path: 'analytics',
            element: <AnalyticsDashboard />
          },
          {
            path: 'settings',
            element: <ProfileSettings />
          },
          {
            path: 'admin',
            element: <AdminDashboard />
          }
        ]
      }
    ]
  }
]);

