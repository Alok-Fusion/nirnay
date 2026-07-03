import { createBrowserRouter, Navigate } from 'react-router-dom';
import { DashboardLayout, AuthLayout } from '../layouts';
import { CommandCenter } from '../features/dashboard/CommandCenter';
import { TransferFlow } from '../features/transfers/TransferFlow';
import { SecurityCenter } from '../features/security/SecurityCenter';
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
            path: 'security',
            element: <SecurityCenter />
          },
          {
            path: 'analytics',
            element: <div>Analytics Placeholder</div>
          },
          {
            path: 'settings',
            element: <div>Settings Placeholder</div>
          }
        ]
      }
    ]
  }
]);
