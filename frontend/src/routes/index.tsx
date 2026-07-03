import { createBrowserRouter, Navigate } from 'react-router-dom';
import { DashboardLayout } from '../layouts';
import { CommandCenter } from '../features/dashboard/CommandCenter';
import { TransferFlow } from '../features/transfers/TransferFlow';
import { SecurityCenter } from '../features/security/SecurityCenter';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/',
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
]);
